public class FlowRunner {
    static void equal(Object a,Object b) {
        if (!java.util.Objects.equals(a,b)) throw new AssertionError(a+" != "+b);
    }
    public static void main(String[] args) {
        switch(args[0]) {
            case "intOverload": equal(1,FlowExamples.select(4)); equal(0,FlowExamples.select(-1)); break;
            case "stringOverload":
                equal(2,FlowExamples.select((String)null)); equal(2,FlowExamples.select("")); equal(3,FlowExamples.select("x")); break;
            case "ternaryFalse": equal(9,FlowExamples.ternary(false,true)); break;
            case "ternaryAll":
                equal(9,FlowExamples.ternary(false,true)); equal(9,FlowExamples.ternary(true,false)); equal(7,FlowExamples.ternary(true,true)); break;
            case "promoted":
                equal(7L,FlowExamples.promoted(true)); equal(1,FlowExamples.calls);
                equal(9L,FlowExamples.promoted(false)); equal(2,FlowExamples.calls); break;
            case "unbox":
                try { FlowExamples.unbox(true,null); throw new AssertionError("Expected NPE"); } catch(NullPointerException expected) { }
                equal(Integer.valueOf(1),FlowExamples.unbox(false,null)); break;
            case "reference": equal("value",FlowExamples.reference(true)); equal(null,FlowExamples.reference(false)); break;
            case "throwingArm":
                try { FlowExamples.throwingArm(true); throw new AssertionError("Expected exception"); } catch(NumberFormatException expected) { }
                equal(5,FlowExamples.throwingArm(false)); break;
            case "conditionThrows":
                try { FlowExamples.conditionThrows(null); throw new AssertionError("Expected NPE"); } catch(NullPointerException expected) { } break;
            case "classSubset":
                equal(1,FlowExamples.select(5)); equal(2,FlowExamples.select((String)null)); equal(7,FlowExamples.ternary(true,true)); break;
            default: throw new IllegalArgumentException(args[0]);
        }
        System.out.println("PASS "+args[0]+" calls="+FlowExamples.calls);
    }
}
