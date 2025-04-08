import os
import json
import sys
from anthropic import Anthropic

def summarize_transcript(transcript_file, api_key=None):
   if api_key is None:
       api_key = os.environ.get("ANTHROPIC_API_KEY")
       if not api_key:
           print("ANTHROPIC_API_KEY environment variable is not set.")
           api_key = input("Enter your Anthropic API key: ")
   
   # Load transcript
   with open(transcript_file, 'r', encoding='utf-8') as f:
       transcript_text = f.read()
   
   # Create Claude API client
   anthropic = Anthropic(api_key=api_key)
   
   # Configure prompt
   system_prompt = """You are an AI assistant that summarizes educational lectures. 
Please analyze the provided lecture transcript and create a summary of the key content.
Follow this format for your summary:
1. Include relevant timestamps in [start time - end time] format for each summary point
2. Include important concepts, definitions, and examples
3. Select key points to summarize the entire lecture in a 1-2 minute format

At the end, please provide a list of the most important timestamps in this format:
===Important Timestamps===
[00:05:30 - 00:06:45] Core concept 1 explanation
[00:12:20 - 00:13:10] Important example
[00:27:15 - 00:28:30] Conclusion
"""
   
   print("Generating summary through Claude API...")
   
   # Request to Claude
   response = anthropic.messages.create(
       model="claude-3-5-sonnet-20240620",
       system=system_prompt,
       max_tokens=2000,
       messages=[
           {"role": "user", "content": f"The following is a lecture transcript:\n\n{transcript_text}"}
       ]
   )
   
   # Extract summary from response
   summary_text = response.content[0].text
   
   # Create output file path
   output_dir = os.path.dirname(transcript_file)
   base_name = os.path.splitext(os.path.basename(transcript_file))[0].replace("_transcript", "").replace("_segments", "")
   output_summary = os.path.join(output_dir, f"{base_name}_summary.txt")
   
   # Save summary
   with open(output_summary, 'w', encoding='utf-8') as f:
       f.write(summary_text)
   
   print(f"Summary saved to '{output_summary}'.")
   
   # Extract timestamps
   import re
   timestamps = []
   timestamp_section = False
   
   for line in summary_text.split('\n'):
       if "===Important Timestamps===" in line:
           timestamp_section = True
           continue
       
       if timestamp_section:
           # Find timestamps in [00:05:30 - 00:06:45] format
           match = re.search(r'\[(\d{2}:\d{2}:\d{2}) - (\d{2}:\d{2}:\d{2})\](.*)', line)
           if match:
               start_time, end_time, description = match.groups()
               timestamps.append({
                   'start_time': start_time,
                   'end_time': end_time,
                   'description': description.strip()
               })
   
   # Save timestamp information
   output_timestamps = os.path.join(output_dir, f"{base_name}_timestamps.json")
   with open(output_timestamps, 'w', encoding='utf-8') as f:
       json.dump(timestamps, f, ensure_ascii=False, indent=2)
   
   print(f"Important timestamps saved to '{output_timestamps}'.")
   return summary_text, timestamps

if __name__ == "__main__":
   if len(sys.argv) < 2:
       print("Usage: python summarize_with_claude.py <transcript_file>")
       sys.exit(1)
   
   transcript_file = sys.argv[1]
   summarize_transcript(transcript_file)