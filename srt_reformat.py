import os
import chardet

def get_latest_file(directory):
    txt_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt') and os.path.isfile(os.path.join(directory, f))]
    txt_files = sorted(txt_files, key=lambda x: os.path.getctime(x), reverse=True)
    return txt_files[0] if txt_files else None

def clean_text(input_file):
    with open(input_file, 'rb') as f:
        raw_data = f.read()
        detected_encoding = chardet.detect(raw_data)['encoding']

    if detected_encoding:
        with open(input_file, 'r', encoding=detected_encoding, errors='replace') as f:
            subs = f.readlines()

        cleaned_text = ""
        for i, sub in enumerate(subs):
            sub = sub.strip()
            # Merge with the previous line if the first word starts with a lowercase letter
            if i > 0 and sub and sub[0].islower():
                cleaned_text = cleaned_text.rstrip() + ' ' + sub
            else:
                cleaned_text += sub.replace('\n', ' ') + ' '
                if i % 10 == 0:  # Add a line break every 10 subtitles for readability
                    cleaned_text += '\n\n'

        # Set the output file name based on the input file name
        output_file = os.path.splitext(input_file)[0] + '_formatted.txt'
        with open(output_file, 'w', encoding=detected_encoding, errors='replace') as f:
            f.write(cleaned_text)
        print("Formatted text written to:", output_file)
    else:
        print("Failed to detect the encoding of the file:", input_file)

# Provide the directory path where your .txt files are located
downloads_dir = 'D:\\Downloads'

# Get the latest .txt file in the specified directory
latest_file = get_latest_file(downloads_dir)

if latest_file:
    # Clean the text in the latest file and write the output to a file with the same name followed by '_formatted'
    clean_text(latest_file)
else:
    print("No .txt files found in the specified directory.")
