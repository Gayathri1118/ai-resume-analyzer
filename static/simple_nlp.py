import re

def tokenize(text):
    text = text.lower()
    return re.findall(r"[a-zA-Z+#.]+", text)

def extract_keywords(text, keywords):
    tokens = tokenize(text)
    found = set()

    for skill in keywords:
        skill_tokens = skill.lower().split()
        if len(skill_tokens) == 1:
            if skill_tokens[0] in tokens:
                found.add(skill)
        else:
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"
            if re.search(pattern, text.lower()):
                found.add(skill)

    return found
