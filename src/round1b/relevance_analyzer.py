import os
from sentence_transformers import SentenceTransformer, util
from round1b.content_prepper import prepare_document_content

model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'all-MiniLM-L6-v2')
model = SentenceTransformer(model_path)

def find_relevant_sections(sections, persona, job_to_be_done):
    if not sections:
        return []

    query = f"Persona: {persona}. Task: {job_to_be_done}"
    query_embedding = model.encode(query, convert_to_tensor=True)

    section_contents = [s['content'] for s in sections]
    section_embeddings = model.encode(section_contents, convert_to_tensor=True)

    cosine_scores = util.cos_sim(query_embedding, section_embeddings)

    for i in range(len(sections)):
        sections[i]['relevance_score'] = cosine_scores[0][i].item()
    
    sorted_sections = sorted(sections, key=lambda x: x['relevance_score'], reverse=True)
    
    return sorted_sections

if __name__ == "__main__":
    persona = "Investment Analyst"
    job = "Analyze revenue trends, R&D investments, and market positioning strategies"

    input_dir = "input"
    pdf_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print("No PDFs found in 'input' directory.")
    else:
        all_sections = prepare_document_content(pdf_files)

        relevant_sections = find_relevant_sections(all_sections, persona, job)

        print("\n" + "="*50)
        print("      TOP 5 MOST RELEVANT SECTIONS")
        print("="*50)
        print(f"QUERY: As an {persona}, I need to '{job}'\n")

        for i, section in enumerate(relevant_sections[:5]):
            print(f"RANK {i+1} | SCORE: {section['relevance_score']:.4f}")
            print(f"  SOURCE: {section['source_doc']} (Page {section['page_num']})")
            print(f"  HEADING: {section['heading_text']}")
            print("-" * 50)