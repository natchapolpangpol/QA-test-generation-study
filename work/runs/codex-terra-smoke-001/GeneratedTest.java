import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class GeneratedTest {
    @Test
    public void returnsOneWhenBothConditionsAreTrue() {
        assertEquals(1, AiTarget.classify(11, 21));
    }

    @Test
    public void returnsZeroWhenFirstConditionIsFalse() {
        assertEquals(0, AiTarget.classify(10, 21));
    }

    @Test
    public void returnsZeroWhenSecondConditionIsFalse() {
        assertEquals(0, AiTarget.classify(11, 20));
    }
}