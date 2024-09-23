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
for song in song_set:
    lib = lib + Song(song)
lib.save_to_file()