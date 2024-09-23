import os
#LSJ
def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
lsj_pdfs = list_files("../lsj_pdf_downloads")

song_set = set()

for pdf in lsj_pdfs:
    if "C_Instruments" not in pdf:
        continue
    print(
        pdf[4:-18]
    )
    song_set.add(pdf[4:-18])

with open("harvest_lsj.txt", 'w') as f:
    for item in song_set:
        f.write(item + "\n")