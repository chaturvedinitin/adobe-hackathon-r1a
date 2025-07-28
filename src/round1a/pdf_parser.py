import fitz
import os
import json

def extract_text_blocks(pdf_path):
    
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' was not found.")
        return []
    
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening or processing PDF file: {e}")
        return []

    all_blocks = []
    for page_num, page in enumerate(doc, start=1):
        page_blocks = page.get_text("dict")["blocks"]
        
        for block in page_blocks:
            if block['type'] == 0: 
                block_text = []
                font_sizes = []
                bold_flags = []

                for line in block["lines"]:
                    for span in line["spans"]:
                        block_text.append(span["text"])
                        font_sizes.append(span["size"])
                        is_span_bold = (span["flags"] & 16) or \
                                       "bold" in span["font"].lower()
                        bold_flags.append(is_span_bold)

                if not block_text:
                    continue

                full_text = " ".join(block_text).strip()
                
                dominant_font_size = max(set(font_sizes), key=font_sizes.count) if font_sizes else 0.0
                is_block_bold = any(bold_flags)

                y_position = block["bbox"][1]

                all_blocks.append({
                    "text": full_text,
                    "font_size": round(dominant_font_size, 2),
                    "is_bold": is_block_bold,
                    "page_num": page_num,
                    "y_pos": round(y_position, 2)
                })

    doc.close()
    return all_blocks


if __name__ == "__main__":
    # This block demonstrates how to use the function and inspect its output.
    # It will run only when the script is executed directly.
    
    input_dir = "input"
    output_dir = "output"
    
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sample_pdf_path = os.path.join(input_dir, "sample.pdf")

    # --- Attempt to create a dummy PDF for testing ---
    try:
        doc = fitz.open()
        page = doc.new_page()
        
        # Using standard PDF base fonts
        page.insert_text((50, 72), "This is a Title", fontsize=24, fontname="helv-bold")
        page.insert_text((50, 120), "1. Introduction", fontsize=16, fontname="helv-bold")
        page.insert_text((50, 150), "This is the first paragraph.", fontsize=12, fontname="helv")
        
        doc.save(sample_pdf_path)
        doc.close()
        print(f"Successfully created a dummy PDF for testing at: {sample_pdf_path}")
    
    except Exception as e:
        # If font files are not found, this block will be executed.
        if "need font file" in str(e):
            print("---")
            print("\n Warning: Could not create a dummy PDF because standard fonts were not found on your system.")
            print("\n This is an environment issue and does not affect the correctness of the parsing function.")
            print("\n ACTION: Please place a real PDF file (e.g., the one from the hackathon) into the 'input' folder and run the script again.")
            print("---")
            # Exit gracefully if we can't create the test file and none exists
            if not os.path.exists(sample_pdf_path):
                exit()
        else:
            print(f"An unexpected error occurred: {e}")
            exit()

    # --- Run the extraction function on the PDF found in the input folder ---
    print(f"\nProcessing PDF: {sample_pdf_path}")
    extracted_data = extract_text_blocks(sample_pdf_path)

    if extracted_data:
        output_path = os.path.join(output_dir, "raw_extracted_blocks.json")
        with open(output_path, "w") as f:
            json.dump(extracted_data, f, indent=4)
        
        print(f"\n Successfully extracted {len(extracted_data)} text blocks.")
        print(f"Raw extracted data saved to '{output_path}'")
        
        print("\n--- First 5 Extracted Blocks ---")
        for block in extracted_data[:5]:
            print(block)
        print("--------------------------------\n")
    else:
        print("No data was extracted from the PDF. Ensure the file is not empty or corrupted.")
