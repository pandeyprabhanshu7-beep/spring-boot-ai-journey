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

Wrapper JAR checksum matched Gradle's published value. Current Gradle build/test evidence is pending CI; prior Maven checks do not validate this migration.
