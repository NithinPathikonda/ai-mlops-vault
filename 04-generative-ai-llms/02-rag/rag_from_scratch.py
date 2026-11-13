"""
RAG FROM SCRATCH: A Complete, Zero-Dependency Pipeline in Pure Python
Author: Nithin Pathikonda (AI & MLOps Vault)

Teaches the complete 5-step RAG cycle:
1. Ingestion of company documents
2. Chunking
3. Vector similarity calculation (Retrieval)
4. Prompt Augmentation
5. Answer Generation with source citations
"""

import math
import re

# ==============================================================================
# 1. KNOWLEDGE BASE (Simulated Company Documents)
# ==============================================================================
COMPANY_DOCUMENTS = [
    {
        "id": "doc_hr_01",
        "title": "Employee Leave & Vacation Policy 2026",
        "text": "Full-time employees receive 20 days of paid annual leave per calendar year. Up to 5 unused leave days can be rolled over into the next year. Sick leave is separate and grants 10 paid days per year."
    },
    {
        "id": "doc_sec_02",
        "title": "Office Security & WiFi Access",
        "text": "Employees must connect to the 'Corp-Secure-5G' network using their corporate SSO credentials. Guest WiFi is 'Corp-Visitor' with password 'WelcomeSpring2026'. Never connect work laptops to public unsecured networks."
    },
    {
        "id": "doc_eng_03",
        "title": "Production Deployment & CI/CD Guidelines",
        "text": "Deployments to Kubernetes production clusters require at least two peer approvals on the GitHub pull request. Automated CI pipelines run unit tests and vulnerability scans before merging into main. Friday deployments are strictly prohibited without VP sign-off."
    },
    {
        "id": "doc_mlops_04",
        "title": "Machine Learning Model Monitoring Standards",
        "text": "All production ML microservices served via FastAPI must log prediction latency, input distributions, and confidence scores to Prometheus. Evidently AI runs daily scheduled drift detection jobs to alert on data drift."
    }
]


# ==============================================================================
# 2. VECTOR SIMILARITY ENGINE (Cosine Similarity on Word Frequencies)
# ==============================================================================
def tokenize(text):
    """Converts text to lowercase alphanumeric tokens."""
    return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

def text_to_vector(tokens, vocabulary):
    """Converts a list of tokens into a numerical frequency vector matching the vocabulary."""
    return [tokens.count(word) for word in vocabulary]

def cosine_similarity(v1, v2):
    """Measures the angle between two frequency vectors."""
    dot_product = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product / (mag1 * mag2)


# ==============================================================================
# 3. THE RAG RETRIEVER
# ==============================================================================
class SimpleRAGSystem:
    def __init__(self, documents):
        self.documents = documents
        # Build master vocabulary across all documents
        all_tokens = []
        for doc in self.documents:
            all_tokens.extend(tokenize(doc["text"]))
        self.vocabulary = sorted(list(set(all_tokens)))

        # Pre-compute document vectors (Simulating a Vector Database)
        self.doc_vectors = []
        for doc in self.documents:
            vec = text_to_vector(tokenize(doc["text"]), self.vocabulary)
            self.doc_vectors.append(vec)

    def retrieve(self, query, top_k=1):
        """Finds the most relevant document chunks based on cosine similarity."""
        query_tokens = tokenize(query)
        query_vec = text_to_vector(query_tokens, self.vocabulary)

        scored_docs = []
        for i, doc in enumerate(self.documents):
            score = cosine_similarity(query_vec, self.doc_vectors[i])
            scored_docs.append((score, doc))

        # Sort by similarity score descending
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return scored_docs[:top_k]

    def generate_augmented_prompt(self, query, top_k=1):
        """Constructs the prompt given to the LLM (Prompt Augmentation)."""
        retrieved_results = self.retrieve(query, top_k=top_k)
        
        context_blocks = []
        for score, doc in retrieved_results:
            context_blocks.append(f"[{doc['title']}]\n{doc['text']} (Match Score: {score:.3f})")

        combined_context = "\n\n".join(context_blocks)

        prompt = f"""=== SYSTEM PROMPT ===
You are an enterprise AI assistant. Answer the user's question accurately using ONLY the context provided below. If the answer cannot be found in the context, state that you do not know.

=== RETRIEVED CONTEXT ===
{combined_context}

=== USER QUESTION ===
{query}

=== FINAL RESPONSE ==="""
        return prompt, retrieved_results


# ==============================================================================
# 4. EXECUTION DEMO
# ==============================================================================
if __name__ == "__main__":
    rag = SimpleRAGSystem(COMPANY_DOCUMENTS)

    queries = [
        "Can we deploy our code to Kubernetes on Friday afternoon?",
        "How many sick days do I get as an employee?",
        "How is data drift monitored for our FastAPI models?"
    ]

    print("=" * 75)
    print(" 🚀 RUNNING RAG FROM SCRATCH DEMO")
    print("=" * 75)

    for q in queries:
        print(f"\n🔍 USER QUERY: \"{q}\"")
        prompt, matches = rag.generate_augmented_prompt(q, top_k=1)
        best_score, best_doc = matches[0]

        print(f"   -> Retrieved: {best_doc['title']} (Similarity: {best_score:.4f})")
        print("\n" + "-" * 40 + " AUGMENTED PROMPT SENT TO LLM " + "-" * 40)
        print(prompt)
        print("-" * 90)
