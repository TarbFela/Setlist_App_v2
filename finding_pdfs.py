from SetlistModule import *


slib = load_from_file()
i=0
libsize = len(slib.songs)
for song in slib.songs:
    i+=1
    #if i>10: break
    #print(f"Processing song {i} out of {libsize} ({round(100*i/libsize)}%)")
    if len(song.pdfs) == 0:
        #print(f"Song {song.name} has no PDFs...")
        song.find_pdfs(recursive=False, verbose=False)
        if len(song.pdfs) == 0:
            print(f"NRC Song {song.name} STILL! has no PDFs...")
            song.find_pdfs(recursive=False, verbose=False)
            if len(song.pdfs) == 0:
                print(f"YRC Song {song.name} STILL! has no PDFs...")
                print("LAST RESORT:")
                song.find_pdfs(sim_thresh=0.6,recursive=False,verbose=True)

        #print("\n\n")
slib.save_to_file()