package org.apache.commons.cli;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import org.junit.Test;
import static org.junit.Assert.*;

public class GeneratedTest {
    @Test
    public void emptyCommandLineReturnsEmptyCollectionsAndMissingValues() {
        CommandLine line = new CommandLine();
        assertFalse(line.hasOption("missing"));
        assertFalse(line.hasOption('x'));
        assertNull(line.getOptionValue("missing"));
        assertNull(line.getOptionValue('x'));
        assertNull(line.getOptionValues("missing"));
        assertNull(line.getOptionValues('x'));
        assertNull(line.getOptionObject("missing"));
        assertNull(line.getOptionObject('x'));
        assertEquals("fallback", line.getOptionValue("missing", "fallback"));
        assertEquals("fallback", line.getOptionValue('x', "fallback"));
        assertNull(line.getOptionValue("missing", null));
        assertArrayEquals(new String[0], line.getArgs());
        assertTrue(line.getArgList().isEmpty());
        assertEquals(0, line.getOptions().length);
        assertFalse(line.iterator().hasNext());
    }

    @Test
    public void resolvesShortAndLongNamesWithLeadingHyphens() {
        CommandLine line = new CommandLine();
        Option output = new Option("o", "output", true, "output destination");
        output.addValue("result.txt");
        line.addOption(output);

        for (String name : new String[] {"o", "-o", "--o", "output", "-output", "--output"}) {
            assertTrue(name, line.hasOption(name));
            assertEquals(name, "result.txt", line.getOptionValue(name));
            assertArrayEquals(new String[] {"result.txt"}, line.getOptionValues(name));
            assertEquals("result.txt", line.getOptionValue(name, "unused"));
        }
        assertTrue(line.hasOption('o'));
        assertEquals("result.txt", line.getOptionValue('o'));
        assertArrayEquals(new String[] {"result.txt"}, line.getOptionValues('o'));
        assertEquals("result.txt", line.getOptionValue('o', "unused"));
        assertFalse(line.hasOption("OUTPUT"));
        assertFalse(line.hasOption("absent"));
        assertNull(line.getOptionValues("absent"));
        assertNull(line.getOptionObject("absent"));
    }

    @Test
    public void presentOptionsWithoutValuesReturnNullAndUseDefaults() {
        CommandLine line = new CommandLine();
        Option flag = new Option("v", "verbose", false, "verbose mode");
        flag.setType(PatternOptionBuilder.STRING_VALUE);
        line.addOption(flag);
        Option argument = new Option("a", true, "argument not supplied");
        argument.setType(PatternOptionBuilder.STRING_VALUE);
        line.addOption(argument);

        assertTrue(line.hasOption("--verbose"));
        assertTrue(line.hasOption('a'));
        assertNull(line.getOptionValues('v'));
        assertNull(line.getOptionValue("verbose"));
        assertNull(line.getOptionObject('v'));
        assertNull(line.getOptionObject("a"));
        assertEquals("default", line.getOptionValue('v', "default"));
        assertEquals("default", line.getOptionValue("a", "default"));
        assertFalse(line.hasOption("missing"));
    }

    @Test
    public void multipleValuesKeepTheirOrderAndFirstValueIsSelected() {
        CommandLine line = new CommandLine();
        Option include = new Option("i", "include", true, "include paths");
        include.setArgs(3);
        include.addValue("first");
        include.addValue("");
        include.addValue("third");
        line.addOption(include);

        assertArrayEquals(new String[] {"first", "", "third"}, line.getOptionValues('i'));
        assertArrayEquals(new String[] {"first", "", "third"}, line.getOptionValues("--include"));
        assertEquals("first", line.getOptionValue("include"));

        Option empty = new Option("e", true, "empty value");
        empty.addValue("");
        line.addOption(empty);
        assertEquals("", line.getOptionValue('e', "fallback"));
        assertArrayEquals(new String[] {""}, line.getOptionValues('e'));
    }

    @Test
    public void typedStringValuesAreReturnedThroughBothOverloads() {
        CommandLine line = new CommandLine();
        Option text = new Option("t", "text", true, "text value");
        text.setType(PatternOptionBuilder.STRING_VALUE);
        text.addValue("hello world");
        line.addOption(text);

        assertEquals("hello world", line.getOptionObject('t'));
        assertEquals("hello world", line.getOptionObject("--text"));
        assertEquals("hello world", line.getOptionValue("text"));
    }

    @Test
    @SuppressWarnings({"rawtypes", "unchecked"})
    public void argumentsPreserveOrderAndExposeLiveListButSnapshotArray() {
        CommandLine line = new CommandLine();
        line.addArg("first");
        line.addArg("--unknown");
        line.addArg("first");
        line.addArg(null);
        assertArrayEquals(new String[] {"first", "--unknown", "first", null}, line.getArgs());
        List arguments = line.getArgList();
        assertEquals(Arrays.asList("first", "--unknown", "first", null), arguments);
        assertSame(arguments, line.getArgList());

        String[] snapshot = line.getArgs();
        snapshot[0] = "changed";
        assertEquals("first", line.getArgs()[0]);
        arguments.remove(1);
        arguments.add("last");
        assertArrayEquals(new String[] {"first", "first", null, "last"}, line.getArgs());
        line.addArg("later");
        assertEquals("later", arguments.get(arguments.size() - 1));
    }

    @Test
    @SuppressWarnings("rawtypes")
    public void optionArrayAndIteratorContainMembersAndIteratorCanRemove() {
        CommandLine line = new CommandLine();
        Option alpha = new Option("a", "alpha", false, "alpha flag");
        Option beta = new Option("b", false, "beta flag");
        line.addOption(alpha);
        line.addOption(beta);
        line.addOption(alpha);

        Option[] snapshot = line.getOptions();
        assertEquals(2, snapshot.length);
        Set<Option> expected = new HashSet<Option>(Arrays.asList(alpha, beta));
        assertEquals(expected, new HashSet<Option>(Arrays.asList(snapshot)));
        snapshot[0] = null;
        assertEquals(expected, new HashSet<Option>(Arrays.asList(line.getOptions())));

        Set<Option> visited = new HashSet<Option>();
        Iterator iterator = line.iterator();
        while (iterator.hasNext()) {
            visited.add((Option) iterator.next());
        }
        assertEquals(expected, visited);

        iterator = line.iterator();
        Option removed = (Option) iterator.next();
        iterator.remove();
        assertFalse(line.hasOption(removed.getOpt()));
        assertEquals(1, line.getOptions().length);
        Option remaining = line.getOptions()[0];
        assertTrue(line.hasOption(remaining.getOpt()));
        assertNotSame(removed, remaining);
    }
}
