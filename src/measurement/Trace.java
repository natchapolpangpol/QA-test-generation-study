package sqa;

import java.io.*;
import java.nio.charset.StandardCharsets;

/** Replay-only recorder. Never included in search fitness or original bug evaluation. */
public final class Trace {
    private static final PrintWriter OUT = open();
    private static long sequence;
    private static PrintWriter open() {
        String path = System.getProperty("sqa.trace");
        if (path == null) throw new IllegalStateException("Set -Dsqa.trace to a new output file");
        try {
            PrintWriter out = new PrintWriter(new OutputStreamWriter(new FileOutputStream(path), StandardCharsets.UTF_8), true);
            Runtime.getRuntime().addShutdownHook(new Thread(out::close));
            return out;
        } catch (IOException e) { throw new UncheckedIOException(e); }
    }
    public static synchronized void hit(String kind, String id) {
        OUT.println((++sequence) + "\t" + Thread.currentThread().getId() + "\t" + kind + "\t" + id);
        if (OUT.checkError()) throw new IllegalStateException("Coverage trace write failed");
    }
    public static boolean condition(String id, boolean value) {
        hit("condition", id + (value ? ":T" : ":F"));
        return value;
    }
    public static boolean decision(String id, boolean value) {
        hit("decision", id + (value ? ":T" : ":F"));
        return value;
    }
    /** Record the selected ternary arm BEFORE its evaluation, preserving the original ?: operands/types. */
    public static boolean choose(String decision, String trueBlock, String falseBlock, boolean value) {
        decision(decision, value);
        hit("block", value ? trueBlock : falseBlock);
        return value;
    }
    public static boolean enter(String block, String statement, String line) {
        if (!block.isEmpty()) hit("block", block);
        if (!statement.isEmpty()) hit("statement", statement);
        if (!line.isEmpty()) hit("line", line);
        return true;
    }
    private Trace() {}
}
