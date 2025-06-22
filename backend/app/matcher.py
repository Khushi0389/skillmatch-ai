from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_match(resume_text, jd_text):
    emb_resume = model.encode(resume_text, convert_to_tensor=True)
    emb_jd = model.encode(jd_text, convert_to_tensor=True)
    score = util.cos_sim(emb_resume, emb_jd)
    return round(float(score[0][0]) * 100, 2)
