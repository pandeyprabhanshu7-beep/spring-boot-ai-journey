# Spring Boot AI Journey

[![Java CI](https://github.com/pandeyprabhanshu7-beep/spring-boot-ai-journey/actions/workflows/ci.yml/badge.svg)](https://github.com/pandeyprabhanshu7-beep/spring-boot-ai-journey/actions/workflows/ci.yml)

Five small Spring Boot applications exploring practical AI integration in Java. Each is a learning prototype with a labeled no-key demo and a real live-provider path.

## Projects and AI techniques

| Project | Purpose | AI technique | Model in live mode |
|---|---|---|---|
| [AI Q&A](01-ai-qa/README.md) | Explain Java and backend concepts through a stateless question-answer API. | Instruction prompting and text generation | `gpt-4o-mini` |
| [Text Summarizer](02-text-summarizer/README.md) | Turn an article or meeting note into a concise summary with only explicitly stated action items. | Text summarization using a constrained instruction | `gpt-4o-mini` |
| [Support Ticket Triage](03-ticket-triage/README.md) | Suggest a support-ticket category and priority for human review. | Zero-shot classification through an LLM prompt | `gpt-4o-mini` |
| [Action Item Extractor](04-action-extractor/README.md) | Extract explicitly stated tasks, owners, and deadlines into machine-readable JSON. | Information extraction with prompted JSON output | `gpt-4o-mini` |
| [Document-grounded Q&A](05-document-qa/README.md) | Retrieve relevant paragraphs from a local knowledge file and generate an answer with source paragraph IDs. | Retrieval-augmented generation (RAG) with lexical retrieval | `gpt-4o-mini` |

All five use **OpenAI GPT-4o mini by default** through Java's `HttpClient` and the Chat Completions API. `OPENAI_MODEL` changes the requested model. The difference between projects is the task instruction and Java processing. Demo mode runs no AI model. These projects do not use Spring AI, train models, create embeddings, or connect to a vector database. Document Q&A adds lexical retrieval before LLM generation.

Read each project's README for its input/output examples, code responsibilities, prompt, data flow, model configuration, limitations, and interview walkthrough.

## Build with Gradle

Prerequisite: JDK 17. Gradle 8.14.3 is pinned by the checked-in wrapper; install no separate Gradle. The distribution checksum is verified and CI validates wrapper JARs.

From the repository root on macOS/Linux:

```bash
./gradlew clean build
./gradlew :01-ai-qa:bootRun
```

From the repository root on Windows PowerShell:

```powershell
.\gradlew.bat clean build
.\gradlew.bat :01-ai-qa:bootRun
```

To work on just one project:

```bash
cd 03-ticket-triage
./gradlew test
./gradlew bootRun
```

On Windows use `.\gradlew.bat` in that folder. Every folder has its own complete Gradle build, settings file, and wrapper; it can be copied to a separate repository. Root build tasks aggregate all five. The first build requires internet access for Gradle and dependencies.

Executable application JARs are written to `<project>/build/libs/<project>-0.1.0.jar`. Run one using `java -jar` or use `bootRun`. Test reports are under `<project>/build/reports/tests/test/index.html`.

## Run live AI

The default `AI_MODE=demo` uses fixed fixtures. For a live run set `AI_MODE=live`, `OPENAI_API_KEY`, and optionally `OPENAI_MODEL` before starting a project. The per-project READMEs include Bash and PowerShell commands. API keys are never required for tests; live API usage incurs provider charges. Run one application at a time on port 8080 or change `PORT`.

## Build files

- `settings.gradle` includes all five applications in the root build.
- Root `build.gradle` aggregates `clean`, `test`, and `build` tasks.
- Each project `build.gradle` uses the Spring Boot 3.5.16 Gradle plugin and the matching dependency BOM, Java 17 toolchain, and JUnit Platform.
- `gradlew`, `gradlew.bat`, and `gradle/wrapper/` make the Gradle version reproducible.
- `.github/workflows/ci.yml` validates wrappers, builds/tests all applications, and packages every project independently.

## Validation status

On 2026-10-07, GitHub Actions ran `./gradlew --no-daemon clean build`: all five application builds and all 10 tests passed. It also ran `bootJar` from each project folder: all five standalone packages succeeded. Wrapper validation passed. [Gradle validation run](https://github.com/pandeyprabhanshu7-beep/spring-boot-ai-journey/actions/runs/37643306756). Live model calls remain untested without credentials. Tests cover labeled demo responses and blank-input rejection, not model accuracy.

## Portfolio and future work

Pin this repository, add relevant topics, and link a short demo recording after running real requests. Record genuine learning and code changes in [LEARNING_LOG.md](LEARNING_LOG.md). Treat this as beginner AI integration experience and be able to explain the Java classes.

Use [MASTER_PROMPT.md](MASTER_PROMPT.md) and [PROJECT_INSTRUCTIONS.md](PROJECT_INSTRUCTIONS.md) for future changes. Example: “Using the master prompt, add a beginner semantic-search project with Gradle.”

## Official references

- [Spring Boot 3.5 system requirements](https://docs.spring.io/spring-boot/3.5/system-requirements.html)
- [Gradle wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)
- [Gradle release checksums](https://gradle.org/release-checksums/)
- [GPT-4o mini model](https://developers.openai.com/api/docs/models/gpt-4o-mini)
