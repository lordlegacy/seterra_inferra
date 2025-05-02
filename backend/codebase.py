import os

def aggregate_files_to_txt(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                
                # Skip binary files based on extensions or try reading text only
                try:
                    with open(file_path, 'r', encoding='utf-8') as in_f:
                        content = in_f.read()
                except Exception as e:
                    # If UTF-8 fails, skip binary or unreadable files
                    continue
                
                out_f.write(f"{'='*80}\n")
                out_f.write(f"FILE: {file_path}\n")
                out_f.write(f"{'='*80}\n")
                out_f.write(content + "\n\n")

# Example usage:
aggregate_files_to_txt('it-ticketing-system', 'aggregated_codebase.txt')
