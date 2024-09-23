from SetlistModule import *
all_names = set()

with open("Harvesting/harvest_lsj.txt",'r') as f:
    for line in f: all_names.add((line.split()[0]))
with open("Harvesting/Real_Book_6_Indices.csv", 'r') as f:
    for line in f: all_names.add((line.split(',')[0]))

print(len(all_names))


slib = SongLibrary(name="HARVESTING SONG NAMES")
i=0
for n in all_names:
    i+=1
    print(f"Processing song {i} out of {len(all_names)} ({round(100*i/len(all_names))}%)")
    slib += Song(n, get_pdfs=True)

slib.save_to_file()

