public class FlowExamples {
    public static int calls;
    public static int select(int n) {
        if (n > 0) { return 1; }
        return 0;
    }
    public static int select(String s) {
        if (s == null || s.isEmpty()) { return 2; }
        return 3;
    }
    public static int ternary(boolean a, boolean b) {
        return a && b ? 7 : 9;
    }
    public static long promoted(boolean a) {
        return a ? nextInt() : nextLong();
    }
    public static Number unbox(boolean a, Integer value) {
        return a ? value : 1;
    }
    public static String reference(boolean a) {
        return a ? identity("value") : null;
    }
    public static int throwingArm(boolean a) {
        return a ? Integer.parseInt("invalid") : 5;
    }
    public static int conditionThrows(Boolean a) {
        return a ? 1 : 2;
    }
    public static int nextInt() { calls++; return 7; }
    public static long nextLong() { calls++; return 9L; }
    public static <T> T identity(T t) { return t; }
    public static int neverCalled(int n) {
        if (n == 42) { return 10; }
        return 20;
    }
}
