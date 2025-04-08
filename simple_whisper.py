import os
import whisper

def transcribe_video(video_path, output_dir="output", model_size="base"):
   # Create output directory
   if not os.path.exists(output_dir):
       os.makedirs(output_dir)
   
   # Extract filename
   base_name = os.path.splitext(os.path.basename(video_path))[0]
   output_txt = os.path.join(output_dir, f"{base_name}_transcript.txt")
   
   # Load Whisper model
   print(f"Loading Whisper {model_size} model...")
   model = whisper.load_model(model_size)
   
   # Perform speech recognition
   print(f"Converting '{video_path}' file...")
   result = model.transcribe(video_path, word_timestamps=True)
   
   # Save results
   with open(output_txt, 'w', encoding='utf-8') as f:
       f.write(result["text"])
   
   print(f"Conversion complete. Text saved to '{output_txt}'.")
   
   # Also save in segment format with timestamp information
   output_segments = os.path.join(output_dir, f"{base_name}_segments.txt")
   with open(output_segments, 'w', encoding='utf-8') as f:
       for segment in result["segments"]:
           start_time = format_time(segment["start"])
           end_time = format_time(segment["end"])
           text = segment["text"].strip()
           f.write(f"[{start_time} - {end_time}] {text}\n")
   
   print(f"Segment information saved to '{output_segments}'.")
   return result

def format_time(seconds):
   """Convert seconds to HH:MM:SS format"""
   hours = int(seconds // 3600)
   minutes = int((seconds % 3600) // 60)
   seconds = int(seconds % 60)
   return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

if __name__ == "__main__":
   import sys
   if len(sys.argv) < 2:
       print("Usage: python simple_whisper.py <video_file_path> [output_dir] [model_size]")
       sys.exit(1)
   
   video_path = sys.argv[1]
   output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
   model_size = sys.argv[3] if len(sys.argv) > 3 else "base"
   
   transcribe_video(video_path, output_dir, model_size)