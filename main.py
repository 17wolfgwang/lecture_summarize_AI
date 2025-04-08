import os
import sys
import argparse

def main():
   parser = argparse.ArgumentParser(description='Lecture Video Text Extraction and Summarization Tool')
   parser.add_argument('video_path', help='Path to the video file to process')
   parser.add_argument('--pdf', help='Path to lecture slides PDF file (optional)')
   parser.add_argument('--output_dir', default='output', help='Output directory (default: output)')
   parser.add_argument('--model_size', default='base', choices=['tiny', 'base', 'small', 'medium', 'large'], 
                       help='Whisper model size (default: base)')
   
   args = parser.parse_args()
   
   # Create output directory
   if not os.path.exists(args.output_dir):
       os.makedirs(args.output_dir)
   
   # Get base filename
   base_name = os.path.splitext(os.path.basename(args.video_path))[0]
   
   # 1. Generate subtitles
   print("1. Generating subtitles...")
   from simple_whisper import transcribe_video
   transcribe_video(args.video_path, args.output_dir, args.model_size)
   
   # 2. Process PDF (if available)
   pdf_text = None
   if args.pdf:
       print("2. Processing PDF slides...")
       from extract_pdf import extract_text_from_pdf
       pdf_text_path = extract_text_from_pdf(args.pdf, args.output_dir)
       
       if pdf_text_path:
           # Load PDF text
           with open(pdf_text_path, 'r', encoding='utf-8') as f:
               pdf_text = f.read()
   
   # 3. Summarize transcript
   print("3. Summarizing lecture content...")
   from summarize_with_claude import summarize_transcript
   segments_file = os.path.join(args.output_dir, f"{base_name}_segments.txt")
   
   # Include PDF text in prompt if available
   if pdf_text:
       # Simple implementation, you can modify summarize_with_claude.py to process PDF content together
       with open(segments_file, 'r', encoding='utf-8') as f:
           segments_text = f.read()
       
       with open(os.path.join(args.output_dir, f"{base_name}_combined.txt"), 'w', encoding='utf-8') as f:
           f.write("=== Lecture Transcript ===\n\n")
           f.write(segments_text)
           f.write("\n\n=== Slide Content ===\n\n")
           f.write(pdf_text)
       
       # Summarize using combined file
       summarize_transcript(os.path.join(args.output_dir, f"{base_name}_combined.txt"))
   else:
       # Summarize using transcript only
       summarize_transcript(segments_file)
   
   print("\nComplete process finished!")
   print(f"Result files are saved in the '{args.output_dir}' directory.")
   print("Please check the original video at the important timestamps identified in the summary.")

if __name__ == "__main__":
   main()