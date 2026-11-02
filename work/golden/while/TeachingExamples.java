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
        int words = 0;
        char last = ' ';
        for (int i = 0; i < str.length(); i++) {
            if (!Character.isLetter(str.charAt(i)) && (last == 's' || last == 'r')) {
                words++;
            }
            last = str.charAt(i);
        }
        if (last == 's' || last == 'r') {
            words++;
        }
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
        sqa.Trace.enter("TeachingExamples#whileLoop(int)@30:block4", "TeachingExamples#whileLoop(int)@30:statement1", "L31");
        int i = 0;
        while ((sqa.Trace.enter("TeachingExamples#whileLoop(int)@30:block2", "TeachingExamples#whileLoop(int)@30:statement2", "L32") && sqa.Trace.decision("TeachingExamples#whileLoop(int)@30:decision1", sqa.Trace.condition("TeachingExamples#whileLoop(int)@30:condition1", i < n)))) {
            sqa.Trace.enter("TeachingExamples#whileLoop(int)@30:block3", "TeachingExamples#whileLoop(int)@30:statement3", "L32");
            i++;
        }
        sqa.Trace.enter("TeachingExamples#whileLoop(int)@30:block1", "TeachingExamples#whileLoop(int)@30:statement4", "L33");
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
