import os
import json
from collections import Counter

# We will reuse the function from Phase 2. This is good modular practice.
from pdf_parser import extract_text_blocks

def analyze_structure(blocks):
    """
    Analyzes a list of text blocks to identify the document title and
    headings (H1, H2, H3) based on font size and style.

    Args:
        blocks (list): A list of block dictionaries from extract_text_blocks.

    Returns:
        tuple: A tuple containing:
            - title (str): The identified document title.
            - headings (list): A list of dictionaries for each identified heading.
    """
    if not blocks:
        return None, []

    # --- 1. Find the most common font size (likely the body text) ---
    font_sizes = [b['font_size'] for b in blocks if b['text'].strip()]
    if not font_sizes:
        return None, []
    body_size = Counter(font_sizes).most_common(1)[0][0]

    # --- 2. Identify potential headings and the document title ---
    potential_headings = []
    potential_title_block = None

    for b in blocks:
        # Rule: A block is a potential heading if it's bold and larger than body text.
        if b['font_size'] > body_size and b['is_bold']:
            potential_headings.append(b)
        
        # Rule: The title is often the largest text on the first couple of pages.
        if b['page_num'] <= 2:
            if not potential_title_block or b['font_size'] > potential_title_block['font_size']:
                potential_title_block = b

    title = potential_title_block['text'] if potential_title_block else "No Title Found"

    if not potential_headings:
        return title, []

    # --- 3. Group heading font sizes and rank them to determine H1, H2, H3 ---
    heading_font_sizes = sorted(list(set([h['font_size'] for h in potential_headings])), reverse=True)
    
    # Create a mapping from a font size to a heading level (H1, H2, H3)
    size_to_level = {}
    if len(heading_font_sizes) > 0:
        size_to_level[heading_font_sizes[0]] = "H1"
    if len(heading_font_sizes) > 1:
        size_to_level[heading_font_sizes[1]] = "H2"
    if len(heading_font_sizes) > 2:
        # Assign H3 to all other smaller heading sizes
        for size in heading_font_sizes[2:]:
            size_to_level[size] = "H3"
            
    # --- 4. Final Pass: Create the final list of headings ---
    headings = []
    for h in potential_headings:
        size = h['font_size']
        if size in size_to_level:
            headings.append({
                "level": size_to_level[size],
                "text": h['text'],
                "page": h['page_num']
            })
            
    return title, headings

# --- Example Usage ---
if __name__ == "__main__":
    input_pdf = os.path.join("input", "sample.pdf")

    # Step 1: Run the parser from Phase 2
    print(f"Parsing PDF: {input_pdf}...")
    blocks = extract_text_blocks(input_pdf)
    
    # Step 2: Run the analyzer from Phase 3
    if blocks:
        print("Analyzing document structure...")
        title, headings = analyze_structure(blocks)

        # Step 3: Print the results
        print("\n" + "="*40)
        print("          DOCUMENT STRUCTURE")
        print("="*40)
        print(f"\nTITLE: {title}\n")
        print("--- HEADINGS ---")
        if headings:
            for heading in headings:
                indent = "  " if heading['level'] == 'H2' else "    " if heading['level'] == 'H3' else ""
                print(f"{indent}[{heading['level']}] {heading['text']} (Page {heading['page']})")
        else:
            print("No headings were identified.")
        print("\n" + "="*40)