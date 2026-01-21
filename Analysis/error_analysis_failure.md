# Error Analysis - failure test.

This document explains why the failures happened after running the pipeline evaluation with intentionally ambiguous queries. This was done to 'stress test' the pipeline and embedding system to look for weaknesses that can be improved in the next phase of development in this project.

## Process

This evaluation focused on intentionally ambiguous, natural-language queries designed to stress-test a TF-IDF–based retrieval system operating at the chunk level. While performance was strong for explicit keyword queries, results degraded significantly under ambiguity, revealing important system limitations.

## Query 1: “machine stopped unexpectedly during operation”
Precision@5: 0.00

Expected primary document:

Production Line Downtime Response Playbook

Observed behavior:
The retriever surfaced safety protocols, operating guidelines, and training documents instead of downtime response documentation.

Root cause:

The query contains generic operational terms (“machine”, “operation”, “stopped”) that appear across many documents.

TF-IDF overweighted surface-level term frequency rather than incident-response intent.

Chunk-level retrieval fragmented procedural context, preventing escalation-oriented documents from ranking higher.


## Query 2: “software issue reported by operators on the line”
Precision@5: 0.00

Expected primary document:

Incident Reporting Workflow

Observed behavior:
Results favored the Machine Software Update Policy and customer feedback documents.

Root cause:

Strong lexical overlap on “software” dominated ranking.

The phrase “reported by operators” implies process escalation, but TF-IDF cannot model reporting workflows or organizational roles.

Incident management concepts are semantically implied, not explicitly named.


## Query 3: “power usage seems higher than normal”
Precision@5: 0.00

Expected primary document:

Energy Consumption Monitoring

Observed behavior:
Energy monitoring ranked below logs, decommissioning, and inventory documents.

Root cause:

Informal phrasing (“seems higher than normal”) lacks explicit domain keywords like “energy”, “consumption”, or “utilities”.

TF-IDF failed to infer anomaly detection or monitoring intent.

Chunk fragmentation diluted context from energy-focused sections.


## Query 4: “maintenance keeps happening on the same equipment”
Precision@5: 0.00

Expected primary document:

Root Cause Analysis Framework

Observed behavior:
Preventive and predictive maintenance documents ranked higher.

Root cause:

Repeated references to “maintenance” biased ranking toward maintenance execution rather than failure recurrence analysis.

Root cause analysis relies on conceptual escalation, not repeated lexical signals.

TF-IDF cannot infer systemic failure patterns.


## Query 5: “who decides when production jobs get delayed”
Precision@5: 0.40

Expected primary document:

Production Scheduling Rules

Observed behavior:
Correct document appeared at rank 1 and rank 5, alongside unrelated telemetry documents.

Root cause:

Presence of governance language (“who decides”) partially aligned with scheduling rules.

However, vague phrasing allowed unrelated operational documents to enter top results.


## Summary of Failure Patterns

| Failure Category          | Impact                                                          |
| ------------------------- | --------------------------------------------------------------- |
| Implicit intent           | TF-IDF cannot infer escalation, governance, or diagnostic goals |
| Generic vocabulary        | Common operational terms dominate ranking                       |
| Chunk-level fragmentation | Critical procedural context is split across chunks              |
| Lack of semantics         | No understanding of cause, responsibility, or abnormality       |


## Implications for System Design

Implications for System Design

These results demonstrate that while TF-IDF performs well for explicit keyword matching, it is not sufficient for intent-driven industrial queries. This limitation is expected and acceptable for a baseline retrieval system, and it motivates future enhancements such as:

Semantic embeddings for intent inference

Query expansion or intent tagging

Hierarchical or document-aware chunking strategies