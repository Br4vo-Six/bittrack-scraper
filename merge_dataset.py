
from dotenv import load_dotenv
import os
import json

def merge(directory, output_file):
    merged_data = []

    # Iterate over all files in the directory
    i = 0
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        merged_data.extend(data)
                    else:
                        merged_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {filename}: {e}")
            print(f"File done: {i}")
            os.system( 'cls' )
            i+=1

    # Write the merged data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    print(f"All JSON files have been merged into {output_file}")

if __name__ == "__main__":
    load_dotenv()
    file_path = os.path.join(os.getenv('OUTPUT_DIR'), "elliptic++_txs.json")
    merge(os.getenv('OUTPUT_DIR'), file_path)