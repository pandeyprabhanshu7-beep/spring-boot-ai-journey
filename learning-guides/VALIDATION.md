# Validation report — GitHub learning edition

Rechecked locally 7 October 2026. This report separates actual execution from static review. Earlier framework-source parsing and prior visual checks were performed 17 September 2026 on the unchanged companion sources.

## Executed locally

- **21 Python tests passed in this edition**: five attention tests, four TeamCity encoding tests, and the following 12 core tests: six retrieval/citation/vector checks and six context-budget checks.
- **4 TeamCity message-encoding tests passed**: special-character escaping, normal text, message framing and invalid kind rejection.
- **19 Java checks passed** using the Java 17 source launcher: five attention checks, eight retrieval checks, and six context-budget checks.
- **6 Java context-budget checks passed**, including exact fit, zero budget, invalid sizes, duplicate IDs and rank-preserving selection.
- Java/Python retrieval examples agree on the first document and score: `payments-r7`, approximately `0.530330`.
- **5 Bash files passed `bash -n`**, covering four publisher/deployer scripts and the shared helper. No script was executed against a cloud account.
- Eight companion Python sources parsed; six Java sources parsed through the JDK compiler API. Framework parsing is not dependency type checking.
- POM XML, supplied YAML files, JSON/YAML/XML fenced examples and single-line JSON bodies in HTTP examples parsed successfully.
- All guide code fences are balanced; code inclusions resolve to supplied files; all image paths exist.
- **26 SVG figures parsed and rasterized to PNG**. The new transformer and Kubernetes reconciliation diagrams were visually inspected in this edition; selected earlier figures were inspected during the September work.
- Three self-contained HTML editions passed static checks for chapter anchors and embedded SVG image data. They contain 101 teaching/reference chapters plus three contents headings, approximately 49,000 words including code/examples, 113 fenced code/diagram blocks and 31 Mermaid blocks.
- `SOURCES.md` indexes 125 distinct linked primary sources. Links are cited near claims; this is not a claim that every external link was re-crawled by an automated link checker.
- The publication directory excludes Python bytecode caches, generated classes and intermediate draft expansions. It preserves the existing repository applications and supplies a separate guide index.

## Not established by these checks

- No AWS/Azure deployment, registry push, Kubernetes API call, Docker build or real credential exchange was performed.
- TeamCity DSL and Jenkinsfile examples were reviewed as adaptation templates; they were not compiled/executed on those CI servers. Agent configuration, plugins and trust policy are installation-specific.
- No live model endpoint or PostgreSQL/pgvector database was started. Retrieval quality, provider behavior, protocol interoperability and generated-answer accuracy require integration/evaluation tests.
- The Spring project was not dependency-compiled: the available runtime was Java 17 without Maven/Java 21. Its example targets Java 21; the supplied CI/Docker configuration provides a route to a suitable build environment.
- Python dependency ranges are not a resolved, hash-locked transitive environment. Framework examples require dependency resolution and live service configuration.
- Mermaid blocks received structural checks, not a Mermaid renderer parse. The HTML uses independently generated embedded SVG illustrations and preserves Mermaid source for editing.
- Full browser screenshot QA was unavailable because no browser executable was installed. HTML received static checks; illustrations were rendered and inspected separately.

## Implementation boundaries

The full local API examples are learning foundations. The expanded chapters provide additional contracts and integration fragments; they do not silently upgrade the local examples into authenticated, globally quota-controlled production services. In particular, configure and test transport deadlines, cancellation, output/body limits, durable state, per-resource authorization, redacted telemetry and release evaluation before production adaptation.

The AWS/Azure scripts require pre-provisioned roles/resources, trusted release agents, protected immutable release tags and approved digest records. They isolate temporary CLI/kubeconfig files and check image repository scope, but they do not implement organization-specific provenance verification, approval or schema migration policy. See `delivery/README.md`.
