from SetlistModule import *

files = ["Harvesting/harvest_realbooklisten.txt","Harvesting/harvest_lsj.txt" ]

song_set = set()
for filepath in files:
    with open(filepath, 'r') as f:
        for line in f:
            if line == '': continue
            while line[-1] == '\n':
                line = line[:-1]
            song_set.add(
                name_cleanup(line)
            )
print(song_set)

lib = SongLibrary()

size = len(song_set)
i = 0
for song in song_set:
    i+=1
    if i%10 == 0: print(f"{i}/{size} songs processed... {round(100*i/size)}%")
    s = Song(song)
    s.find_pdfs()
    lib = lib + Song(song)
lib.save_to_file()