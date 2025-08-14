# semantic_matcher.py

from sentence_transformers import SentenceTransformer, util
import numpy as np

# --- Model Loading ---
# This line downloads the model and loads it into memory. 
# We do this once when the module is loaded, so it's not reloaded on every API call.
print("Loading sentence-transformer model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded successfully.")

def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """
    Calculates the semantic similarity between two texts using a sentence-transformer model.
    Returns a score between 0 and 100.
    """
    # 1. Encode the texts into vector embeddings
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)

    # 2. Calculate the cosine similarity between the embeddings
    # util.cos_sim returns a tensor of tensors, e.g., tensor([[0.75]])
    cosine_scores = util.cos_sim(embedding1, embedding2)
    
    # 3. Get the raw score (e.g., 0.75) and normalize it to a 0-100 scale
    # .item() extracts the raw float value from the tensor
    score = cosine_scores[0][0].item() 
    
    # Normalize score from -1 to 1 range to 0-100 range
    # A score of 0 in similarity is not "bad", so we can map 0->50, 1->100, -1->0
    normalized_score = (score + 1) * 50
    
    return round(normalized_score, 2)