import os
from collections import Counter
from round1a.pdf_parser import extract_text_blocks

def prepare_document_content(pdf_paths):
    all_sections = []
    
    for pdf_path in pdf_paths:
        print(f"Processing document: {pdf_path}...")
        blocks = extract_text_blocks(pdf_path)
        if not blocks:
            continue

        font_sizes = [b['font_size'] for b in blocks if b['text'].strip()]
        if not font_sizes:
            continue
        body_size = Counter(font_sizes).most_common(1)[0][0]

        document_sections = []
        current_section = None

        for b in blocks:
            text = b['text'].strip()
            if not text:
                continue

            is_heading = b['is_bold'] and b['font_size'] > body_size

            if is_heading:
                if current_section:
                    document_sections.append(current_section)
                current_section = {
                    "source_doc": os.path.basename(pdf_path),
                    "heading_text": text,
                    "page_num": b['page_num'],
                    "content": text + " " 
                }
            elif current_section:
                current_section["content"] += text + " "
        
        if current_section:
            document_sections.append(current_section)

        all_sections.extend(document_sections)
        print(f"  Found {len(document_sections)} sections.")

    return all_sections

if __name__ == "__main__":
    input_dir = "input"
    pdf_files_to_process = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]

    if not pdf_files_to_process:
        print(f"No PDF files found in '{input_dir}'. Please add some PDFs to test.")
    else:
        sections = prepare_document_content(pdf_files_to_process)

        if sections:
            print(f"\n✅ Total sections extracted from all documents: {len(sections)}")
            
            for section in sections[:2]:
                section['content'] = section['content'][:200] + "..." if len(section['content']) > 200 else section['content']
                print(section)
                print("-" * 20)
