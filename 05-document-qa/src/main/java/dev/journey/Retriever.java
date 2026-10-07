package dev.journey;
import java.util.*;
import java.util.stream.*;
import java.nio.charset.StandardCharsets;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
@Service
public class Retriever {
 private final List<String> paragraphs;
 public Retriever() throws java.io.IOException {
  try(var in=new ClassPathResource("knowledge.txt").getInputStream()) {paragraphs=List.of(new String(in.readAllBytes(),StandardCharsets.UTF_8).split("\n\s*\n"));}
 }
 public record Hit(String id,String text,int score){}
 public List<Hit> search(String query) {
  Set<String> words=Arrays.stream(query.toLowerCase(Locale.ROOT).split("[^a-z0-9]+")).filter(w->w.length()>2).collect(Collectors.toSet());
  return IntStream.range(0,paragraphs.size()).mapToObj(i->{String p=paragraphs.get(i);Set<String> tokens=new HashSet<>(Arrays.asList(p.toLowerCase(Locale.ROOT).split("[^a-z0-9]+")));return new Hit("P"+(i+1),p,(int)words.stream().filter(tokens::contains).count());}).filter(h->h.score()>0).sorted(Comparator.comparingInt(Hit::score).reversed().thenComparing(Hit::id)).limit(2).toList();
 }
}
