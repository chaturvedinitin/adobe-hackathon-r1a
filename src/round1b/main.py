import os
import json
import datetime
from content_prepper import prepare_document_content
from relevance_analyzer import find_relevant_sections

def generate_final_json(persona, job, sections, docs, output_path):
    sub_sections = [{
        "document": s['source_doc'],
        "page_number": s['page_num'],
        "refined_text": s['content'][:300] + "..."
    } for s in sections[:5]] # Analyze top 5 sections
    sub_sections = [{
        "document": s['source_doc'],
        "page_number": s['page_num'],
        "refined_text": s['content'][:300] + "..."
    } for s in sections[:5]]

    output_data = {
        "metadata": {
            "input_documents": docs,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.datetime.now().isoformat()
        },
        "extracted_section": [{
            "document": s['source_doc'],
            "page_number": s['page_num'],
            "section_title": s['heading_text'],
            "importance_rank": i + 1
        } for i, s in enumerate(sections)],
        "sub_section_analysis": sub_sections
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    input_dir = "/app/input"
    output_dir = "/app/output"

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    pdf_paths = [os.path.join(input_dir, f) for f in pdf_files]

    try:
        with open(os.path.join(input_dir, 'persona.txt'), 'r') as f:
            persona = f.read().strip()
    except FileNotFoundError:
        persona = "Investment Analyst"

    try:
        with open(os.path.join(input_dir, 'job.txt'), 'r') as f:
            job = f.read().strip()
    except FileNotFoundError:
        job = "Analyze revenue trends"

    print("Step 1: Preparing content from all documents...")
    all_sections = prepare_document_content(pdf_paths)
    print("Step 2: Finding relevant sections...")
    relevant_sections = find_relevant_sections(all_sections, persona, job)
    output_path = os.path.join(output_dir, "challenge1b_output.json")
    print(f"Step 3: Generating final output at {output_path}...")
    generate_final_json(persona, job, relevant_sections, pdf_files, output_path)
    print("\n✅ Round 1B processing complete!")