from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_tfidf_index(records):
    texts = [r["text"] for r in records]
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000
    )
    matrix = vectorizer.fit_transform(texts)
    return vectorizer, matrix

def retrieve_tfidf(query, records, vectorizer, matrix, top_k=3):
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, matrix)[0]

    ranked = sorted(
        zip(records, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {
            "document_id": r["document_id"],
            "chunk_id": r.get("chunk_id", None), # just added this. Remove if it causes problems!
            "score": float(score)
        }
        for r, score in ranked[:top_k]
    ]
