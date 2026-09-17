from fastapi import APIRouter, HTTPException
from app.ml.semantic_classifier import SemanticClassifier

router = APIRouter(prefix="/roles", tags=["Job Roles"])

@router.get("")
def list_roles():
    profiles = SemanticClassifier.get_instance().profiles
    return [
        {
            "id": role_id,
            "name": p["name"],
            "category": p["category"],
            "description": p["description"]
        }
        for role_id, p in profiles.items()
    ]

@router.get("/{role_id}")
def get_role(role_id: str):
    profiles = SemanticClassifier.get_instance().profiles
    profile = profiles.get(role_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Role profile not found.")
    return profile
