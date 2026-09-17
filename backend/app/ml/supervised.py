from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np

from app.core.config import get_settings
from app.ml.taxonomy import CATEGORY_PROFILES


@lru_cache(maxsize=1)
def load_supervised_model():
    path = Path(get_settings().model_path)
    if not path.exists():
        return None
    try:
        bundle = joblib.load(path)
        if not all(key in bundle for key in ("pipeline", "labels", "metrics")):
            return None
        return bundle
    except Exception:
        return None


def predict_supervised(text: str, target_role: str, top_k: int = 5) -> tuple[list[dict], dict] | None:
    bundle = load_supervised_model()
    if not bundle:
        return None
    pipeline = bundle["pipeline"]
    query = f"{text}\nTarget role: {target_role}" if target_role else text
    probabilities = pipeline.predict_proba([query])[0]
    classes = pipeline.classes_
    ranked = np.argsort(probabilities)[::-1][:top_k]
    results = []
    lowered = text.lower()
    for index in ranked:
        category = str(classes[index])
        profile = CATEGORY_PROFILES.get(category, {"skills": []})
        evidence = [skill for skill in profile["skills"] if skill in lowered][:7]
        results.append({
            "category": category,
            "confidence": round(float(probabilities[index] * 100), 1),
            "reason": f"The supervised model found the strongest learned evidence for {category}." + (f" Supporting skills: {', '.join(evidence[:5])}." if evidence else ""),
            "evidence": evidence,
        })
    return results, bundle.get("metrics", {})
