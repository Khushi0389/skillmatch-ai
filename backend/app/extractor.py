import spacy

nlp = spacy.load("en_core_web_sm")
known_skills = {
    "python", "java", "sql", "spring boot", "docker", "html", "css", "tensorflow",
    "react", "node.js", "fastapi", "kubernetes", "git", "aws"
}

def extract_skills(text):
    doc = nlp(text.lower())
    tokens = {token.text for token in doc if not token.is_stop and not token.is_punct}
    return list(known_skills.intersection(tokens))
