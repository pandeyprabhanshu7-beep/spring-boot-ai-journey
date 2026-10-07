# Spring Boot AI Journey

[![Java CI](https://github.com/pandeyprabhanshu7-beep/spring-boot-ai-journey/actions/workflows/ci.yml/badge.svg)](https://github.com/pandeyprabhanshu7-beep/spring-boot-ai-journey/actions/workflows/ci.yml)

A Java backend developer learning practical AI integration through five small, explainable projects.

| Project | Purpose | AI concept |
|---|---|---|
| [AI Q&A](01-ai-qa/README.md) | Explain Java and backend concepts through a stateless question-answer API. | Prompting |
| [Text Summarizer](02-text-summarizer/README.md) | Turn a supplied article or meeting note into a short summary and action items. | Summarization |
| [Support Ticket Triage](03-ticket-triage/README.md) | Classify support tickets into a category and priority for human review. | Classification |
| [Action Item Extractor](04-action-extractor/README.md) | Extract explicitly stated tasks, owners, and deadlines into JSON. | Structured extraction |
| [Document-grounded Q&A](05-document-qa/README.md) | Retrieve relevant paragraphs from a local knowledge file and answer with source IDs. | Retrieval grounding |

## Start here

Read projects in numerical order. Each directory is a standalone Maven application; root `mvn verify` tests all five. Run one at a time on port 8080, or set PORT. All default to labeled demo mode; live mode uses the provider API. No API key is needed for tests.

## Portfolio approach

Pin this repository, write a concise description, and use relevant topics: java, spring-boot, ai, llm, retrieval-augmented-generation. Link it from your resume and LinkedIn. Add a short demo recording after running live requests. A readable portfolio supports evaluation; repository activity alone does not guarantee recruiter outreach.

Treat these as learning prototypes. Record genuine changes and dates in LEARNING_LOG.md. Do not manufacture contributions, backdate commits, or describe generated code as work you have independently mastered. Be able to explain and change every class.

## Validation status

GitHub Actions ran `mvn -B verify` on Java 17 on 2026-10-07: all five applications built successfully and 10 tests passed (zero failures, errors, or skips). [Validation run](https://github.com/pandeyprabhanshu7-beep/spring-boot-ai-journey/actions/runs/37637378765). Tests cover labeled demo responses and blank-input rejection; they do not measure live model accuracy or provider failure behavior. Live model calls remain untested without credentials.

## Reuse

See MASTER_PROMPT.md and PROJECT_INSTRUCTIONS.md. The repository prompt is the durable source of instructions for future work.
