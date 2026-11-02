/**
 * Copyright 1999-2001,2004 The Apache Software Foundation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.commons.cli;

import java.util.Collection;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;
import java.util.HashSet;

/**
 * <p>Represents list of arguments parsed against
 * a {@link Options} descriptor.<p>
 *
 * <p>It allows querying of a boolean {@link #hasOption(String opt)},
 * in addition to retrieving the {@link #getOptionValue(String opt)}
 * for options requiring arguments.</p>
 *
 * <p>Additionally, any left-over or unrecognized arguments,
 * are available for further processing.</p>
 *
 * @author bob mcwhirter (bob @ werken.com)
 * @author <a href="mailto:jstrachan@apache.org">James Strachan</a>
 * @author John Keyes (john at integralsource.com)
 */
public class CommandLine {

    /**
     * the unrecognised options/arguments
     */
    private List args = new LinkedList();

    /**
     * the processed options
     */
    private Set options = new HashSet();

    /**
     * Map of unique options for ease to get complete list of options
     */
    //    private Set allOptions = new HashSet();
    /**
     * Creates a command line.
     */
    CommandLine() {
        // nothing to do
    }

    /**
     * Query to see if an option has been set.
     *
     * @param opt Short name of the option
     * @return true if set, false if not
     */
    public boolean hasOption(String opt) {
        sqa.Trace.enter("CommandLine#hasOption(String)@65:block1", "CommandLine#hasOption(String)@65:statement1", "L67");
        return options.contains(resolveOption(opt));
    }

    /**
     * Query to see if an option has been set.
     *
     * @param opt character name of the option
     * @return true if set, false if not
     */
    public boolean hasOption(char opt) {
        sqa.Trace.enter("CommandLine#hasOption(char)@76:block1", "CommandLine#hasOption(char)@76:statement1", "L78");
        return hasOption(String.valueOf(opt));
    }

    /**
     * Return the <code>Object</code> type of this <code>Option</code>.
     *
     * @param opt the name of the option
     * @return the type of this <code>Option</code>
     */
    public Object getOptionObject(String opt) {
        sqa.Trace.enter("CommandLine#getOptionObject(String)@87:block7", "CommandLine#getOptionObject(String)@87:statement1", "L89");
        String res = getOptionValue(opt);
        sqa.Trace.enter("", "CommandLine#getOptionObject(String)@87:statement2", "L91");
        Option option = resolveOption(opt);
        if ((sqa.Trace.enter("CommandLine#getOptionObject(String)@87:block5", "CommandLine#getOptionObject(String)@87:statement3", "L92") && sqa.Trace.decision("CommandLine#getOptionObject(String)@87:decision1", sqa.Trace.condition("CommandLine#getOptionObject(String)@87:condition1", option == null)))) {
            sqa.Trace.enter("CommandLine#getOptionObject(String)@87:block6", "CommandLine#getOptionObject(String)@87:statement4", "L94");
            return null;
        }
        sqa.Trace.enter("CommandLine#getOptionObject(String)@87:block4", "CommandLine#getOptionObject(String)@87:statement5", "L97");
        Object type = option.getType();
        sqa.Trace.enter("", "CommandLine#getOptionObject(String)@87:statement6", "L99");
        return (sqa.Trace.enter("CommandLine#getOptionObject(String)@87:block1", "CommandLine#getOptionObject(String)@87:statement7", "L99") && sqa.Trace.choose("CommandLine#getOptionObject(String)@87:decision2", "CommandLine#getOptionObject(String)@87:block2", "CommandLine#getOptionObject(String)@87:block3", (sqa.Trace.condition("CommandLine#getOptionObject(String)@87:condition2", res == null)))) ? null : TypeHandler.createValue(res, type);
    }

    /**
     * Return the <code>Object</code> type of this <code>Option</code>.
     *
     * @param opt the name of the option
     * @return the type of opt
     */
    public Object getOptionObject(char opt) {
        sqa.Trace.enter("CommandLine#getOptionObject(char)@108:block1", "CommandLine#getOptionObject(char)@108:statement1", "L110");
        return getOptionObject(String.valueOf(opt));
    }

    /**
     * Retrieve the argument, if any, of this option.
     *
     * @param opt the name of the option
     * @return Value of the argument if option is set, and has an argument,
     * otherwise null.
     */
    public String getOptionValue(String opt) {
        sqa.Trace.enter("CommandLine#getOptionValue(String)@120:block4", "CommandLine#getOptionValue(String)@120:statement1", "L122");
        String[] values = getOptionValues(opt);
        sqa.Trace.enter("", "CommandLine#getOptionValue(String)@120:statement2", "L124");
        return (sqa.Trace.enter("CommandLine#getOptionValue(String)@120:block1", "CommandLine#getOptionValue(String)@120:statement3", "L124") && sqa.Trace.choose("CommandLine#getOptionValue(String)@120:decision1", "CommandLine#getOptionValue(String)@120:block2", "CommandLine#getOptionValue(String)@120:block3", (sqa.Trace.condition("CommandLine#getOptionValue(String)@120:condition1", values == null)))) ? null : values[0];
    }

    /**
     * Retrieve the argument, if any, of this option.
     *
     * @param opt the character name of the option
     * @return Value of the argument if option is set, and has an argument,
     * otherwise null.
     */
    public String getOptionValue(char opt) {
        sqa.Trace.enter("CommandLine#getOptionValue(char)@134:block1", "CommandLine#getOptionValue(char)@134:statement1", "L136");
        return getOptionValue(String.valueOf(opt));
    }

    /**
     * Retrieves the array of values, if any, of an option.
     *
     * @param opt string name of the option
     * @return Values of the argument if option is set, and has an argument,
     * otherwise null.
     */
    public String[] getOptionValues(String opt) {
        sqa.Trace.enter("CommandLine#getOptionValues(String)@146:block4", "CommandLine#getOptionValues(String)@146:statement1", "L148");
        Option key = resolveOption(opt);
        if ((sqa.Trace.enter("CommandLine#getOptionValues(String)@146:block2", "CommandLine#getOptionValues(String)@146:statement2", "L150") && sqa.Trace.decision("CommandLine#getOptionValues(String)@146:decision1", sqa.Trace.condition("CommandLine#getOptionValues(String)@146:condition1", options.contains(key))))) {
            sqa.Trace.enter("CommandLine#getOptionValues(String)@146:block3", "CommandLine#getOptionValues(String)@146:statement3", "L152");
            return key.getValues();
        }
        sqa.Trace.enter("CommandLine#getOptionValues(String)@146:block1", "CommandLine#getOptionValues(String)@146:statement4", "L155");
        return null;
    }

    /**
     * <p>Retrieves the option object given the long or short option as a String</p>
     * @param opt short or long name of the option
     * @return Canonicalized option
     */
    private Option resolveOption(String opt) {
        sqa.Trace.enter("CommandLine#resolveOption(String)@163:block9", "CommandLine#resolveOption(String)@163:statement1", "L165");
        opt = Util.stripLeadingHyphens(opt);
        sqa.Trace.hit("block", "CommandLine#resolveOption(String)@163:block8");
        sqa.Trace.enter("", "CommandLine#resolveOption(String)@163:statement2", "L166");
        for (Iterator it = options.iterator(); (sqa.Trace.enter("CommandLine#resolveOption(String)@163:block2", "CommandLine#resolveOption(String)@163:statement3", "L166") && sqa.Trace.decision("CommandLine#resolveOption(String)@163:decision1", sqa.Trace.condition("CommandLine#resolveOption(String)@163:condition1", it.hasNext()))); ) {
            sqa.Trace.enter("CommandLine#resolveOption(String)@163:block7", "CommandLine#resolveOption(String)@163:statement4", "L168");
            Option option = (Option) it.next();
            if ((sqa.Trace.enter("CommandLine#resolveOption(String)@163:block5", "CommandLine#resolveOption(String)@163:statement5", "L169") && sqa.Trace.decision("CommandLine#resolveOption(String)@163:decision2", sqa.Trace.condition("CommandLine#resolveOption(String)@163:condition2", opt.equals(option.getOpt()))))) {
                sqa.Trace.enter("CommandLine#resolveOption(String)@163:block6", "CommandLine#resolveOption(String)@163:statement6", "L171");
                return option;
            }
            if ((sqa.Trace.enter("CommandLine#resolveOption(String)@163:block3", "CommandLine#resolveOption(String)@163:statement7", "L173") && sqa.Trace.decision("CommandLine#resolveOption(String)@163:decision3", sqa.Trace.condition("CommandLine#resolveOption(String)@163:condition3", opt.equals(option.getLongOpt()))))) {
                sqa.Trace.enter("CommandLine#resolveOption(String)@163:block4", "CommandLine#resolveOption(String)@163:statement8", "L175");
                return option;
            }
        }
        sqa.Trace.enter("CommandLine#resolveOption(String)@163:block1", "CommandLine#resolveOption(String)@163:statement9", "L179");
        return null;
    }

    /**
     * Retrieves the array of values, if any, of an option.
     *
     * @param opt character name of the option
     * @return Values of the argument if option is set, and has an argument,
     * otherwise null.
     */
    public String[] getOptionValues(char opt) {
        sqa.Trace.enter("CommandLine#getOptionValues(char)@189:block1", "CommandLine#getOptionValues(char)@189:statement1", "L191");
        return getOptionValues(String.valueOf(opt));
    }

    /**
     * Retrieve the argument, if any, of an option.
     *
     * @param opt name of the option
     * @param defaultValue is the default value to be returned if the option
     * is not specified
     * @return Value of the argument if option is set, and has an argument,
     * otherwise <code>defaultValue</code>.
     */
    public String getOptionValue(String opt, String defaultValue) {
        sqa.Trace.enter("CommandLine#getOptionValue(String,String)@203:block4", "CommandLine#getOptionValue(String,String)@203:statement1", "L205");
        String answer = getOptionValue(opt);
        sqa.Trace.enter("", "CommandLine#getOptionValue(String,String)@203:statement2", "L207");
        return (sqa.Trace.enter("CommandLine#getOptionValue(String,String)@203:block1", "CommandLine#getOptionValue(String,String)@203:statement3", "L207") && sqa.Trace.choose("CommandLine#getOptionValue(String,String)@203:decision1", "CommandLine#getOptionValue(String,String)@203:block2", "CommandLine#getOptionValue(String,String)@203:block3", (sqa.Trace.condition("CommandLine#getOptionValue(String,String)@203:condition1", answer != null)))) ? answer : defaultValue;
    }

    /**
     * Retrieve the argument, if any, of an option.
     *
     * @param opt character name of the option
     * @param defaultValue is the default value to be returned if the option
     * is not specified
     * @return Value of the argument if option is set, and has an argument,
     * otherwise <code>defaultValue</code>.
     */
    public String getOptionValue(char opt, String defaultValue) {
        sqa.Trace.enter("CommandLine#getOptionValue(char,String)@219:block1", "CommandLine#getOptionValue(char,String)@219:statement1", "L221");
        return getOptionValue(String.valueOf(opt), defaultValue);
    }

    /**
     * Retrieve any left-over non-recognized options and arguments
     *
     * @return remaining items passed in but not parsed as an array
     */
    public String[] getArgs() {
        sqa.Trace.enter("CommandLine#getArgs()@229:block1", "CommandLine#getArgs()@229:statement1", "L231");
        String[] answer = new String[args.size()];
        sqa.Trace.enter("", "CommandLine#getArgs()@229:statement2", "L233");
        args.toArray(answer);
        sqa.Trace.enter("", "CommandLine#getArgs()@229:statement3", "L235");
        return answer;
    }

    /**
     * Retrieve any left-over non-recognized options and arguments
     *
     * @return remaining items passed in but not parsed as a <code>List</code>.
     */
    public List getArgList() {
        sqa.Trace.enter("CommandLine#getArgList()@243:block1", "CommandLine#getArgList()@243:statement1", "L245");
        return args;
    }

    /**
     * jkeyes
     * - commented out until it is implemented properly
     * <p>Dump state, suitable for debugging.</p>
     *
     * @return Stringified form of this object
     */
    /*
    public String toString() {
        StringBuffer buf = new StringBuffer();
            
        buf.append("[ CommandLine: [ options: ");
        buf.append(options.toString());
        buf.append(" ] [ args: ");
        buf.append(args.toString());
        buf.append(" ] ]");
            
        return buf.toString();
    }
    */
    /**
     * Add left-over unrecognized option/argument.
     *
     * @param arg the unrecognised option/argument.
     */
    void addArg(String arg) {
        sqa.Trace.enter("CommandLine#addArg(String)@275:block1", "CommandLine#addArg(String)@275:statement1", "L277");
        args.add(arg);
    }

    /**
     * Add an option to the command line.  The values of
     * the option are stored.
     *
     * @param opt the processed option
     */
    void addOption(Option opt) {
        sqa.Trace.enter("CommandLine#addOption(Option)@286:block1", "CommandLine#addOption(Option)@286:statement1", "L288");
        options.add(opt);
    }

    /**
     * Returns an iterator over the Option members of CommandLine.
     *
     * @return an <code>Iterator</code> over the processed {@link Option}
     * members of this {@link CommandLine}
     */
    public Iterator iterator() {
        sqa.Trace.enter("CommandLine#iterator()@297:block1", "CommandLine#iterator()@297:statement1", "L299");
        return options.iterator();
    }

    /**
     * Returns an array of the processed {@link Option}s.
     *
     * @return an array of the processed {@link Option}s.
     */
    public Option[] getOptions() {
        sqa.Trace.enter("CommandLine#getOptions()@307:block1", "CommandLine#getOptions()@307:statement1", "L309");
        Collection processed = options;
        sqa.Trace.enter("", "CommandLine#getOptions()@307:statement2", "L312");
        // reinitialise array
        Option[] optionsArray = new Option[processed.size()];
        sqa.Trace.enter("", "CommandLine#getOptions()@307:statement3", "L315");
        // return the array
        return (Option[]) processed.toArray(optionsArray);
    }
}
