import os
from pdf_parser import extract_text_blocks
from structure_analyzer import analyze_structure
import json

def generate_json_output(title, headings, output_path):
    """Formats the data and writes it to a JSON file."""
    output_data = {
        "title": title,
        "outline": headings
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # These paths are where Docker will mount the volumes [cite: 67]
    input_dir = "/app/input"
    output_dir = "/app/output"

    print("Starting solution...")
    
    if not os.path.exists(input_dir):
        print(f"Input directory not found: {input_dir}")
        exit()
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process every PDF file in the input directory [cite: 69]
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            input_pdf_path = os.path.join(input_dir, filename)
            output_json_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".json")
            
            print(f"Processing {input_pdf_path}...")

            # Phase 2: Parse the PDF
            blocks = extract_text_blocks(input_pdf_path)
            
            if blocks:
                # Phase 3: Analyze the structure
                title, headings = analyze_structure(blocks)
                
                # Final Step: Generate the required JSON output [cite: 43]
                generate_json_output(title, headings, output_json_path)
                print(f"Successfully generated {output_json_path}")
            else:
                print(f"Could not extract any blocks from {input_pdf_path}.")
                
    print("Processing complete.")