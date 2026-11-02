package org.apache.commons.cli;

import static org.junit.Assert.*;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import org.junit.Test;

public class GeneratedTest {
    @Test
    public void emptyCommandLineReturnsAbsentValuesAndEmptyCollections() {
        CommandLine line = new CommandLine();
        assertFalse(line.hasOption("x"));
        assertFalse(line.hasOption('x'));
        assertNull(line.getOptionValue("x"));
        assertNull(line.getOptionValue('x'));
        assertNull(line.getOptionValues("x"));
        assertNull(line.getOptionValues('x'));
        assertNull(line.getOptionObject("x"));
        assertNull(line.getOptionObject('x'));
        assertEquals("fallback", line.getOptionValue("x", "fallback"));
        assertEquals("fallback", line.getOptionValue('x', "fallback"));
        assertArrayEquals(new String[0], line.getArgs());
        assertTrue(line.getArgList().isEmpty());
        assertFalse(line.iterator().hasNext());
        assertEquals(0, line.getOptions().length);
    }

    @Test
    public void resolvesShortLongAndHyphenatedNamesAndReturnsValues() {
        CommandLine line = new CommandLine();
        Option option = new Option("a", "alpha", true, "description");
        option.setArgs(2);
        option.addValue("first");
        option.addValue("second");
        line.addOption(option);

        assertTrue(line.hasOption("a"));
        assertTrue(line.hasOption('a'));
        assertTrue(line.hasOption("-a"));
        assertTrue(line.hasOption("alpha"));
        assertTrue(line.hasOption("--alpha"));
        assertFalse(line.hasOption("other"));
        assertArrayEquals(new String[] {"first", "second"}, line.getOptionValues("--alpha"));
        assertArrayEquals(new String[] {"first", "second"}, line.getOptionValues('a'));
        assertEquals("first", line.getOptionValue("alpha"));
        assertEquals("first", line.getOptionValue('a'));
        assertEquals("first", line.getOptionValue("a", "fallback"));
        assertEquals("first", line.getOptionValue('a', "fallback"));
        assertNull(line.getOptionValues("other"));
    }

    @Test
    public void presentOptionWithoutValueUsesDefaults() {
        CommandLine line = new CommandLine();
        Option flag = new Option("f", "flag", false, "flag");
        line.addOption(flag);
        assertTrue(line.hasOption("flag"));
        assertNull(line.getOptionValues("f"));
        assertNull(line.getOptionValue("f"));
        assertNull(line.getOptionObject("flag"));
        assertNull(line.getOptionObject('f'));
        assertEquals("default", line.getOptionValue("flag", "default"));
        assertEquals("default", line.getOptionValue('f', "default"));
        assertNull(line.getOptionValue("missing", null));
    }

    @Test
    public void convertsTypedOptionValues() {
        CommandLine line = new CommandLine();
        Option number = new Option("n", "number", true, "number");
        number.setType(PatternOptionBuilder.NUMBER_VALUE);
        number.addValue("42");
        line.addOption(number);
        assertEquals(42L, ((Number) line.getOptionObject("--number")).longValue());
        assertEquals(42L, ((Number) line.getOptionObject('n')).longValue());
    }

    @Test
    public void argumentsRetainOrderAndListIsLiveWhileArrayIsSnapshot() {
        CommandLine line = new CommandLine();
        line.addArg("one");
        line.addArg("two");
        String[] snapshot = line.getArgs();
        assertArrayEquals(new String[] {"one", "two"}, snapshot);
        line.getArgList().add("three");
        assertArrayEquals(new String[] {"one", "two"}, snapshot);
        snapshot[0] = "changed";
        assertArrayEquals(new String[] {"one", "two", "three"}, line.getArgs());
        line.getArgList().remove("two");
        assertArrayEquals(new String[] {"one", "three"}, line.getArgs());
    }

    @Test
    public void iteratorAndOptionsExposeProcessedSet() {
        CommandLine line = new CommandLine();
        Option a = new Option("a", false, "a");
        Option b = new Option("b", "beta", false, "b");
        line.addOption(a);
        line.addOption(b);
        line.addOption(a);
        Set<Option> expected = new HashSet<Option>(Arrays.asList(a, b));
        assertEquals(expected, new HashSet<Option>(Arrays.asList(line.getOptions())));
        Set<Option> iterated = new HashSet<Option>();
        for (Iterator it = line.iterator(); it.hasNext();) {
            iterated.add((Option) it.next());
        }
        assertEquals(expected, iterated);
        Option[] snapshot = line.getOptions();
        snapshot[0] = null;
        assertEquals(expected, new HashSet<Option>(Arrays.asList(line.getOptions())));
    }
}