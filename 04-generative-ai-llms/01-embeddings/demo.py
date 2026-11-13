"""
A simple, zero-dependency demonstration of Embeddings & Cosine Similarity in pure Python.
Perfect for teaching beginners how vectors capture meaning!
"""

import math

def dot_product(v1, v2):
    """Multiplies matching coordinate dimensions and sums them."""
    return sum(a * b for a, b in zip(v1, v2))

def magnitude(v):
    """Calculates vector length: sqrt(x^2 + y^2 + ...)."""
    return math.sqrt(sum(a * a for a in v))

def cosine_similarity(v1, v2):
    """
    Measures the angle between two vectors.
    1.0 = Identical meaning
    0.0 = Completely unrelated
    """
    mag1 = magnitude(v1)
    mag2 = magnitude(v2)
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product(v1, v2) / (mag1 * mag2)


# =====================================================================
# SIMULATED EMBEDDINGS (3 dimensions: [Is_Pet, Is_Feline, Is_Vehicle])
# =====================================================================
concepts = {
    "Golden Retriever (Dog)": [0.95, 0.05, 0.00],
    "Siamese Cat":           [0.92, 0.98, 0.00],
    "Bengal Tiger":          [0.10, 0.99, 0.00],
    "Sports Car":            [0.00, 0.00, 0.95],
}

print("=" * 60)
print(" 🧠 EMBEDDING SIMILARITY DEMONSTRATOR")
print("=" * 60)

cat = concepts["Siamese Cat"]
dog = concepts["Golden Retriever (Dog)"]
tiger = concepts["Bengal Tiger"]
car = concepts["Sports Car"]

print(f"\n1. Siamese Cat vs. Bengal Tiger (Both are felines):")
sim_cat_tiger = cosine_similarity(cat, tiger)
print(f"   Similarity: {sim_cat_tiger:.4f}  (Very High!)")

print(f"\n2. Siamese Cat vs. Golden Retriever (Both are domestic pets):")
sim_cat_dog = cosine_similarity(cat, dog)
print(f"   Similarity: {sim_cat_dog:.4f}  (Moderate-High)")

print(f"\n3. Siamese Cat vs. Sports Car (Totally unrelated):")
sim_cat_car = cosine_similarity(cat, car)
print(f"   Similarity: {sim_cat_car:.4f}  (Near Zero)")

print("\n" + "=" * 60)
print("Conclusion: Embeddings turn semantic meaning into geometry!")
print("=" * 60)
