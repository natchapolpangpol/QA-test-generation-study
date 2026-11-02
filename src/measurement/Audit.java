package sqa;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import java.nio.file.*;
import java.util.*;

/** Read-only readiness audit; does not claim coverage or drop unsupported methods. */
public class Audit {
    public static void main(String[] args) throws Exception {
        CompilationUnit cu=StaticJavaParser.parse(Paths.get(args[0]));
        List<MethodDeclaration> methods=cu.findAll(MethodDeclaration.class);
        Map<String,Integer> names=new HashMap<>();
        methods.forEach(m->names.merge(m.getNameAsString(),1,Integer::sum));
        List<String> rows=new ArrayList<>();
        rows.add("method\tline\tsyntax_status\tname_selector_ambiguous\tdetail");
        for(MethodDeclaration m:methods) {
            String status="supported_by_prototype_validator",detail="Still requires compile and semantic validation";
            try { Instrument.validate(m); }
            catch(IllegalArgumentException e) { status="unsupported"; detail=e.getMessage(); }
            rows.add(m.getDeclarationAsString(false,false,false)+"\t"+m.getBegin().get().line+"\t"+status+"\t"+(names.get(m.getNameAsString())>1)+"\t"+detail.replace('\n',' ').replace('\t',' '));
        }
        Files.write(Paths.get(args[1]),rows);
        System.out.println("Audited "+methods.size()+" methods; constructors and field initializers require separate scope policy");
    }
}
