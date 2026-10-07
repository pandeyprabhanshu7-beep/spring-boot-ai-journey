package example.atlas;

import java.util.*;
import java.util.regex.Pattern;

/** Standard-library retrieval contract lab. Run: java AtlasCore.java */
public class AtlasCore {
    record Doc(String id, String tenant, String text) {}
    record Hit(Doc doc, double score) {}
    static final List<Doc> DOCS = List.of(
        new Doc("payments-r7", "acme", "Payments rollback: restore the previous verified image digest. Check database migration compatibility before rollback."),
        new Doc("cache-r2", "acme", "Prevent cache stampede with bounded single flight and randomized TTL. A Redis lock needs ownership-aware release."),
        new Doc("vectors-r3", "acme", "Embedding migration requires a new index generation. Never mix vectors from incompatible embedding models."),
        new Doc("private-r1", "globex", "Payments rollback uses the confidential Globex recovery procedure.")
    );

    static Map<String,Integer> terms(String text) {
        Map<String,Integer> result = new HashMap<>();
        var matcher = Pattern.compile("[a-z0-9]+").matcher(text.toLowerCase(Locale.ROOT));
        while (matcher.find()) result.merge(matcher.group(), 1, Integer::sum);
        return result;
    }

    static double score(String query, String text) {
        var a = terms(query); var b = terms(text);
        double dot = a.entrySet().stream().mapToDouble(e -> e.getValue() * b.getOrDefault(e.getKey(), 0)).sum();
        double aa = a.values().stream().mapToDouble(v -> (double)v*v).sum();
        double bb = b.values().stream().mapToDouble(v -> (double)v*v).sum();
        return aa == 0 || bb == 0 ? 0 : dot / Math.sqrt(aa*bb);
    }

    static List<Hit> retrieve(String query, String trustedTenant, int k) {
        if (k < 1 || k > 20) throw new IllegalArgumentException("k outside bounds");
        return DOCS.stream().filter(d -> d.tenant().equals(trustedTenant))
            .map(d -> new Hit(d, score(query, d.text()))).filter(h -> h.score() > 0)
            .sorted(Comparator.comparingDouble(Hit::score).reversed().thenComparing(h -> h.doc().id()))
            .limit(k).toList();
    }

    static double cosine(double[] a, double[] b) {
        if (a.length == 0 || a.length != b.length) throw new IllegalArgumentException("dimensions");
        double aa=0, bb=0, dot=0;
        for (int i=0; i<a.length; i++) {
            if (!Double.isFinite(a[i]) || !Double.isFinite(b[i])) throw new IllegalArgumentException("nonfinite");
            aa += a[i]*a[i]; bb += b[i]*b[i]; dot += a[i]*b[i];
        }
        if (aa == 0 || bb == 0) throw new IllegalArgumentException("zero vector");
        return dot / Math.sqrt(aa*bb);
    }

    static List<Map.Entry<String,Double>> rrf(List<List<String>> rankings, int k) {
        if (k < 1) throw new IllegalArgumentException("k");
        Map<String,Double> scores = new HashMap<>();
        for (var ranking : rankings) {
            int rank=0;
            for (String id : new LinkedHashSet<>(ranking)) scores.merge(id, 1.0/(k + ++rank), Double::sum);
        }
        return scores.entrySet().stream().sorted(Map.Entry.<String,Double>comparingByValue()
            .reversed().thenComparing(Map.Entry.comparingByKey())).toList();
    }

    static void check(boolean condition, String label) {
        if (!condition) throw new AssertionError(label);
    }

    public static void main(String[] args) {
        var hits = retrieve("payments rollback", "acme", 3);
        check(hits.get(0).doc().id().equals("payments-r7"), "first relevant result");
        check(hits.stream().allMatch(h -> h.doc().tenant().equals("acme")), "tenant isolation");
        check(retrieve("payments", "unknown", 3).isEmpty(), "unknown scope");
        check(retrieve("xyzzynonexistent", "acme", 3).isEmpty(), "missing evidence");
        check(Math.abs(cosine(new double[]{1,0}, new double[]{.8,.6}) - .8) < 1e-10, "cosine");
        boolean rejected=false;
        try { cosine(new double[]{0}, new double[]{1}); } catch (IllegalArgumentException e) { rejected=true; }
        check(rejected, "zero vector rejected");
        var fused = rrf(List.of(List.of("A","X","B","Y"), List.of("B","Z","W","A")), 60);
        check(fused.get(0).getKey().equals("B"), "RRF rank");
        check(Math.abs(fused.get(0).getValue() - (1.0/63+1.0/61)) < 1e-10, "RRF score");
        System.out.println("Java core: 8 contract checks passed");
        hits.forEach(h -> System.out.printf(Locale.ROOT, "%s\t%.6f%n", h.doc().id(), h.score()));
    }
}
