public class TeachingExamples {

    static int calls;

    public static int eager(int a, int b) {
        if (a > 10 & b > 20) {
            return 1;
        } else {
            return 0;
        }
    }

    public static int shortCircuit(int a, int b) {
        if (a > 10 && b > 20) {
            return 1;
        } else {
            return 0;
        }
    }

    public static int countWords(String str) {
        sqa.Trace.enter("TeachingExamples#countWords(String)@11:block10", "TeachingExamples#countWords(String)@11:statement1", "L12");
        int words = 0;
        sqa.Trace.enter("", "TeachingExamples#countWords(String)@11:statement2", "L13");
        char last = ' ';
        sqa.Trace.hit("block", "TeachingExamples#countWords(String)@11:block9");
        sqa.Trace.enter("", "TeachingExamples#countWords(String)@11:statement3", "L14");
        for (int i = 0; (sqa.Trace.enter("TeachingExamples#countWords(String)@11:block4", "TeachingExamples#countWords(String)@11:statement4", "L14") && sqa.Trace.decision("TeachingExamples#countWords(String)@11:decision1", sqa.Trace.condition("TeachingExamples#countWords(String)@11:condition1", i < str.length()))); sqa.Trace.hit("block", "TeachingExamples#countWords(String)@11:block5"), sqa.Trace.enter("", "TeachingExamples#countWords(String)@11:statement5", "L14"), i++) {
            if ((sqa.Trace.enter("TeachingExamples#countWords(String)@11:block7", "TeachingExamples#countWords(String)@11:statement6", "L15") && sqa.Trace.decision("TeachingExamples#countWords(String)@11:decision2", sqa.Trace.condition("TeachingExamples#countWords(String)@11:condition2", !Character.isLetter(str.charAt(i))) && (sqa.Trace.condition("TeachingExamples#countWords(String)@11:condition3", last == 's') || sqa.Trace.condition("TeachingExamples#countWords(String)@11:condition4", last == 'r'))))) {
                sqa.Trace.enter("TeachingExamples#countWords(String)@11:block8", "TeachingExamples#countWords(String)@11:statement7", "L15");
                words++;
            }
            sqa.Trace.enter("TeachingExamples#countWords(String)@11:block6", "TeachingExamples#countWords(String)@11:statement8", "L16");
            last = str.charAt(i);
        }
        if ((sqa.Trace.enter("TeachingExamples#countWords(String)@11:block2", "TeachingExamples#countWords(String)@11:statement9", "L18") && sqa.Trace.decision("TeachingExamples#countWords(String)@11:decision3", sqa.Trace.condition("TeachingExamples#countWords(String)@11:condition5", last == 's') || sqa.Trace.condition("TeachingExamples#countWords(String)@11:condition6", last == 'r')))) {
            sqa.Trace.enter("TeachingExamples#countWords(String)@11:block3", "TeachingExamples#countWords(String)@11:statement10", "L18");
            words++;
        }
        sqa.Trace.enter("TeachingExamples#countWords(String)@11:block1", "TeachingExamples#countWords(String)@11:statement11", "L19");
        return words;
    }

    public static boolean touch(boolean value) {
        calls++;
        return value;
    }

    public static int sideEffects(boolean a, boolean b) {
        if (touch(a) && touch(b)) {
            return 1;
        }
        return 0;
    }

    public static int exceptional(Integer a, boolean b) {
        if (a > 0 && touch(b)) {
            return 1;
        }
        return 0;
    }

    public static int whileLoop(int n) {
        int i = 0;
        while (i < n) {
            i++;
        }
        return i;
    }

    public static int nestedConditions(boolean a, boolean b, boolean c) {
        if (a && (b || c)) {
            return 1;
        }
        return 0;
    }

    public static int eagerOr(boolean a, boolean b) {
        if (touch(a) | touch(b)) {
            return 1;
        }
        return 0;
    }

    public static int booleanXor(boolean a, boolean b) {
        if (a ^ b) {
            return 1;
        }
        return 0;
    }

    public static int emptyItems() {
        return 7;
    }

    public static int unsupported(int n) {
        switch(n) {
            case 1:
                return 3;
            default:
                return 7;
        }
    }

    public static int multiline(int a, int b) {
        if (a > 0 && b > 0) {
            return 1;
        }
        return 0;
    }
}
