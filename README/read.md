# README

This project simulates an AI-driven data pipeline using a knowledge base of automotive parts manufacturing documentation. The goal is to demonstrate ingestion, processing, and retrieval of structured and semi-structured operational knowledge, supporting RAG-style queries and analytics workflows. The project is intentionally designed to mirror industrial data realities: verbose documentation, overlapping terminology, heterogeneous formats, and imperfect retrieval performance. This repository focuses on data engineering, retrieval evaluation, and error analysis, rather than deploying a production ML system.

## Problem Statement

Manufacturing ops docs are messy, unstructured, and hard to search for sometimes. This project presents a pipeline using natural language processing techniques to embed information in a collection of engineering documents for easier search and retrieval to locate appropriate documents containing requested information from a user's query.

## Project Goals

* Simulate a manufacturing knowledge base used in automotive production environments
* Design a clean ingestion → processing → retrieval → evaluation pipeline
* Establish a TF-IDF baseline for document retrieval
* Quantify retrieval quality using Precision@K
* Analyze failure modes to inform future improvements (embeddings, tagging, chunking)


## Data Layer

### Source Documents

The knowledge base consists of markdown documents representing common automotive manufacturing artifacts, including:

* Machine operation and maintenance manuals
* Safety and emergency shutdown procedures
* Quality inspection and defect handling guides
* Production scheduling and throughput planning documents
* Energy, utilities, and facility monitoring references

Each document was confirmed to:

* Exceed minimal length thresholds
* Contain domain-specific terminology
* Use distinct verb styles and controlled vocabulary divergence
* Anchor semantics to specific operational contexts

This design reduces accidental embedding overlap and improves evaluation realism.

## Preprocessing

Before ingestion, documents undergo:

* Markdown normalization
* Header and section consistency checks
* Removal of non-informative boilerplate
* Validation for minimum semantic density

## Chunking Strategy

Documents are chunked using:

* Section-based segmentation (by headers, rather than by word counts, to preserve meaning)
* Overlap-aware chunk sizing
* Preservation of semantic boundaries (procedures, definitions, steps)

## Pipeline Design

Ingest → Clean → Chunk → Validate → Vectorize (TF-IDF) → Retrieve → Evaluate

## Retrieval Method
The project used TF-IDF vectorization and cosine similarity ranking. TF-IDF was used as a lightweight baseline for this project but can be swapped out for a more robust NLP machine learning model through API calls. The goal if this project was not to build a machine learning model in itself. The plan was to keep the project simple without the use of external models and API calls.

## Evaluation Methodology
The method used for evaluation here was the precision at determined K values.
Three K values (1,3, and 5) were used to determine the number of results to be returned after a query is made. At K=1, the pipeline is successful if the query matches the expected document that is returned by the model. At K=3, three results would be returned and precision is calculated as a percentage of how many of the three results contain the expected document i.e. if one of the three documents is the desired one, then precision is calculated as 1/3 = 0.33. At K=5, five results would be returned and precision is calculated as the percentage of the five documents which actually contain the desired document i.e. if two of the five documents contain the relevant chunks, then precision is 2/5 = 0.4. Results are determined by chunks, not entire documents. It is possible to have results returning different chunks from the same document. In each result returned, the top most result represents the highest precision score form that particular query and points to the document the model recommends for the given query.
The table for the results are displayed in the file "Results.md" to keep this README file concise and organised.

The limitations and next steps are also presented in the "error_analysis.md" file in the "Analysis" folder. 


## Evaluation Results
see Results.md file in Data folder.

## Next Steps

* Metadata-aware reranking

* Feedback loop

* Implement embedding-based retrieval to capture semantic meaning beyond exact term matches.

* Refine chunking logic to maintain procedural context.

* Add tags or metadata to support equipment-specific, process-specific, or safety-critical queries.

* Evaluate retrieval improvements using Precision@K or Recall metrics for real-world query sets.

## Summary

This project demonstrates practical data engineering for AI pipelines, retrieval evaluation beyond surface-level demos and a foundation for scaling toward semantic search or production-grade RAG systems.