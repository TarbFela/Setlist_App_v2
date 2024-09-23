from SetlistModule import *

lib = load_from_file()

res = lib.search_library("Ceorea",1)
print(res)
res = lib.search_library("Ceorea",5)
for song in res: print(song.name,end=",")
print()
res = lib.search_library("Ceorea",0)
for song in res: print(song.name,end=",")
