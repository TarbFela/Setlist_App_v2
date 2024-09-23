from string import *
from re import sub
import PyPDF2
f = open("Real_Book_6_Indices.csv","r")
f_str = f.read()
f_lines = f_str.split("\n")
f.close()

songs_names = [
    sub('"', "", ",".join(line.split(",")[:-2]))
     for line in f_lines
]
songs_pages = [
    int(line.split(",")[-2])
    for line in f_lines
]

songs_info = [ pair for pair in zip(songs_names, songs_pages)]
for line in songs_info: print(line)




def split_pdf(input_pdf, output_folder):
    # Open the input PDF file
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        # Iterate through all pages and save each as a separate PDF
        #i = 0
        for title, page in songs_info:
            #i += 1
            #if i>10: break

            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[page - 2])

            # Create the output PDF file name
            output_pdf = f"{output_folder}/{title}_RB6_Bb.pdf"

            # Write the page to a new PDF file
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            print(f"Saved {output_pdf}")

# Usage
input_pdf = 'Eb_Real_Book_Harvesting.pdf'    # Path to your input PDF
output_folder = 'individual_pages_folder_Eb'  # Folder where you want to save the individual PDFs
split_pdf(input_pdf, output_folder)