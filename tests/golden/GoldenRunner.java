public class GoldenRunner {
    static void equal(int expected, int actual) {
        if (expected != actual) throw new AssertionError(expected + " != " + actual);
    }
    public static void main(String[] args) {
        switch(args[0]) {
            case "eager":
                equal(0, TeachingExamples.eager(20,10)); equal(0, TeachingExamples.eager(5,30)); break;
            case "short":
                equal(0, TeachingExamples.shortCircuit(20,10)); equal(0, TeachingExamples.shortCircuit(5,30)); break;
            case "eagerFull":
                equal(0, TeachingExamples.eager(20,10)); equal(0, TeachingExamples.eager(5,30)); equal(1, TeachingExamples.eager(20,30)); break;
            case "shortFull":
                equal(0, TeachingExamples.shortCircuit(20,10)); equal(0, TeachingExamples.shortCircuit(5,30)); equal(1, TeachingExamples.shortCircuit(20,30)); break;
            case "countOne": equal(2, TeachingExamples.countWords("cats|dogs")); break;
            case "countBoth": equal(2, TeachingExamples.countWords("cats|dogs")); equal(1, TeachingExamples.countWords("cats|dog")); break;
            case "countRepeat":
                for(int i=0;i<3;i++) equal(2, TeachingExamples.countWords("cats|dogs")); break;
            case "countEmpty": equal(0, TeachingExamples.countWords("")); break;
            case "side":
                equal(0, TeachingExamples.sideEffects(false,true)); equal(1, TeachingExamples.calls);
                equal(1, TeachingExamples.sideEffects(true,true)); equal(3, TeachingExamples.calls); break;
            case "exception":
                try { TeachingExamples.exceptional(null, true); throw new AssertionError("Expected NPE"); }
                catch(NullPointerException expected) { equal(0, TeachingExamples.calls); }
                break;
            case "while": equal(0, TeachingExamples.whileLoop(0)); equal(3, TeachingExamples.whileLoop(3)); break;
            case "nested":
                equal(1, TeachingExamples.nestedConditions(true,true,false));
                equal(0, TeachingExamples.nestedConditions(false,false,true));
                equal(1, TeachingExamples.nestedConditions(true,false,true)); break;
            case "or": equal(1, TeachingExamples.eagerOr(true,false)); equal(2, TeachingExamples.calls); break;
            case "xor":
                equal(1, TeachingExamples.booleanXor(true,false));
                equal(0, TeachingExamples.booleanXor(true,true)); break;
            case "noDecisions": equal(7, TeachingExamples.emptyItems()); break;
            default: throw new IllegalArgumentException(args[0]);
        }
        System.out.println("PASS " + args[0] + " calls=" + TeachingExamples.calls);
    }
}
