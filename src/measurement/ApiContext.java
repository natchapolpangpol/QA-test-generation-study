package sqa;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.body.*;
import java.nio.file.*;
import java.util.*;

/** Dependency signatures for equal model context; no tests, bug reports or patch information. */
public class ApiContext {
    public static void main(String[] args) throws Exception {
        List<String> lines=new ArrayList<>();
        try(java.util.stream.Stream<Path> stream=Files.list(Paths.get(args[0]))) {
            for(Path file:stream.filter(p->p.toString().endsWith(".java")).sorted().toArray(Path[]::new)) {
                if(file.getFileName().toString().equals("CommandLine.java")) continue;
                for(TypeDeclaration<?> type:StaticJavaParser.parse(file).getTypes()) {
                    lines.add("Type "+type.getNameAsString());
                    if(type instanceof ClassOrInterfaceDeclaration) {
                        ClassOrInterfaceDeclaration c=(ClassOrInterfaceDeclaration)type;
                        lines.add("extends "+c.getExtendedTypes()+" implements "+c.getImplementedTypes());
                    }
                    for(BodyDeclaration<?> member:type.getMembers()) {
                        if(member instanceof MethodDeclaration && !((MethodDeclaration)member).isPrivate())
                            lines.add(((MethodDeclaration)member).getDeclarationAsString()+";");
                        if(member instanceof ConstructorDeclaration && !((ConstructorDeclaration)member).isPrivate())
                            lines.add(((ConstructorDeclaration)member).getDeclarationAsString()+";");
                        if(member instanceof FieldDeclaration && ((FieldDeclaration)member).isPublic())
                            lines.add(member.toString());
                    }
                    lines.add("");
                }
            }
        }
        Files.write(Paths.get(args[1]),lines);
    }
}
