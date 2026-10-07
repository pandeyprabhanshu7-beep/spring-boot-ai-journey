# AI, Cloud Delivery and Backend Engineering — Learning Guides

Three illustrated guides for Java developers moving from basic AI knowledge to detailed backend and platform design. Read a simple explanation, trace concrete inputs and outputs, run a small example, then study the failure cases and trade-offs.

**Edition:** 7 October 2026. Approximately 49,000 words including code and examples, 101 teaching/reference chapters, 26 original illustrations, 31 editable Mermaid diagrams, and 125 distinct linked primary sources. Counts describe coverage, not a guarantee of expertise or production readiness.

## Choose a guide

| Guide | Markdown | Offline HTML | What you will learn |
|---|---|---|---|
| AI platform engineering | [Read](01_ai_platform_simple_to_advanced.md) | [Download/open](01_ai_platform_simple_to_advanced.html) | Tokens, attention, embeddings, ingestion, hybrid retrieval, RAG, MCP, model serving, evaluation, caching and provider choices |
| CI/CD and Kubernetes | [Read](02_cicd_kubernetes_aws_azure.md) | [Download/open](02_cicd_kubernetes_aws_azure.html) | Container internals, Kubernetes controllers, networking, storage, AWS/Azure identities, ECR/ACR, EKS/AKS, TeamCity, Jenkins and alternatives |
| Spring AI, Python APIs and interviews | [Read](03_spring_ai_python_apis_and_interviews.md) | [Download/open](03_spring_ai_python_apis_and_interviews.html) | Framework subcomponents, paired Java/Python patterns, retrieval APIs, tool execution, streaming, resilience, durable jobs and interview designs |

GitHub renders Markdown directly. To read the styled HTML, clone/download the repository and open [index.html](index.html) locally. Each guide embeds its illustrations and works offline; external reference links still require internet. HTML files committed to GitHub are not automatically a hosted website.

![Transformer attention: projections, matching and weighted mixing](images/learning_transformer.png)

## A practical study route

1. **Understand one request.** Read AI A1–A5. Explain where model weights, documents, embeddings and conversation history live. Run the numerical attention lab below.
2. **Build an API.** Read Spring/Python C1–C6, then the complete implementation chapters. Follow the request through validation, retrieval, model generation and citation validation.
3. **Deliver it.** Read CI/CD B1–B8. Trace a source commit to an image digest, cloud identity, Kubernetes API request, scheduled Pod and healthy endpoint.
4. **Break it deliberately.** Work through provider timeouts, unavailable replicas, invalid citations, lost agent credentials and incompatible schema rollbacks.
5. **Defend the design.** Use the interview questions to state the invariant, bottleneck, chosen trade-off, failure response and measurement. Reconstruct the diagram without looking.

For each session produce evidence: a passing small test, a numerical dry run, a failure trace, or a written decision. Reading alone is not a completed implementation milestone.

## Run the offline examples

From this `learning-guides` directory, with Python 3.10+ and JDK 17+:

```bash
python3 -m unittest discover -s learning_labs -p 'test_*.py'
python3 -m unittest discover -s code/python -p 'test_*.py'
python3 -m unittest discover -s delivery -p 'test_*.py'
java learning_labs/AttentionDemo.java
java code/java-core/AtlasCore.java
java code/java-core/Budget.java
```

These use no API keys and make no live provider calls. The attention example computes weights approximately `[0.669762, 0.330238]` and output `[6.697615, 6.604769]`; it teaches one attention operation, not a complete transformer.

## Directory map and implementation boundaries

| Path | Purpose | Boundary |
|---|---|---|
| `learning_labs/` | Attention mathematics in Java and Python | Small deterministic learning example |
| `code/java-core/` | Retrieval, citation and context-budget contracts | Dependency-free; locally executed |
| `code/python/` | Core tests plus FastAPI/MCP examples | Framework/provider integrations need their own environment |
| `code/spring/` | Standalone Spring AI reference example | Uses the guide's Java 21/Maven baseline; not an added root Gradle application |
| `code/k8s/`, `code/ci/` | Kubernetes and CI adaptation examples | Not deployed or installed as repository workflows |
| `delivery/` | AWS/Azure publisher/deployer scripts, Jenkins and TeamCity templates | Real operations when run; read prerequisites first |
| `images/` | PNG illustrations and editable SVG originals | HTML embeds the SVG equivalents |
| `SOURCES.md` | Linked primary documentation | See source dates and refresh scope |
| `VALIDATION.md` | Executed checks and untested boundaries | Do not interpret static parsing as integration verification |

The five existing applications at the repository root retain their Java 17/Gradle builds. The advanced reference example is supplied with its original documented build baseline to match the guide; it is intentionally outside those applications and their root build. Do not copy Spring AI 2.x dependencies into a Boot 3.x application without choosing a compatible release family.

## Rebuild the readers

The committed HTML is ready to read. To regenerate it, use Node.js 20+ and install `marked` 17.0.5 and `sharp` 0.35.4 into this directory, then run:

```bash
npm install --no-save marked@17.0.5 sharp@0.35.4
node build_readers.cjs
python3 -m pip install PyYAML
python3 validate_bundle.py
```

`build_readers.cjs` rasterizes SVGs and rebuilds the three self-contained readers. The validator checks structured examples, image paths and HTML anchors. Dependency versions identify the builder used for this edition; they are not a security audit or a transitive lockfile. Mermaid source is retained in collapsible sections; the HTML illustrations are separately authored SVGs.

## Research and honesty

Original source research was performed 16–17 September 2026. Spring AI compatibility, MCP protocol revision and the Python MCP SDK API were refreshed on 7 October 2026. The rest of the source set retains its original check date. Numerical examples, workloads and the fictional Atlas system are teaching scenarios, not vendor benchmarks or claims about this repository's production traffic.

These materials were created with AI assistance. They are study references and implementation starting points; personal mastery, live deployment and model-quality claims require separate evidence. See [validation](VALIDATION.md) before adapting the examples.
