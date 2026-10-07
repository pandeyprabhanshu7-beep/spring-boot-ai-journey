# Support Ticket Triage

Suggest a support-ticket category and priority for human review.

This is a beginner learning prototype for a Java backend developer starting practical AI integration.

## What AI is used?

| Part | Implementation |
|---|---|
| Model in live mode | OpenAI `gpt-4o-mini`, configurable using `OPENAI_MODEL` |
| AI technique | Zero-shot classification through an LLM prompt |
| Integration | Java 17 `HttpClient` calls OpenAI Chat Completions over HTTPS |
| Provider endpoint | `POST https://api.openai.com/v1/chat/completions` |
| AI framework | Direct REST integration; this starter does not use Spring AI or an OpenAI SDK |
| Demo mode | Fixed canned fixture; no model runs and no provider request is made |
| Training | Uses a pretrained model for inference; no training or fine-tuning is performed |

`gpt-4o-mini` is the configured model name, not a model built or hosted by this application. The task-specific system instruction tells the model how to handle the user text. All five portfolio projects use the same default model with different instructions.

## How this project works

1. `Api` receives a ticket description.
2. The instruction supplies a label vocabulary: `billing`, `technical`, `account`, `other`, and priorities `low`, `medium`, `high`.
3. The model is asked to return a JSON object with `category`, `priority`, and `reason`.
4. Jackson parses that model-produced string. Java rejects malformed JSON or a non-object response with HTTP 502.
5. The parsed JSON object is returned in `result` for a person or another service to inspect.

“Zero-shot” means this request supplies an instruction and labels without example classifications. No labeled training dataset or separate classification model is created here.

## Understand the example

The sample outage belongs to the technical category and suggests high priority because it affects all users. A vague ticket such as “it does not work” needs clarification. The current API does not automate routing or act on the predicted priority.

## Run with Gradle

Install **JDK 17** and set `JAVA_HOME` if needed. The checked-in Gradle 8.14.3 wrapper downloads Gradle on the first run, so a separate Gradle install is unnecessary. The first build needs internet access for the distribution and dependencies.

From this project directory on macOS/Linux:

```bash
./gradlew clean build
./gradlew bootRun
```

From this project directory on Windows PowerShell:

```powershell
.\gradlew.bat clean build
.\gradlew.bat bootRun
```

From the repository root, select this project explicitly:

```bash
./gradlew :03-ticket-triage:test
./gradlew :03-ticket-triage:bootRun
```

`./gradlew clean build` at the repository root builds and tests all five projects. The local `settings.gradle` and wrapper allow this folder to build independently when copied into its own repository. Import the folder as a Gradle project in IntelliJ or Eclipse/STS.

## Demo and live modes

The default mode is `demo`: it returns the fixed example below regardless of text. The response is labeled `mode: demo`. Demo mode tests the API and parsing, not AI quality.

For real AI inference on macOS/Linux:

```bash
export AI_MODE=live
export OPENAI_API_KEY='your-own-key'
export OPENAI_MODEL=gpt-4o-mini
./gradlew bootRun
```

For real AI inference in Windows PowerShell:

```powershell
$env:AI_MODE = 'live'
$env:OPENAI_API_KEY = 'your-own-key'
$env:OPENAI_MODEL = 'gpt-4o-mini'
.\gradlew.bat bootRun
```

API usage is billed by the provider. Store the key in your environment and use non-sensitive test text. Stop the existing process before changing mode. Run one project at a time on port 8080 or set `PORT` to another port.

## Request and example output

macOS/Linux:

```bash
curl -s http://localhost:8080/api/run -H 'Content-Type: application/json' -d '{"text": "All users receive HTTP 500 after the deployment."}'
```

Windows PowerShell:

```powershell
$body = @{ text = 'All users receive HTTP 500 after the deployment.' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri 'http://localhost:8080/api/run' -ContentType 'application/json' -Body $body
```

Fixed demo response for this sample:

```json
{
  "mode": "demo",
  "result": {
    "category": "technical",
    "priority": "high",
    "reason": "Service failure affects all users."
  }
}
```

Live results vary. This example is a fixture, not a recorded live provider result.

## AI responsibilities and Java responsibilities

| Responsibility | Component |
|---|---|
| Define task and validate input | `Api.java` (`@NotBlank`, maximum 12,000 characters) |
| Interpret natural language and produce the answer | External LLM in live mode |
| Build system/user messages, send HTTP, read generated content | `AiClient.java` |
| Parse model JSON and ensure the top-level value is an object | Jackson in `Api.java` |
| Map validation and provider exceptions | `Errors.java` |

## Provider request details

`AiClient` sends `model`, `messages`, and `max_completion_tokens: 600`. The messages contain a system instruction and the user input. It reads `choices[0].message.content` from the response. Connection timeout is 10 seconds; request timeout is 30 seconds. Provider failures produce HTTP 502 with a safe message, and blank or oversized input produces HTTP 400.

No streaming, automatic retries, conversation storage, or external tools are implemented. The supplied text is sent to the provider in live mode.

## Design choices and limitations

Prompt-based classification makes it easy to change categories, but repeated live results can vary. The code checks JSON syntax and object type only; it does not enforce required fields, allowed enum values, or schema. The provider request does not enable JSON mode or Structured Outputs.

This API has no authentication, persistence, or rate limit; keep the learning demo local. Prompt instructions do not guarantee correctness or protect against every prompt injection. A change to `OPENAI_MODEL` must select a model available to your API account and compatible with this request format.

## Test scope

Two JUnit/MockMvc tests check a labeled demo response and rejection of blank text. They require no API key. They do not measure live-model quality, schema correctness, citation correctness, or provider timeout behavior. Gradle CI builds the executable Spring Boot JAR and runs the tests; the root README records the current verification evidence.

## Interview walkthrough

1. Describe the user problem and why an LLM is useful here.
2. Show `Api.java` and its task instruction.
3. Explain how `AiClient.java` sends the model request and handles errors.
4. Demonstrate the sample request and explain demo versus live mode.
5. Discuss the limitations and next milestone without claiming production readiness.

## Next milestone

Add schema validation and provider Structured Outputs, then evaluate a labeled ticket set with a confusion matrix.

## Official references

- [GPT-4o mini model](https://developers.openai.com/api/docs/models/gpt-4o-mini)
- [Chat Completions API](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
- [Spring Boot 3.5 Gradle plugin](https://docs.spring.io/spring-boot/3.5/gradle-plugin/index.html)
- [Gradle wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)
