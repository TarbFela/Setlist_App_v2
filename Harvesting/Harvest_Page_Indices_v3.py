from string import *
from re import sub
f = open("ToC_v3.txt","r")
f_str = f.read()
f_lines = f_str.split("\n")
f.close()

names = []
volumes = []
pages = []

while "Real Book Volume Index RonHackettMusic.com" in f_lines:
    f_lines.remove("Real Book Volume Index RonHackettMusic.com")


print(len(f_lines))

for i, line in enumerate( f_lines):
    if line.isnumeric(): del f_lines[i]

print(len(f_lines))

for line in f_lines:
    wrds = line.split()
    if not wrds[-1].isnumeric():
        print(f"Bad line: {line}")
        continue

    pages.append(wrds[-1])
    volumes.append(wrds[-2])
    try:
        name = " ".join( wrds[:-2])
        #print(name)
        names.append(name)
    except:
        print(f"Bad sum: {line}, sum of: {wrds[:-2]}")

    if volumes[-1] == "VI": print( pages[-1], volumes[-1], names[-1])




