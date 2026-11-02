public class FlowExamples {

    public static int calls;

    public static int select(int n) {
        if ((sqa.Trace.enter("FlowExamples#select(int)@3:block2", "FlowExamples#select(int)@3:statement1", "L4") && sqa.Trace.decision("FlowExamples#select(int)@3:decision1", sqa.Trace.condition("FlowExamples#select(int)@3:condition1", n > 0)))) {
            sqa.Trace.enter("FlowExamples#select(int)@3:block3", "FlowExamples#select(int)@3:statement2", "L4");
            return 1;
        }
        sqa.Trace.enter("FlowExamples#select(int)@3:block1", "FlowExamples#select(int)@3:statement3", "L5");
        return 0;
    }

    public static int select(String s) {
        if ((sqa.Trace.enter("FlowExamples#select(String)@7:block2", "FlowExamples#select(String)@7:statement1", "L8") && sqa.Trace.decision("FlowExamples#select(String)@7:decision1", sqa.Trace.condition("FlowExamples#select(String)@7:condition1", s == null) || sqa.Trace.condition("FlowExamples#select(String)@7:condition2", s.isEmpty())))) {
            sqa.Trace.enter("FlowExamples#select(String)@7:block3", "FlowExamples#select(String)@7:statement2", "L8");
            return 2;
        }
        sqa.Trace.enter("FlowExamples#select(String)@7:block1", "FlowExamples#select(String)@7:statement3", "L9");
        return 3;
    }

    public static int ternary(boolean a, boolean b) {
        sqa.Trace.enter("", "FlowExamples#ternary(boolean,boolean)@11:statement1", "L12");
        return (sqa.Trace.enter("FlowExamples#ternary(boolean,boolean)@11:block1", "FlowExamples#ternary(boolean,boolean)@11:statement2", "L12") && sqa.Trace.choose("FlowExamples#ternary(boolean,boolean)@11:decision1", "FlowExamples#ternary(boolean,boolean)@11:block2", "FlowExamples#ternary(boolean,boolean)@11:block3", sqa.Trace.condition("FlowExamples#ternary(boolean,boolean)@11:condition1", a) && sqa.Trace.condition("FlowExamples#ternary(boolean,boolean)@11:condition2", b))) ? 7 : 9;
    }

    public static long promoted(boolean a) {
        sqa.Trace.enter("", "FlowExamples#promoted(boolean)@14:statement1", "L15");
        return (sqa.Trace.enter("FlowExamples#promoted(boolean)@14:block1", "FlowExamples#promoted(boolean)@14:statement2", "L15") && sqa.Trace.choose("FlowExamples#promoted(boolean)@14:decision1", "FlowExamples#promoted(boolean)@14:block2", "FlowExamples#promoted(boolean)@14:block3", sqa.Trace.condition("FlowExamples#promoted(boolean)@14:condition1", a))) ? nextInt() : nextLong();
    }

    public static Number unbox(boolean a, Integer value) {
        sqa.Trace.enter("", "FlowExamples#unbox(boolean,Integer)@17:statement1", "L18");
        return (sqa.Trace.enter("FlowExamples#unbox(boolean,Integer)@17:block1", "FlowExamples#unbox(boolean,Integer)@17:statement2", "L18") && sqa.Trace.choose("FlowExamples#unbox(boolean,Integer)@17:decision1", "FlowExamples#unbox(boolean,Integer)@17:block2", "FlowExamples#unbox(boolean,Integer)@17:block3", sqa.Trace.condition("FlowExamples#unbox(boolean,Integer)@17:condition1", a))) ? value : 1;
    }

    public static String reference(boolean a) {
        sqa.Trace.enter("", "FlowExamples#reference(boolean)@20:statement1", "L21");
        return (sqa.Trace.enter("FlowExamples#reference(boolean)@20:block1", "FlowExamples#reference(boolean)@20:statement2", "L21") && sqa.Trace.choose("FlowExamples#reference(boolean)@20:decision1", "FlowExamples#reference(boolean)@20:block2", "FlowExamples#reference(boolean)@20:block3", sqa.Trace.condition("FlowExamples#reference(boolean)@20:condition1", a))) ? identity("value") : null;
    }

    public static int throwingArm(boolean a) {
        sqa.Trace.enter("", "FlowExamples#throwingArm(boolean)@23:statement1", "L24");
        return (sqa.Trace.enter("FlowExamples#throwingArm(boolean)@23:block1", "FlowExamples#throwingArm(boolean)@23:statement2", "L24") && sqa.Trace.choose("FlowExamples#throwingArm(boolean)@23:decision1", "FlowExamples#throwingArm(boolean)@23:block2", "FlowExamples#throwingArm(boolean)@23:block3", sqa.Trace.condition("FlowExamples#throwingArm(boolean)@23:condition1", a))) ? Integer.parseInt("invalid") : 5;
    }

    public static int conditionThrows(Boolean a) {
        sqa.Trace.enter("", "FlowExamples#conditionThrows(Boolean)@26:statement1", "L27");
        return (sqa.Trace.enter("FlowExamples#conditionThrows(Boolean)@26:block1", "FlowExamples#conditionThrows(Boolean)@26:statement2", "L27") && sqa.Trace.choose("FlowExamples#conditionThrows(Boolean)@26:decision1", "FlowExamples#conditionThrows(Boolean)@26:block2", "FlowExamples#conditionThrows(Boolean)@26:block3", sqa.Trace.condition("FlowExamples#conditionThrows(Boolean)@26:condition1", a))) ? 1 : 2;
    }

    public static int nextInt() {
        sqa.Trace.enter("FlowExamples#nextInt()@29:block1", "FlowExamples#nextInt()@29:statement1", "L29");
        calls++;
        sqa.Trace.enter("", "FlowExamples#nextInt()@29:statement2", "L29");
        return 7;
    }

    public static long nextLong() {
        sqa.Trace.enter("FlowExamples#nextLong()@30:block1", "FlowExamples#nextLong()@30:statement1", "L30");
        calls++;
        sqa.Trace.enter("", "FlowExamples#nextLong()@30:statement2", "L30");
        return 9L;
    }

    public static <T> T identity(T t) {
        sqa.Trace.enter("FlowExamples#identity(T)@31:block1", "FlowExamples#identity(T)@31:statement1", "L31");
        return t;
    }

    public static int neverCalled(int n) {
        if ((sqa.Trace.enter("FlowExamples#neverCalled(int)@32:block2", "FlowExamples#neverCalled(int)@32:statement1", "L33") && sqa.Trace.decision("FlowExamples#neverCalled(int)@32:decision1", sqa.Trace.condition("FlowExamples#neverCalled(int)@32:condition1", n == 42)))) {
            sqa.Trace.enter("FlowExamples#neverCalled(int)@32:block3", "FlowExamples#neverCalled(int)@32:statement2", "L33");
            return 10;
        }
        sqa.Trace.enter("FlowExamples#neverCalled(int)@32:block1", "FlowExamples#neverCalled(int)@32:statement3", "L34");
        return 20;
    }
}
