import os
import re
import json
from collections import Counter, defaultdict
from datetime import datetime

# Heuristic patterns for attribute extraction
AGE_PATTERNS = [
    (re.compile(r"\bI'?m (\d{2})\b"), "direct_age"),
    (re.compile(r"\b(\d{2}) years? old\b"), "direct_age"),
    (re.compile(r"\bwhen I was (\d{2})\b"), "past_age"),
]
OCCUPATION_PATTERNS = [
    (re.compile(r"\bI work as a[n]? ([\w\s]+)\b", re.I), "direct"),
    (re.compile(r"\bmy job is ([\w\s]+)\b", re.I), "direct"),
    (re.compile(r"\bI am a[n]? ([\w\s]+)\b", re.I), "direct"),
]
RELATIONSHIP_PATTERNS = [
    (re.compile(r"\bmy (wife|husband|boyfriend|girlfriend|partner)\b", re.I), "partner"),
    (re.compile(r"\bI'?m (single|married|divorced|engaged)\b", re.I), "status"),
]
LOCATION_PATTERNS = [
    (re.compile(r"\bI live in ([\w\s,]+)\b", re.I), "direct"),
    (re.compile(r"\bfrom ([\w\s,]+)\b", re.I), "direct"),
]
MBTI_TRAITS = {
    "Introvert": [r"\bprefer (quiet|alone|solitude)\b", r"\bnot a people person\b"],
    "Extrovert": [r"\blove (parties|meeting people|socializing)\b", r"\bpeople person\b"],
    "Thinking": [r"\blogic\b", r"\brational\b"],
    "Feeling": [r"\bfeelings?\b", r"\bemotional\b"],
    "Judging": [r"\borganized\b", r"\bplan\b"],
    "Perceiving": [r"\bspontaneous\b", r"\bgo with the flow\b"],
}
MOTIVATION_PATTERNS = {
    "Speed": [r"\bfast\b", r"\bquick\b"],
    "Comfort": [r"\bcomfortable\b", r"\bcozy\b"],
    "Wellness": [r"\bhealthy\b", r"\bwellness\b"],
}
FRUSTRATION_PATTERNS = [
    re.compile(r"\bfrustrat(ed|ing)\b", re.I),
    re.compile(r"\bannoy(ed|ing)\b", re.I),
    re.compile(r"\bcan'?t stand\b", re.I),
]
ARCHETYPES = {
    "Creator": [r"\bmake\b", r"\bcreate\b", r"\bbuilt\b"],
    "Analyst": [r"\banalyz(e|ed|ing)\b", r"\bdata\b", r"\bresearch\b"],
    "Minimalist": [r"\bminimal(ist|ism)\b", r"\bsimple\b"],
    "Early Adopter": [r"\bnew\b", r"\bearly\b", r"\bfirst to try\b"],
}

def load_reddit_data(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_attribute(patterns, text):
    for pat, label in patterns:
        match = pat.search(text)
        if match:
            return match.group(1), match.group(0)
    return None, None

def extract_mbti(text):
    traits = []
    for trait, pats in MBTI_TRAITS.items():
        for pat in pats:
            if re.search(pat, text, re.I):
                traits.append(trait)
                break
    return traits

def extract_motivations(text):
    motivations = []
    for motive, pats in MOTIVATION_PATTERNS.items():
        for pat in pats:
            if re.search(pat, text, re.I):
                motivations.append(motive)
                break
    return motivations

def extract_archetypes(text):
    found = []
    for arch, pats in ARCHETYPES.items():
        for pat in pats:
            if re.search(pat, text, re.I):
                found.append(arch)
                break
    return found

def extract_frustrations(text):
    for pat in FRUSTRATION_PATTERNS:
        if pat.search(text):
            return True
    return False

def analyze_usage(posts):
    times = []
    subreddits = Counter()
    for post in posts:
        if "created_utc" in post:
            times.append(datetime.utcfromtimestamp(post["created_utc"]).hour)
        if "subreddit" in post:
            subreddits[post["subreddit"]] += 1
    usage = {}
    if times:
        usage["active_hours"] = f"{min(times)}:00 - {max(times)}:00 UTC"
    if subreddits:
        usage["top_subreddits"] = subreddits.most_common(3)
    return usage

def persona_from_reddit(json_path, output_path):
    data = load_reddit_data(json_path)

    
    if isinstance(data, list):
        posts = data
    else:
        posts = data.get("comments", []) + data.get("posts", [])

    persona = defaultdict(list)
    evidence = defaultdict(list)

    for post in posts:
        text = post.get("body") or post.get("selftext") or post.get("title") or ""
        age, age_ev = extract_attribute(AGE_PATTERNS, text)
        if age:
            persona["Estimated Age"].append(age)
            evidence["Estimated Age"].append(age_ev)
        occ, occ_ev = extract_attribute(OCCUPATION_PATTERNS, text)
        if occ:
            persona["Occupation"].append(occ)
            evidence["Occupation"].append(occ_ev)
        rel, rel_ev = extract_attribute(RELATIONSHIP_PATTERNS, text)
        if rel:
            persona["Relationship Status"].append(rel)
            evidence["Relationship Status"].append(rel_ev)
        loc, loc_ev = extract_attribute(LOCATION_PATTERNS, text)
        if loc:
            persona["Location"].append(loc)
            evidence["Location"].append(loc_ev)
        for trait in extract_mbti(text):
            persona["MBTI Traits"].append(trait)
            evidence["MBTI Traits"].append(text)
        for motive in extract_motivations(text):
            persona["Motivational Drivers"].append(motive)
            evidence["Motivational Drivers"].append(text)
        for arch in extract_archetypes(text):
            persona["Consumer Archetypes"].append(arch)
            evidence["Consumer Archetypes"].append(text)
        if extract_frustrations(text):
            persona["Expressions of Frustration"].append("Yes")
            evidence["Expressions of Frustration"].append(text)

    usage = analyze_usage(posts)
    if usage:
        persona["Reddit Usage Habits"].append(str(usage))
        evidence["Reddit Usage Habits"].append("Based on post timestamps and subreddits.")

    for k in persona:
        persona[k] = list(set(persona[k]))
        evidence[k] = list(set(evidence[k]))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Reddit User Persona Report\n")
        f.write("="*30 + "\n\n")
        for attr in [
            "Estimated Age", "Occupation", "Relationship Status", "Location",
            "MBTI Traits", "Motivational Drivers", "Consumer Archetypes",
            "Reddit Usage Habits", "Expressions of Frustration"
        ]:
            if persona[attr]:
                f.write(f"{attr}:\n")
                for i, val in enumerate(persona[attr]):
                    f.write(f"  - {val}\n")
                    if i < len(evidence[attr]):
                        f.write(f"    Evidence: \"{evidence[attr][i]}\"\n")
                f.write("\n")

if __name__ == "__main__":
    input_json = "data/Hungry-Move-6603_raw.json"
    output_txt = "output/hungry_move_persona.txt"
    persona_from_reddit(input_json, output_txt)
