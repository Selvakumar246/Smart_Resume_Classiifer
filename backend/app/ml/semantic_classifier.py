import os
import json
import logging
from pathlib import Path
import numpy as np

logger = logging.getLogger("smart-resume-classification")

class SemanticClassifier:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def __init__(self):
        self.model = None
        self.role_embeddings = {}
        self.profiles = {}
        self.load_profiles()
        self.init_model()
        
    def load_profiles(self):
        profiles_dir = Path(__file__).parent / "role_profiles"
        if not profiles_dir.exists():
            return
            
        for path in profiles_dir.glob("*.json"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    profile = json.load(f)
                    role_id = path.stem  # e.g. "software_engineer"
                    profile["id"] = role_id
                    self.profiles[role_id] = profile
            except Exception as e:
                logger.error(f"Error loading profile {path.name}: {e}")
                
    def init_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            # Load model (downloads or uses local cache)
            # Use all-MiniLM-L6-v2 as requested
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.compute_role_embeddings()
            logger.info("SentenceTransformer model loaded successfully.")
        except Exception as e:
            logger.warning(f"Failed to load sentence-transformers: {e}. Falling back to TF-IDF.")
            self.model = None
            
    def compute_role_embeddings(self):
        if not self.model:
            return
            
        for role_id, profile in self.profiles.items():
            # Combine role title, description and core skills for a rich semantic profile
            role_text = f"Role: {profile['name']}. Description: {profile['description']}. Core Skills: {', '.join(profile['core_skills'])}"
            embedding = self.model.encode(role_text, convert_to_numpy=True)
            self.role_embeddings[role_id] = embedding

    def compute_similarity(self, resume_text: str) -> dict[str, float]:
        """
        Computes the cosine similarity of the resume text against all role profiles.
        Returns a dictionary mapping role_id -> score (0-100).
        """
        scores = {}
        
        # If SentenceTransformers is loaded and embeddings are computed
        if self.model and self.role_embeddings:
            try:
                resume_embedding = self.model.encode(resume_text, convert_to_numpy=True)
                for role_id, role_emb in self.role_embeddings.items():
                    dot_product = np.dot(resume_embedding, role_emb)
                    norm_a = np.linalg.norm(resume_embedding)
                    norm_b = np.linalg.norm(role_emb)
                    similarity = dot_product / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0
                    # Scale similarity from [-1, 1] to [0, 100]
                    scores[role_id] = max(0.0, float(similarity)) * 100.0
                return scores
            except Exception as e:
                logger.error(f"Error in SentenceTransformer semantic comparison: {e}")
                
        # TF-IDF fallback if sentence-transformers is not installed/loaded
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        role_ids = list(self.profiles.keys())
        if not role_ids:
            return {}
            
        docs = []
        for r_id in role_ids:
            profile = self.profiles[r_id]
            docs.append(f"{profile['name']} {profile['description']} {' '.join(profile['core_skills'])}")
            
        try:
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform(docs)
            resume_vector = vectorizer.transform([resume_text])
            similarities = cosine_similarity(resume_vector, tfidf_matrix).ravel()
            for idx, similarity in enumerate(similarities):
                scores[role_ids[idx]] = float(similarity) * 100.0
        except Exception as e:
            logger.error(f"Fallback TF-IDF similarity failed: {e}")
            for r_id in role_ids:
                scores[r_id] = 0.0
                
        return scores
