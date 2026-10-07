# AI Q&A

Explain Java and backend concepts through a stateless question-answer API.

An early learning project in my Java-to-AI journey. This is a small API prototype, not a production service.

## What I learned

- Connect a Spring Boot REST endpoint to an LLM over HTTP.
- Separate provider transport from the task-specific prompt.
- Validate input and return safe provider errors without exposing credentials.
- Keep AI output separate from deterministic application behavior.
- Use a task-specific system instruction and user input.

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
curl -s http://localhost:8080/api/run -H 'Content-Type: application/json' -d '{"text": "What is dependency injection?"}'
```

Demo result:

```json
{
  "mode": "demo",
  "result": "A dependency is supplied to a class instead of constructed inside it. Constructor injection makes dependencies explicit."
}
```

Live results vary; the example above is a demo fixture.

## Code tour

`Application` starts Spring. `Api` validates requests and defines this task. `AiClient` builds the provider HTTP request with connection and request timeouts. `Errors` maps validation to 400 and provider failures to 502. 

## Design choices and limits

Direct REST integration keeps the provider boundary visible for learning; Spring AI is a future refactor. No conversation memory, persistence, automatic retries, streaming, authentication, or quotas. LLM answers may be wrong.  Supplied text is untrusted and may contain prompt injection; prompt instructions are not a security boundary.

## Interview demo

1. Run tests and the sample request in demo mode.
2. Explain the flow from validated input to system/user messages and provider response.
3. Run live mode with non-sensitive sample data.
4. Discuss one failure case and how you would improve it.

## Next milestone

Add a small evaluation set with expected properties, not exact generated wording. Then add a Spring AI adapter and compare the abstraction with direct HTTP.

## References

- [Spring Boot requirements](https://docs.spring.io/spring-boot/3.5/system-requirements.html)
- [Provider API](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
