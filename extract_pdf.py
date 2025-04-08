import os
import sys
from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(pdf_path, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Extract File
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_txt = os.path.join(output_dir, f"{base_name}_slides.txt")
    
    print(f"PDF '{pdf_path}' handling,,,")
    
    try:
        # PDF to Image
        pages = convert_from_path(pdf_path, 300)
        
        with open(output_txt, 'w', encoding='utf-8') as f:
            for i, page in enumerate(pages):
                # Text extract with OCR
                text = pytesseract.image_to_string(page, lang='kor+eng')
                f.write(f"===== 슬라이드 {i+1} =====\n")
                f.write(text)
                f.write("\n\n")
        
        print(f"PDF text saved in '{output_txt}'")
        return output_txt
    
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("How to use: python extract_pdf.py <pdf_file_path> [output_dir]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
    
    extract_text_from_pdf(pdf_path, output_dir)