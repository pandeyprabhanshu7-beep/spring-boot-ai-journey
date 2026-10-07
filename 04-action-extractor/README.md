# Action Item Extractor

Extract explicitly stated tasks, owners, and deadlines into machine-readable JSON.

This is a beginner learning prototype for a Java backend developer starting practical AI integration.

## What AI is used?

| Part | Implementation |
|---|---|
| Model in live mode | OpenAI `gpt-4o-mini`, configurable using `OPENAI_MODEL` |
| AI technique | Information extraction with prompted JSON output |
| Integration | Java 17 `HttpClient` calls OpenAI Chat Completions over HTTPS |
| Provider endpoint | `POST https://api.openai.com/v1/chat/completions` |
| AI framework | Direct REST integration; this starter does not use Spring AI or an OpenAI SDK |
| Demo mode | Fixed canned fixture; no model runs and no provider request is made |
| Training | Uses a pretrained model for inference; no training or fine-tuning is performed |

`gpt-4o-mini` is the configured model name, not a model built or hosted by this application. The task-specific system instruction tells the model how to handle the user text. All five portfolio projects use the same default model with different instructions.

## How this project works

1. `Api` receives a meeting note or message.
2. Its instruction asks for a `tasks` array, with `task`, `owner`, and `deadline` for each item.
3. The instruction asks the model to use JSON `null` for missing owners or deadlines and extract only stated tasks.
4. Jackson parses the generated text and checks it is a JSON object.
5. The object is returned in `result`; the application does not create reminders or assign work.

The LLM interprets natural language and fills the requested fields. Jackson is the deterministic JSON parser, not the AI model.

## Understand the example

The sample note maps to task “Review the API design”, owner “Priya”, and deadline “Thursday”. For “Review the API design”, the expected owner and deadline should be null. “Thursday” remains a text phrase; the application does not convert it to a date or timezone.

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
./gradlew :04-action-extractor:test
./gradlew :04-action-extractor:bootRun
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
curl -s http://localhost:8080/api/run -H 'Content-Type: application/json' -d '{"text": "Priya will review the API design by Thursday."}'
```

Windows PowerShell:

```powershell
$body = @{ text = 'Priya will review the API design by Thursday.' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri 'http://localhost:8080/api/run' -ContentType 'application/json' -Body $body
```

Fixed demo response for this sample:

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

The starter exposes how extraction works without adding a database. JSON validity does not prove that tasks match the source. Required fields, task arrays, types, and enum/schema rules are not enforced beyond the top-level object check. The request does not use provider Structured Outputs.

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

Add schema validation and evaluation cases for multiple tasks, missing fields, and ambiguous dates.

## Official references

- [GPT-4o mini model](https://developers.openai.com/api/docs/models/gpt-4o-mini)
- [Chat Completions API](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
- [Spring Boot 3.5 Gradle plugin](https://docs.spring.io/spring-boot/3.5/gradle-plugin/index.html)
- [Gradle wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)
