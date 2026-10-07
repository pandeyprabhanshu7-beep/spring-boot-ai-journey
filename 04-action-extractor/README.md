# Action Item Extractor

Extract explicitly stated tasks, owners, and deadlines into JSON.

An early learning project in my Java-to-AI journey. This is a small API prototype, not a production service.

## What I learned

- Connect a Spring Boot REST endpoint to an LLM over HTTP.
- Separate provider transport from the task-specific prompt.
- Validate input and return safe provider errors without exposing credentials.
- Parse model JSON, while recognizing JSON syntax alone does not validate a business schema.
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
curl -s http://localhost:8080/api/run -H 'Content-Type: application/json' -d '{"text": "Priya will review the API design by Thursday."}'
```

Demo result:

```json
{
  "mode": "demo",
  "result": {
    "tasks": [
      {
        "task": "Review the API design",
        "owner": "Priya",
        "deadline": "Thursday"
      }
    ]
  }
}
```

Live results vary; the example above is a demo fixture.

## Code tour

`Application` starts Spring. `Api` validates requests and defines this task. `AiClient` builds the provider HTTP request with connection and request timeouts. `Errors` maps validation to 400 and provider failures to 502. 

## Design choices and limits

Direct REST integration keeps the provider boundary visible for learning; Spring AI is a future refactor. No conversation memory, persistence, automatic retries, streaming, authentication, or quotas. LLM answers may be wrong. JSON responses are parsed but fields and enums are not yet schema-validated. Human review is required. Supplied text is untrusted and may contain prompt injection; prompt instructions are not a security boundary.

## Interview demo

1. Run tests and the sample request in demo mode.
2. Explain the flow from validated input to system/user messages and provider response.
3. Run live mode with non-sensitive sample data.
4. Discuss one failure case and how you would improve it.

## Next milestone

Add schema validation and evaluation cases for ambiguous input. Then add a Spring AI adapter and compare the abstraction with direct HTTP.

## References

- [Spring Boot requirements](https://docs.spring.io/spring-boot/3.5/system-requirements.html)
- [Provider API](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
