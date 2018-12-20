from flair.data import Dictionary

d = Dictionary()
for line in open("characters_merged.txt"):
    if line.strip("\n"):
        c = line.strip("\n")[0]
        d.add_item(c)
d.add_item("\n")
d.add_item(" ")
d.save("characters_merged.bin")
print("Done")