import fitz  # PyMuPDF
import re

# Replace with the path to your PDF file
pdf_path = "book_of_mormon_kat.pdf"
output_file = "book_of_mormon_kat.txt"
# The phrase after which all text should be excluded
cut_phrase = "თემატური სარჩევი მორმონის წიგნში"

# Open the PDF document
doc = fitz.open(pdf_path)

all_text = ""

for page in doc:
    # Get detailed text information as a dictionary
    page_dict = page.get_text("dict")
    for block in page_dict.get("blocks", []):
        # Only process blocks that contain text lines
        if "lines" not in block:
            continue
        for line in block["lines"]:
            line_text = ""
            for span in line["spans"]:
                # Check if the span is italic (using the font name and flags)
                font_name = span.get("font", "").lower()
                flags = span.get("flags", 0)
                if "italic" in font_name or (flags & 2):
                    continue  # Skip italic text
                else:
                    line_text += span.get("text", "")
            # Add the cleaned line if it's not empty
            if line_text.strip():
                all_text += line_text + "\n"
    # Optional: add an extra newline between pages
    all_text += "\n"

# Replace all numbers (one or more digits) with a newline
all_text = re.sub(r'თავი \d+', '\n', all_text)
all_text = re.sub(r'\d+', '\n', all_text)

# Remove everything after the cut phrase (if it exists)
if cut_phrase in all_text:
    all_text = all_text.split(cut_phrase)[0]

# Remove every instance of the page-marker pattern.
# This pattern matches a line with any non-newline characters (the book name),
# followed by a line with a colon, then a line with a dash.
page_marker_pattern = r'(?m)^[^\n]+\s*\n\s*:\s*\n\s*–\s*\n?'
all_text = re.sub(page_marker_pattern, '', all_text)

# The marker phrase before which we want to remove text
marker_phrase = "მორმონი \n, გვ. \n–"


if marker_phrase in all_text:
    marker_index = all_text.index(marker_phrase) + len(marker_phrase)
    all_text = all_text[marker_index:]
else:
    print("Marker phrase not found in the text.")


# Save the resulting text to a file (UTF-8 encoding)
with open(output_file, "w", encoding="utf-8") as f:
    f.write(all_text)

print(f"Extracted text saved to {output_file}")