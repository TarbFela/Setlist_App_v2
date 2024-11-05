fr= open("Real_book_v5_vol3_indices_Raw", "r")
fw = open("Real_book_v5_vol3_indices_cleaned", "w")

f_content = []
i=0
lhc = 0
for line in fr:
    line = line.replace("\n","")
    if len(line.replace(" ","")) > 0:
        if line.replace(" ","").isnumeric():
            #print(f"FOUND A NUMERIC: {line}")
            if i > 200 and int(line)< 200: line = str(int(line)+484)
            f_content.append(str(int(line)))
        elif len(line.replace(" ","")) < 2:
            lhc += 1
            #print(f"FOUND A LETTER HEADER: {line} #{lhc}")
        else:
            #print(f"FOUND A SONG NAME: {line}")
            f_content.append(" ".join(line.split()))
        #if i%2 == 0: print(line)
        #else: print( int(line))

        #f_content.append(line)
        i += 1

fr.close()

print(f"len of f_content = {len(f_content)}")
print(f"last value: {f_content[-1]}")

for i, line in enumerate( f_content):
    fw.write(f"{line:<80}")
    if i%2: fw.write("\n")
    else: fw.write("PG#")

exit()

f_content_paired = {}
for i in range(len(f_content)/2):
    f_content_paired[ f_content[2*i] ] = f_content[2*1 + 1]

for key in f_content_paired:
    fw.write(f_content_paired[key], key)
fw.close()
