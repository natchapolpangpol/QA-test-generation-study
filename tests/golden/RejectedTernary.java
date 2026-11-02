public class RejectedTernary {
    public int nested(boolean a,boolean b) { return a ? (b ? 1 : 2) : 3; }
    public int initializer(boolean a) { int n = a ? 1 : 2; return n; }
    public int argument(boolean a) { return Integer.compare(a ? 1 : 2, 3); }
    public int supported(int n) { return n; }
}
