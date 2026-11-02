import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class GeneratedTest {
    @Test
    public void bothConditionsTrue() {
        assertEquals(1, AiTarget.classify(11, 21));
    }

    @Test
    public void firstTrueSecondFalseAtBoundary() {
        assertEquals(0, AiTarget.classify(11, 20));
    }

    @Test
    public void firstFalseShortCircuitsWithSecondOtherwiseTrue() {
        assertEquals(0, AiTarget.classify(10, 21));
    }

    @Test
    public void firstFalseShortCircuitsWithSecondOtherwiseFalse() {
        assertEquals(0, AiTarget.classify(10, 20));
    }
}