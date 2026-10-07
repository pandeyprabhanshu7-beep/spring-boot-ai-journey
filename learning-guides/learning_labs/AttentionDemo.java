import java.util.Arrays;

/** One-query teaching example; not an inference runtime. Java 17+. */
public class AttentionDemo {
    record Result(double[] weights, double[] output) {}

    static Result attention(double[] query, double[][] keys, double[][] values) {
        int d = query.length;
        if (d == 0 || keys.length == 0 || keys.length != values.length)
            throw new IllegalArgumentException("invalid shape");
        int valueDimension = values[0].length;
        if (valueDimension == 0) throw new IllegalArgumentException("empty value");
        for (double q : query) if (!Double.isFinite(q))
            throw new IllegalArgumentException("nonfinite query");
        double[] scores = new double[keys.length];
        for (int i = 0; i < keys.length; i++) {
            if (keys[i].length != d || values[i].length != valueDimension)
                throw new IllegalArgumentException("inconsistent dimensions");
            for (double v : values[i]) if (!Double.isFinite(v))
                throw new IllegalArgumentException("nonfinite value");
            for (int j = 0; j < d; j++) {
                if (!Double.isFinite(keys[i][j]))
                    throw new IllegalArgumentException("nonfinite key");
                scores[i] += query[j] * keys[i][j];
            }
            scores[i] /= Math.sqrt(d);
            if (!Double.isFinite(scores[i])) throw new IllegalArgumentException("score overflow");
        }
        double max = Arrays.stream(scores).max().orElseThrow();
        double[] weights = Arrays.stream(scores).map(s -> Math.exp(s - max)).toArray();
        double sum = Arrays.stream(weights).sum();
        double[] output = new double[valueDimension];
        for (int i = 0; i < weights.length; i++) {
            weights[i] /= sum;
            for (int j = 0; j < valueDimension; j++) output[j] += weights[i] * values[i][j];
        }
        return new Result(weights, output);
    }

    static void close(double actual, double expected) {
        if (Math.abs(actual - expected) > 1e-9) throw new AssertionError(actual + " != " + expected);
    }

    public static void main(String[] args) {
        var result = attention(new double[]{1, 0}, new double[][]{{2, 0}, {1, 1}},
            new double[][]{{10, 0}, {0, 20}});
        close(result.weights()[0], 0.6697615493266569);
        close(Arrays.stream(result.weights()).sum(), 1.0);
        close(result.output()[0], 6.697615493266569);
        close(result.output()[1], 6.604769013466862);
        var equal = attention(new double[]{0}, new double[][]{{1}, {2}}, new double[][]{{10}, {20}});
        close(equal.output()[0], 15.0);
        System.out.println("5 attention checks passed");
        System.out.println("weights: " + Arrays.toString(result.weights()));
        System.out.println("output: " + Arrays.toString(result.output()));
    }
}
