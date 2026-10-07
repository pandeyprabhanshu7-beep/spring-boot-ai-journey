import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

public class Budget {
    record Passage(String id, int tokens) {}

    static List<Passage> pack(List<Passage> passages, int budget) {
        if (budget < 0) throw new IllegalArgumentException("negative budget");
        var ids = new HashSet<String>();
        for (var p : passages) {
            if (p.tokens() <= 0) throw new IllegalArgumentException("invalid tokens");
            if (!ids.add(p.id())) throw new IllegalArgumentException("duplicate ID");
        }
        var selected = new ArrayList<Passage>();
        int remaining = budget;
        for (var p : passages) {
            if (p.tokens() <= remaining) {
                selected.add(p);
                remaining -= p.tokens();
            }
        }
        return List.copyOf(selected);
    }

    static void check(boolean condition) {
        if (!condition) throw new AssertionError("check failed");
    }

    static void rejects(Runnable operation) {
        try { operation.run(); }
        catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("expected IllegalArgumentException");
    }

    public static void main(String[] args) {
        var values = List.of(new Passage("a", 1400),
            new Passage("b", 1100), new Passage("c", 700));
        check(pack(values, 2200).stream().map(Passage::id).toList()
            .equals(List.of("a", "c")));
        check(pack(List.of(new Passage("a", 100)), 100).size() == 1);
        check(pack(List.of(new Passage("a", 1)), 0).isEmpty());
        rejects(() -> pack(List.of(), -1));
        rejects(() -> pack(List.of(new Passage("a", 0)), 100));
        rejects(() -> pack(List.of(new Passage("a", 1), new Passage("a", 2)), 100));
        System.out.println("6 budget checks passed; selected [a, c]");
    }
}
