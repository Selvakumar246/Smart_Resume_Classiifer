import json
import re
from pathlib import Path
from functools import lru_cache

# Path helpers
TAXONOMY_DIR = Path(__file__).parent / "taxonomy"

@lru_cache(maxsize=1)
def load_taxonomy():
    skills_path = TAXONOMY_DIR / "skills.json"
    aliases_path = TAXONOMY_DIR / "aliases.json"

    # Default fallback mapping in case files don't load or exist during testing
    skills = {}
    aliases = {}

    if skills_path.exists():
        with open(skills_path, "r", encoding="utf-8") as f:
            skills = json.load(f)
    if aliases_path.exists():
        with open(aliases_path, "r", encoding="utf-8") as f:
            aliases = json.load(f)

    # Invert aliases mapping: lowercase_alias -> canonical_name
    alias_to_canonical = {}
    for canonical, alias_list in aliases.items():
        for alias in alias_list:
            alias_to_canonical[alias.lower()] = canonical
        # Ensure canonical name itself matches
        alias_to_canonical[canonical.lower()] = canonical

    # For skills that have no aliases in aliases.json, add their canonical name to the alias mapping
    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower not in alias_to_canonical:
            alias_to_canonical[skill_lower] = skill

    return skills, alias_to_canonical

def extract_skills_from_text(text: str) -> list[dict]:
    """
    Extracts canonical skills from text using boundary-safe regex matching for technical terms.
    Returns a list of dicts: {'canonical_name': str, 'category': str, 'mentions': int}
    """
    skills_categories, alias_map = load_taxonomy()
    
    # We want to match all aliases. Sort alias keys by length descending to match longest phrases first
    sorted_aliases = sorted(alias_map.keys(), key=len, reverse=True)
    
    mentions_count = {}
    
    for alias in sorted_aliases:
        canonical_name = alias_map[alias]
        
        # Safe technical boundary check
        # Must not be preceded or followed by alphanumeric, '+', '#', or '.'
        pattern = rf"(?<![a-zA-Z0-9#+.])({re.escape(alias)})(?![a-zA-Z0-9#+.])"
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        
        if matches:
            mentions_count[canonical_name] = mentions_count.get(canonical_name, 0) + len(matches)
            # Remove matched occurrences from temporary search text so shorter sub-phrases don't double-match
            # e.g., if we match "Tailwind CSS", we temporarily substitute it so "CSS" doesn't match the same text.
            # But we must preserve position offsets or character count so boundaries remain valid. We replace with spaces.
            def replacer(match):
                return " " * len(match.group(0))
            text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)

    results = []
    for skill_name, count in mentions_count.items():
        category = skills_categories.get(skill_name, "Other")
        results.append({
            "canonical_name": skill_name,
            "category": category,
            "mentions": count
        })
        
    return sorted(results, key=lambda x: x["mentions"], reverse=True)
