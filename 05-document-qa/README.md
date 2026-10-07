# Document-grounded Q&A

Retrieve relevant paragraphs from a local knowledge file and answer with source IDs.

An early learning project in my Java-to-AI journey. This is a small API prototype, not a production service.

## What I learned

- Connect a Spring Boot REST endpoint to an LLM over HTTP.
- Separate provider transport from the task-specific prompt.
- Validate input and return safe provider errors without exposing credentials.
- Keep AI output separate from deterministic application behavior.
- Retrieve paragraphs with lexical overlap before generating an answer. This is retrieval-augmented generation without embeddings or a vector database.

## Run

Install JDK 17+ and Maven 3.6.3+. From this directory:

```bash
mvn test
mvn spring-boot:run
```

Default demo mode requires no credentials and returns a **fixed canned example regardless of input**. It verifies API wiring, not model quality. The response includes `mode: demo`.

For real AI responses, configure environment variables in your shell:

```bash
export AI_MODE=live
export OPENAI_API_KEY='your-own-key'
export OPENAI_MODEL=gpt-4o-mini
mvn spring-boot:run
```

API usage is billed separately by the provider. Never commit keys. Keep this unauthenticated learning API local.

## Example request

```bash
curl -s http://localhost:8080/api/run -H 'Content-Type: application/json' -d '{"text": "How long are logs retained?"}'
```

Demo result:

```json
{
  "mode": "demo",
  "result": "Logs are retained for 14 days [P1]."
}
```

Document Q&A also returns retrieved paragraph IDs, text, and overlap scores. No lexical match returns `I do not know.` without calling the model. Demo text is still a fixed fixture and is not grounded for arbitrary queries.

## Code tour

`Application` starts Spring. `Api` validates requests and defines this task. `AiClient` builds the provider HTTP request with connection and request timeouts. `Errors` maps validation to 400 and provider failures to 502. `Retriever` loads knowledge.txt, tokenizes text, scores word overlap, and chooses two paragraphs.

## Design choices and limits

Direct REST integration keeps the provider boundary visible for learning; Spring AI is a future refactor. No conversation memory, persistence, automatic retries, streaming, authentication, or quotas. LLM answers may be wrong.  Lexical retrieval misses synonyms, uses no embeddings, and does not guarantee citation correctness. Prompt instructions reduce but do not eliminate prompt injection.

## Interview demo

1. Run tests and the sample request in demo mode.
2. Explain the flow from validated input to system/user messages and provider response.
3. Run live mode with non-sensitive sample data.
4. Discuss one failure case and how you would improve it.

## Next milestone

Add a small evaluation set with expected properties, not exact generated wording. Then replace lexical scoring with embeddings and compare retrieval quality.

## References

- [Spring Boot requirements](https://docs.spring.io/spring-boot/3.5/system-requirements.html)
- [Provider API](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
