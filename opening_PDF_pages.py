import os

indices_files_list = ["SetlistResources/Real_book_v5_indices_cleaned",
                   "SetlistResources/Real_book_v5_vol2_indices_cleaned",
                   "SetlistResources/Real_book_v5_vol3_indices_cleaned"]
indices_files_pdf_fps_C = [
    "SetlistResources/Real-Book-5th-Edition-C.pdf",
    "SetlistResources/Real-Book-Fifth-Edition-Volume-2-C.pdf",
    "SetlistResources/Real-Book-Fifth-Edition-Volume-3-C.pdf"
]
indices_files_pdf_fps_Bb = [
    "SetlistResources/Real-Book-5th-Edition-Bb.pdf",
    "SetlistResources/Real-Book-Fifth-Edition-Volume-2-Bb.pdf",
    "SetlistResources/Real-Book-Fifth-Edition-Volume-3-Bb.pdf"
]
indices_files_pdf_fps_Eb = [
    "SetlistResources/Real-Book-5th-Edition-Bb.pdf",
    "SetlistResources/Real-Book-Fifth-Edition-Volume-2-Eb.pdf",
    None
]

#used to match up the pdf filepath lists with the indices database files
def get_pdf_fp(indices_file_fp, key="C"):
    if key.lower() == "c": pdf_fps = indices_files_pdf_fps_C
    elif key.lower() =="bb": pdf_fps = indices_files_pdf_fps_Bb
    elif key.lower() == "eb": pdf_fps = indices_files_pdf_fps_Eb
    else: raise ValueError
    index = indices_files_list.index(indices_file_fp)
    return pdf_fps[index]

# USED TO OPEN THE PDF IN MACOS PREVIEW
def open_pdf_in_preview(pdf_path):
    if type(pdf_path) != str:
        raise TypeError(f"passed bad pdf path: {pdf_path}")
    # Ensure the file path is properly formatted as a URL for Chrome
    pdf_url = f"{os.path.abspath(pdf_path)}"

    # Command to open the PDF in Chrome
    command = f"open '{pdf_url}'"
    os.system(command)

# USED TO INVOKE AN APPLESCRIPT TO FORCE THE NAVIGATION TO A CERTAIN PAGE
def set_pdf_page(page_number):
    script = f'''
    set pageNumber to {page_number}

    tell application "Preview"
        activate
        tell front document
            tell application "System Events"
                keystroke "g" using {{option down, command down}} -- Go to Page dialog
                delay 0.2
                keystroke (pageNumber as text)
                delay 0.5
                keystroke return
            end tell
        end tell
    end tell
    '''
    os.system(f"osascript -e '{script}'")

# USED TO LOAD INFO FROM THE INDICES FILES
def load_real_book_index_data(files = indices_files_list):
    d = {}
    for f_number, fp in enumerate(files):
        with open(fp,'r') as f:
            for line in f:
                info = line.split("PG#")
                song_name = (" ".join(info[0].split())).lower()
                try:
                    page_number = int(info[1].split()[0])
                except:
                    exit()
                d[song_name]={'page':page_number,
                              'index_file_fp':fp,
                              'c_pdf_fp':get_pdf_fp(fp,"C"),
                              'bb_pdf_fp':get_pdf_fp(fp,"Bb"),
                              'eb_pdf_fp':get_pdf_fp(fp,"Eb")}
    return d

#COMBINES THE ABOVE FUNCTIONS TO OPEN A PDF TO THE CORRECT (HOPEFULLY) PAGE OF A PDF IN THE CORRECT KEY
def open_song_pdf_page(song_name: str, key: str = "C"):
    d = load_real_book_index_data()
    if song_name in d.keys():
        print(f"Song name {song_name} found in data... {d[song_name]}")
    else:
        print(f"Song name '{song_name}' not found in database.")
        return -1

    pdf_fp = d[song_name][key.lower() + "_pdf_fp"]

    if pdf_fp == None:
        raise ValueError(f"Song {song_name} not found in {key}")

    open_pdf_in_preview(pdf_fp)
    set_pdf_page(d[song_name]['page'])

if __name__ == "__main__":
    open_song_pdf_page("got a match ?", "Bb")