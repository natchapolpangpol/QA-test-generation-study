package sqa;

import com.github.javaparser.*;
import com.github.javaparser.ast.*;
import com.github.javaparser.ast.body.*;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.stmt.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.*;

/** Fail-closed prototype for selected methods; unsupported syntax never disappears from a denominator. */
public final class Instrument {
    private final List<Map<String,Object>> items = new ArrayList<>(), nodes = new ArrayList<>(), edges = new ArrayList<>();
    private final Map<Node,String> statement = new IdentityHashMap<>(), block = new IdentityHashMap<>();
    private final Map<ForStmt,String> initBlock = new IdentityHashMap<>(), updateBlock = new IdentityHashMap<>();
    private final Map<ConditionalExpr,String[]> ternaryBlocks = new IdentityHashMap<>();
    private final Map<String,Integer> counts = new HashMap<>();
    private final Set<String> lines = new HashSet<>();
    private String prefix;

    private static Map<String,Object> obj(Object... pairs) {
        Map<String,Object> m = new LinkedHashMap<>();
        for (int i=0; i<pairs.length; i+=2) m.put((String)pairs[i], pairs[i+1]);
        return m;
    }
    private static String json(Object o) {
        if (o == null) return "null";
        if (o instanceof String) {
            StringBuilder b = new StringBuilder("\"");
            for (char c : ((String)o).toCharArray()) {
                if (c=='"' || c=='\\') b.append('\\').append(c);
                else if (c<32) b.append(String.format("\\u%04x",(int)c));
                else b.append(c);
            }
            return b.append('"').toString();
        }
        if (o instanceof Map) {
            List<String> parts = new ArrayList<>();
            ((Map<?,?>)o).forEach((k,v)->parts.add(json(k)+":"+json(v)));
            return "{"+String.join(",",parts)+"}";
        }
        if (o instanceof Collection) {
            List<String> parts = new ArrayList<>();
            for(Object x:(Collection<?>)o) parts.add(json(x));
            return "["+String.join(",",parts)+"]";
        }
        return o.toString();
    }
    private String id(String kind) { return prefix+":"+kind+counts.merge(prefix+kind,1,Integer::sum); }
    private String item(String kind, Node n, String suffix) {
        String key=id(kind);
        items.add(obj("kind",kind,"id",key+suffix,"line",n.getBegin().get().line,"column",n.getBegin().get().column,"source",n.toString()));
        return key;
    }
    private String outcomes(String kind, Node n) {
        String key=item(kind,n,":T");
        items.add(obj("kind",kind,"id",key+":F","line",n.getBegin().get().line,"column",n.getBegin().get().column,"source",n.toString()));
        return key;
    }
    private String line(Node n) {
        String key="L"+n.getBegin().get().line;
        if (lines.add(key)) items.add(obj("kind","line","id",key,"line",n.getBegin().get().line));
        return key;
    }
    private String stmt(Node n) { return statement.computeIfAbsent(n,x->item("statement",x,"")); }
    private String node(Node n, String type, List<Node> members) {
        String key=item("block",n,"");
        List<Integer> locations=new ArrayList<>();
        for(Node x:members) locations.add(x.getBegin().get().line);
        nodes.add(obj("id",key,"type",type,"lines",locations,"source",n.toString(),"counted",true));
        return key;
    }
    private void edge(String a,String b,String label) { edges.add(obj("from",a,"to",b,"label",label)); }
    private static boolean simple(Statement s) { return s.isExpressionStmt() || s.isReturnStmt(); }
    private static Expression unwrap(Expression e) {
        while(e.isEnclosedExpr()) e=e.asEnclosedExpr().getInner();
        return e;
    }
    private static ConditionalExpr returnTernary(Statement s) {
        if(!s.isReturnStmt() || !s.asReturnStmt().getExpression().isPresent()) return null;
        Expression e=unwrap(s.asReturnStmt().getExpression().get());
        return e.isConditionalExpr()?e.asConditionalExpr():null;
    }
    private static boolean linear(Statement s) { return simple(s) && returnTernary(s)==null; }

    // Build source-decision CFG backwards; group maximal straight-line sequences.
    private String cfg(Statement s, String next, String exit) {
        if(s.isEmptyStmt()) return next;
        if(s.isBlockStmt()) {
            NodeList<Statement> list=s.asBlockStmt().getStatements();
            for(int i=list.size()-1;i>=0;) {
                Statement tail=list.get(i);
                if(linear(tail)) {
                    int first=i;
                    while(first>0 && list.get(first-1).isExpressionStmt()) first--;
                    List<Node> members=new ArrayList<>();
                    for(int k=first;k<=i;k++) members.add(list.get(k));
                    String key=node(list.get(first),"process",members);
                    block.put(list.get(first),key);
                    edge(key,tail.isReturnStmt()?exit:next,"next"); next=key; i=first-1;
                } else { next=cfg(tail,next,exit); i--; }
            }
            return next;
        }
        ConditionalExpr ternary=returnTernary(s);
        if(ternary!=null) {
            String predicate=node(ternary.getCondition(),"ternary-decision",Collections.singletonList(ternary.getCondition()));
            String yes=node(ternary.getThenExpr(),"ternary-arm",Collections.singletonList(ternary.getThenExpr()));
            String no=node(ternary.getElseExpr(),"ternary-arm",Collections.singletonList(ternary.getElseExpr()));
            ternaryBlocks.put(ternary,new String[]{predicate,yes,no});
            edge(predicate,yes,"T"); edge(predicate,no,"F");
            edge(yes,exit,"return"); edge(no,exit,"return");
            return predicate;
        }
        if(linear(s)) {
            String key=node(s,"process",Collections.singletonList(s)); block.put(s,key);
            edge(key,s.isReturnStmt()?exit:next,"next"); return key;
        }
        if(s.isIfStmt()) {
            IfStmt x=s.asIfStmt(); String key=node(x.getCondition(),"decision",Collections.singletonList(x.getCondition())); block.put(s,key);
            edge(key,cfg(x.getThenStmt(),next,exit),"T");
            edge(key,x.getElseStmt().isPresent()?cfg(x.getElseStmt().get(),next,exit):next,"F"); return key;
        }
        if(s.isWhileStmt()) {
            WhileStmt x=s.asWhileStmt(); String key=node(x.getCondition(),"decision",Collections.singletonList(x.getCondition())); block.put(s,key);
            edge(key,cfg(x.getBody(),key,exit),"T"); edge(key,next,"F"); return key;
        }
        if(s.isForStmt()) {
            ForStmt x=s.asForStmt(); Expression compare=x.getCompare().get();
            String key=node(compare,"decision",Collections.singletonList(compare)); block.put(s,key);
            String back=key;
            if(!x.getUpdate().isEmpty()) {
                back=node(x.getUpdate().get(0),"for-update",new ArrayList<Node>(x.getUpdate())); updateBlock.put(x,back); edge(back,key,"next");
            }
            edge(key,cfg(x.getBody(),back,exit),"T"); edge(key,next,"F");
            if(!x.getInitialization().isEmpty()) {
                String start=node(x.getInitialization().get(0),"for-init",new ArrayList<Node>(x.getInitialization())); initBlock.put(x,start); edge(start,key,"next"); return start;
            }
            return key;
        }
        throw new IllegalArgumentException("Unsupported statement: "+s.getClass().getSimpleName());
    }
    private static Expression call(String method, Expression... args) {
        return new MethodCallExpr(new NameExpr("sqa.Trace"),method,new NodeList<Expression>(args));
    }
    private static StringLiteralExpr str(String s) { return new StringLiteralExpr(s); }
    private Expression enter(Node n, String blockID) {
        return call("enter",str(blockID==null?"":blockID),str(stmt(n)),str(line(n)));
    }
    private Expression atom(Expression e) {
        if(e.isEnclosedExpr()) return new EnclosedExpr(atom(e.asEnclosedExpr().getInner()));
        if(e.isBinaryExpr()) {
            BinaryExpr b=e.asBinaryExpr(); BinaryExpr.Operator op=b.getOperator();
            if(op==BinaryExpr.Operator.AND || op==BinaryExpr.Operator.OR || op==BinaryExpr.Operator.BINARY_AND || op==BinaryExpr.Operator.BINARY_OR || op==BinaryExpr.Operator.XOR)
                return new BinaryExpr(atom(b.getLeft()),atom(b.getRight()),op);
        }
        // A negated atom is a condition in its written form. Reject negated compounds in v0.1.
        return call("condition",str(outcomes("condition",e)),e.clone());
    }
    private Expression predicate(Statement owner, Expression e) {
        String decision=outcomes("decision",e);
        return new EnclosedExpr(new BinaryExpr(enter(e,block.get(owner)),call("decision",str(decision),atom(e)),BinaryExpr.Operator.AND));
    }
    private BlockStmt rewrite(Statement original) {
        BlockStmt out=new BlockStmt();
        List<Statement> list=original.isBlockStmt()?new ArrayList<>(original.asBlockStmt().getStatements()):Collections.singletonList(original);
        for(Statement s:list) {
            if(s.isEmptyStmt()) continue;
            if(s.isBlockStmt()) { out.addStatement(rewrite(s)); continue; }
            ConditionalExpr ternary=returnTernary(s);
            if(ternary!=null) {
                String[] blocks=ternaryBlocks.get(ternary);
                String decision=outcomes("decision",ternary.getCondition());
                out.addStatement(new ExpressionStmt(enter(s,null)));
                ReturnStmt copy=s.asReturnStmt().clone();
                ConditionalExpr expression=unwrap(copy.getExpression().get()).asConditionalExpr();
                Expression entered=enter(ternary.getCondition(),blocks[0]);
                expression.setCondition(new EnclosedExpr(new BinaryExpr(entered,
                    call("choose",str(decision),str(blocks[1]),str(blocks[2]),atom(ternary.getCondition())),BinaryExpr.Operator.AND)));
                out.addStatement(copy);
                continue;
            }
            if(linear(s)) { out.addStatement(new ExpressionStmt(enter(s,block.get(s)))); out.addStatement(s.clone()); continue; }
            if(s.isIfStmt()) {
                IfStmt x=s.asIfStmt(); IfStmt c=x.clone(); c.setCondition(predicate(s,x.getCondition())); c.setThenStmt(rewrite(x.getThenStmt()));
                if(x.getElseStmt().isPresent()) c.setElseStmt(rewrite(x.getElseStmt().get())); out.addStatement(c);
            } else if(s.isWhileStmt()) {
                WhileStmt x=s.asWhileStmt(); WhileStmt c=x.clone(); c.setCondition(predicate(s,x.getCondition())); c.setBody(rewrite(x.getBody())); out.addStatement(c);
            } else if(s.isForStmt()) {
                ForStmt x=s.asForStmt(); ForStmt c=x.clone();
                if(!x.getInitialization().isEmpty()) {
                    // Emit the init block once before the original for scope. Preserve declarations inside for.
                    out.addStatement(new ExpressionStmt(call("hit",str("block"),str(initBlock.get(x)))));
                    for(Expression e:x.getInitialization()) out.addStatement(new ExpressionStmt(enter(e,null)));
                }
                c.setCompare(predicate(s,x.getCompare().get()));
                NodeList<Expression> updates=new NodeList<>();
                if(!x.getUpdate().isEmpty()) updates.add(call("hit",str("block"),str(updateBlock.get(x))));
                for(Expression e:x.getUpdate()) { updates.add(enter(e,null)); updates.add(e.clone()); }
                c.setUpdate(updates); c.setBody(rewrite(x.getBody())); out.addStatement(c);
            } else throw new IllegalArgumentException("Unsupported: "+s.getClass().getSimpleName());
        }
        return out;
    }
    private static void oneLine(Node n) {
        if(n.getBegin().get().line!=n.getEnd().get().line) throw new IllegalArgumentException("v0.2 rejects multiline executable items at "+n.getRange().get());
    }
    static void validate(MethodDeclaration m) {
        if(!m.getBody().isPresent()) throw new IllegalArgumentException("Method has no body");
        for(Statement s:m.getBody().get().findAll(Statement.class)) {
            if(!(s.isBlockStmt()||s.isIfStmt()||s.isWhileStmt()||s.isForStmt()||simple(s)||s.isEmptyStmt())) throw new IllegalArgumentException("Unsupported syntax "+s.getClass().getSimpleName()+" at "+s.getRange());
            if(simple(s)) oneLine(s);
        }
        for(ForStmt f:m.findAll(ForStmt.class)) {
            if(!f.getCompare().isPresent()) throw new IllegalArgumentException("Infinite for loop unsupported");
            if(f.getInitialization().size()>1) throw new IllegalArgumentException("Multiple for initializers unsupported");
            for(Expression e:f.getInitialization()) {
                oneLine(e);
                if(e.isVariableDeclarationExpr() && e.asVariableDeclarationExpr().getVariables().size()>1) throw new IllegalArgumentException("Multiple for declarations unsupported");
            }
            for(Expression e:f.getUpdate()) oneLine(e);
        }
        List<Expression> predicates=new ArrayList<>();
        m.findAll(IfStmt.class).forEach(x->predicates.add(x.getCondition()));
        m.findAll(WhileStmt.class).forEach(x->predicates.add(x.getCondition()));
        m.findAll(ForStmt.class).forEach(x->predicates.add(x.getCompare().get()));
        predicates.forEach(Instrument::oneLine);
        for(Expression e:m.findAll(Expression.class)) {
            if(e.isConditionalExpr()) {
                ReturnStmt owner=e.findAncestor(ReturnStmt.class).orElse(null);
                if(owner==null || returnTernary(owner)!=e || e.findAll(ConditionalExpr.class).size()!=1)
                    throw new IllegalArgumentException("Only a direct, non-nested return ternary is supported");
                oneLine(e);
            }
            if(e.isLambdaExpr()||e.isSwitchExpr()||e.isMethodReferenceExpr() || (e.isObjectCreationExpr() && e.asObjectCreationExpr().getAnonymousClassBody().isPresent())) throw new IllegalArgumentException("Unsupported nested expression "+e.getClass().getSimpleName());
            if(e.isUnaryExpr() && e.asUnaryExpr().getOperator()==UnaryExpr.Operator.LOGICAL_COMPLEMENT) {
                Expression x=e.asUnaryExpr().getExpression(); while(x.isEnclosedExpr()) x=x.asEnclosedExpr().getInner();
                if(x.isBinaryExpr() && Arrays.asList(BinaryExpr.Operator.AND,BinaryExpr.Operator.OR,BinaryExpr.Operator.BINARY_AND,BinaryExpr.Operator.BINARY_OR,BinaryExpr.Operator.XOR).contains(x.asBinaryExpr().getOperator())) throw new IllegalArgumentException("Negated compound condition unsupported");
            }
        }
    }
    static String signature(MethodDeclaration m) {
        List<String> types=new ArrayList<>();
        m.getParameters().forEach(p->types.add(p.getType().toString().replaceAll("\\s+","")+(p.isVarArgs()?"...":"")));
        return m.getNameAsString()+"("+String.join(",",types)+")";
    }
    private static String owner(MethodDeclaration m) {
        List<String> names=new ArrayList<>();
        Node parent=m.getParentNode().orElse(null);
        while(parent!=null) {
            if(parent instanceof TypeDeclaration) names.add(0,((TypeDeclaration<?>)parent).getNameAsString());
            parent=parent.getParentNode().orElse(null);
        }
        return String.join(".",names);
    }
    public static void main(String[] args) throws Exception {
        if(args.length!=4) throw new IllegalArgumentException("source.java instrumented.java inventory.json methodName|method(Type,...)|Owner#method(Type,...)|class:Owner");
        Path source=Paths.get(args[0]); byte[] bytes=Files.readAllBytes(source);
        StaticJavaParser.setConfiguration(new ParserConfiguration().setLanguageLevel(ParserConfiguration.LanguageLevel.JAVA_11));
        CompilationUnit cu=StaticJavaParser.parse(new String(bytes,StandardCharsets.UTF_8));
        String selector=args[3].replaceAll("\\s+","");
        List<MethodDeclaration> selected;
        List<Map<String,Object>> exclusions=new ArrayList<>();
        if(selector.startsWith("class:")) {
            String className=selector.substring(6);
            List<ClassOrInterfaceDeclaration> classes=cu.findAll(ClassOrInterfaceDeclaration.class,c->c.getNameAsString().equals(className));
            if(classes.size()!=1 || classes.get(0).isInterface()) throw new IllegalArgumentException("Select exactly one concrete class");
            ClassOrInterfaceDeclaration c=classes.get(0);
            selected=new ArrayList<>(c.getMethods());
            for(BodyDeclaration<?> member:c.getMembers()) if(!(member instanceof MethodDeclaration))
                exclusions.add(obj("kind",member.getClass().getSimpleName(),"line",member.getBegin().get().line,"source",member.toString(),"reason","Outside explicit declared-method scope"));
        } else {
            selected=cu.findAll(MethodDeclaration.class,m->selector.equals(m.getNameAsString()) || selector.equals(signature(m)) || selector.equals(owner(m)+"#"+signature(m)));
            if(selected.size()!=1) throw new IllegalArgumentException("Select exactly one unambiguous method; found "+selected.size()+". Use Owner#method(Type,...)");
        }
        if(selected.isEmpty()) throw new IllegalArgumentException("Empty method scope");
        // Validate the ENTIRE requested scope before changing any AST or writing output.
        for(MethodDeclaration m:selected) validate(m);
        Instrument tool=new Instrument();
        List<Map<String,Object>> scopes=new ArrayList<>();
        for(MethodDeclaration m:selected) {
            tool.prefix=owner(m)+"#"+signature(m)+"@"+m.getBegin().get().line;
            String exit=tool.prefix+":EXIT";
            tool.nodes.add(obj("id",exit,"type","exit","counted",false));
            String entry=tool.cfg(m.getBody().get(),exit,exit);
            scopes.add(obj("method",owner(m)+"#"+signature(m),"line",m.getBegin().get().line,"entry",entry,"exit",exit));
            BlockStmt replacement=tool.rewrite(m.getBody().get()); m.setBody(replacement);
        }
        StringBuilder hash=new StringBuilder(); for(byte b:MessageDigest.getInstance("SHA-256").digest(bytes)) hash.append(String.format("%02x",b));
        Map<String,Object> inventory=obj("schema_version",2,"measurement_version","0.2-prototype","scope",args[3],"scope_policy","Selected declared method bodies only; constructors, fields, initializer blocks and nested class members excluded","methods",scopes,"excluded_members",exclusions,"source",source.toAbsolutePath().toString(),"source_sha256",hash.toString(),"line_policy","single-line executable items only; instrumentation attempts count as reached","statement_policy","simple statements plus predicate evaluation (including direct return ternary), for-init and update expressions; entry/sink excluded","entry",scopes.get(0).get("entry"),"items",tool.items,"cfg_nodes",tool.nodes,"cfg_edges",tool.edges);
        Path output=Paths.get(args[1]); Files.createDirectories(output.toAbsolutePath().getParent()); Files.writeString(output,cu.toString());
        Path manifest=Paths.get(args[2]); Files.createDirectories(manifest.toAbsolutePath().getParent()); Files.writeString(manifest,json(inventory));
        System.out.println("Instrumented "+args[3]+"; inventory items="+tool.items.size());
    }
}
