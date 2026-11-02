public class AiTarget {

    public static int classify(int a, int b) {
        if ((sqa.Trace.enter("classify@2:block2", "classify@2:statement1", "L3") && sqa.Trace.decision("classify@2:decision1", sqa.Trace.condition("classify@2:condition1", a > 10) && sqa.Trace.condition("classify@2:condition2", b > 20)))) {
            sqa.Trace.enter("classify@2:block3", "classify@2:statement2", "L3");
            return 1;
        }
        sqa.Trace.enter("classify@2:block1", "classify@2:statement3", "L4");
        return 0;
    }
}
