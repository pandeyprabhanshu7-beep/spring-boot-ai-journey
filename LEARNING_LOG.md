# Learning log

## 2026-10-06 — Starter generation

Created five AI learning prototypes with generated starter code. Personal understanding and live-model evaluation are still to be completed.

## 2026-10-07 — GitHub integration and build validation

Uploaded Q&A, summarization, ticket triage, action extraction, and lexical document Q&A. GitHub Actions ran `mvn -B verify` on Java 17: five application builds and 10 tests passed with no failures, errors, or skips.

Evidence: https://github.com/pandeyprabhanshu7-beep/spring-boot-ai-journey/actions/runs/37637378765

Next: run each app locally, explain its classes, then evaluate live responses using non-sensitive sample data. No live demo or accuracy benchmark has been completed.

For each genuine milestone record date, project, what changed, what you learned, evidence, and next step.


## 2026-10-07 — Gradle conversion and AI documentation

Converted the repository and each standalone project to Gradle 8.14.3 with checked-in Unix/Windows wrappers, a Java 17 toolchain, Spring Boot dependency BOM, and Gradle CI. Removed the Maven POM files. Expanded all five READMEs to explain the actual default model, task-specific technique, Java processing, examples, and limitations.

Wrapper JAR checksum matched Gradle's published value. Gradle CI subsequently built all five applications, passed all 10 tests, and packaged each project independently with `bootJar`.

Evidence: https://github.com/pandeyprabhanshu7-beep/spring-boot-ai-journey/actions/runs/37643306756

Live AI behavior still needs a user-run evaluation with credentials and non-sensitive examples.

## 2026-10-07 — Illustrated engineering reference guides

Added three AI-assisted learning references covering AI platforms/RAG/MCP, CI/CD/Kubernetes/AWS/Azure, and Spring AI/Python APIs/interviews. Each has Markdown and self-contained HTML editions, original diagrams, worked examples, source links and explicit implementation boundaries.

Local guide checks passed: 21 Python tests, 19 Java checks, five Bash syntax checks, structured-example parsing, image references and HTML anchors. This records artifact creation and deterministic checks, not personal mastery or a live production deployment. See [learning path](learning-guides/README.md) and [validation report](learning-guides/VALIDATION.md).

Next: run the attention example, explain one complete request trace, then reproduce a failure scenario from each guide.

