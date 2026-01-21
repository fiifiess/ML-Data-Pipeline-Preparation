# Error Analysis - first run test.

## Overview

Initially, generated embeddings, which did not utilize proper semantics were used, which led to very vague results after evaluation. Running the pipeline and making queries led to poor search results, which implied that semantics needed to be integrated into embedding. After switching to Term Frequency-Inverse Document Frequency(TF-IDF), there was a significant improvement in query results matching intended documents. 

## Observed Retrieval Issues / Failure Patterns

* Lower precision scores were attributed to queries containing common words like “maintenance,” “inspection,” or “data” often matched multiple documents.
* Documents with minimal elaboration or short summaries (e.g., early versions of logs, policies) were sometimes ranked lower despite being relevant.
* It was also observed that the strategy of breaking documents into chunks by headings inside the individual documents could also contribute to reducing semantic relevance in documents, as some headings could render certain queries vaghue, since headings could be similar in different documents.
* The use of shared terminology in different documents could also generate significant overlap and confuse the model into returning irrelevant results for particular queries.

## Implications
* Queries requiring precise operational context (e.g., “how to decommission a robot safely”) occasionally returned related but non-specific procedures (like general shutdown or maintenance docs).

* TF-IDF alone is limited for distinguishing nuanced manufacturing procedures with overlapping vocabulary.

## Recommendations
* To introduce semantic embeddings to improve retrieval for queries where TF-IDF fails due to vocabulary overlap.

* To refine chunking strategy to preserve complete procedural context for longer documents.

* To apply document tags / metadata (e.g., scope, equipment type) to help narrow retrieval and improve Precision@K.