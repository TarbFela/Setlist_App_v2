import os
import string
from difflib import SequenceMatcher
from scratch_string_comp import get_file_paths, fps_searchable, name_cleanup, pdf_fp_cleanup
from opening_PDF_pages import *

pathprefix = ""

Genres = []
try:
    with open("SetlistResources/genres_library.txt", 'r') as f:
        Genres = [ line[:-1] for line in f]
    print(Genres)
except FileNotFoundError:
    cwd = os.getcwd()
    pathprefix = cwd + "/Desktop/Setlist_App_v2/"
    with open(pathprefix+"SetlistResources/genres_library.txt", 'r') as f:
        Genres = [line[:-1] for line in f]
    print(Genres)


#sheet music should work like this:
# You have a song. It is a song.
# Let's reorganize our whole sheet music organization
# We have real books
# We have effendi
# We have LSJ chord charts
class SheetMusic:
    def __init__(self, *argv):
        if type(argv[0]) == str: #if it's just a filepath to a pdf
            self.open_method = self.open_pdf
            self.filepath = argv[0]
        elif type(argv[0]) == dict: #if it's a page of a pdf
            self.open_method = self.open_pdf_to_page
            self.page = None
    def open(self):
        self.open_method()
    def open_pdf(self):
        print(f"Opening {self.filepath}...")
        os.system(f'open "{self.filepath}"')

    def open_pdf_to_page(self):
        print("B")








class Song:
    def __init__(self, name_string_input, get_pdfs = False):
        name = name_cleanup(name_string_input)
        #ADD ALTERNATE NAME SUPPORT (parenthitcals)

        self.name = name
        self.tags = {
            "isLearned": False,
            "genres": set(),
            "difficulty": None,
            "last_played": None,
        }
        if get_pdfs: self.find_pdfs()
        else: self.pdfs = []
        self.recording_links = []



    def find_pdfs(
            self, sim_thresh = 0.6, mode = "replace", recursive = True, verbose = False,
    ):
        fps = get_file_paths("SetlistResources/")
        fps_weights = [
            SequenceMatcher(
                None, self.name, pdf_fp_cleanup(fp)
            ).ratio() for fp in fps
        ]
        match_fps = []
        for fp, sim in zip(fps, fps_weights):
            if sim > sim_thresh:
                match_fps.append(fp)
                if verbose: print(f"{self.name} | {round(1000*sim)/10} | {pdf_fp_cleanup(fp)}")
        if len(match_fps) == 0:
            #print("\t\t\tNONE FOUND")
            self.find_pdfs(sim_thresh=sim_thresh*0.8, mode=mode, recursive=True)
        if mode == "replace":
            self.pdfs = match_fps
            #for p in self.pdfs: print(p)
        elif mode == "append": self.pdfs += match_fps

        return match_fps


    def update_isLearned(self, learned : bool = True):
        self.tags["isLearned"] = learned

    def add_genres(self, genres):
        if type(genres) is str:
            genres = [genres]
        for genre in genres:
            if genre not in Genres: raise ValueError("provided genre was not in library")
            self.tags["genres"].add( genre )
    def remove_genres(self, genres):
        if type(genres) is str:
            genres = [genres]
        for genre in genres:
            if genre not in Genres: raise ValueError("provided genre was not in library")
            try:
                self.tags["genres"].remove( genre )
            except KeyError:
                print(f"{genre} was not found in song genres")
    @property
    def genres(self):
        return self.tags["genres"]

    def __str__(self):
        txt = ""
        #header
        header = "Song: " + self.name
        txt += header + "\n"
        #tags
        for key, value in zip(self.tags.keys(), self.tags.values()):
            if key == 'genres':
                txt += f'\t{key}: '
                for genre in value: txt += f'{genre}, '
                txt += "\n"
            else:
                txt += f'\t{key}: {value}\n'
        #pdfs
        txt += f'\tPDFs: '
        for pdf in self.pdfs:
            txt += f'{pdf}, '#f'{pdf.filepath}, '
        txt += "\n"
        #recording links
        txt += "\tRecordings: "
        for hyperlink in self.recording_links:
            txt += f'{hyperlink}, '
        txt += "\n"
        return txt
    def open_pdf(self, pdf_index = 0):
        os.system(f'open "{self.pdfs[pdf_index]}"')





class SongLibrary:
    def __init__(self, name = "SONG LIBRARY", songs = []):
        self.name = name
        self.songs = songs
    def save_to_file(self):
        with open(pathprefix+"SetlistResources/" + self.name + ".txt", 'w') as f:
            header = self.name
            f.write(header + "\n")
            for song in self.songs:
                f.write( str(song) )
    def __iter__(self, i):
        return self.songs[i]
    def __add__(self, other): #allows adding an arbitrary n of songs to lib w/ addition
        if type(other) != list:
           other = [other]
        for item in other:
            if type(item) != Song: raise TypeError ("could not add non-song to library")
            self.songs.append(item)
        return self
    def newsong(self, song_string):
        self += Song(
            song_string
        )

    def search_library(self, search_term, max_n_results = 1): #zero for all results possible
        song_names = [song.name for song in self.songs]
        weights = [
            SequenceMatcher(
                None, name, search_term
            ).ratio() for name in song_names
        ]
        if max_n_results == 1:
            best_result_index = weights.index(max(weights))
            return self.songs[best_result_index]
        else:
            paired_list = [[w, s] for w, s in zip(weights, self.songs)]
            paired_list = reversed( sorted(paired_list,key=lambda x: x[0]))
            #for line in paired_list: print(line[0],line[1].name)
            #sorted song by weight...
            results = [s for (w, s) in paired_list]
            if max_n_results == 0 or max_n_results > len(self.songs):
                return results
            else:
                return results[:max_n_results + 1]




song_library = SongLibrary()

def load_from_file(path = pathprefix+"SetlistResources/SONG LIBRARY.txt"):
    SL = SongLibrary()
    newsong = None
    with (open(path, 'r') as f):
        lines = [line.replace("\n","") for line in f]
        for counter, line in enumerate(lines):
            #print(line)
            if counter == 0:
                SL.name = line
                continue
            if line[0:5] == "Song:":
                if newsong != None: SL.songs.append(newsong)
                newsong = Song(
                    name_string_input=line.replace(
                        "Song: ",""
                    ).replace(
                        "\n",""
                    )
                )
            if "PDFs:" in line:
                line_list = line.replace("\tPDFs: ","")
                line_list = line_list.split(", ")
                if line_list[-1] == '': del line_list[-1]
                #print(line_list)
                newsong.pdfs = line_list
                continue
            if "Recordings:" in line:
                line_list = line.replace("\tRecordings: ","")
                line_list = line_list.split(", ")
                if line_list[-1] == '': del line_list[-1]
                #print(line_list)
                newsong.recording_links = line_list
                continue
            if "genres:" in line:
                line_list = line.replace("\tgenres: ", "")
                line_list = line_list.split(", ")
                if line_list[-1] == '': del line_list[-1]
                line_set = set(line_list)
                #print(line_set)
                newsong.tags["genres"] = line_set
                continue
            if line[0] == "\t": #diff and islearned
                l_key, l_val = line.replace(
                    "\t",""
                ).replace(
                    " ",""
                ).split(":")
                #print(l_key)
                #print(l_val)
                newsong.tags[l_key] = l_val

        SL.songs.append(newsong)
        return SL


if __name__ == "__main__":
    sm = SheetMusic("Happy")
    sm.open()