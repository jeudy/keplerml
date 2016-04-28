import sys

path1 = sys.argv[1]
path2 = sys.argv[2]

f1 = open(path1, "r")
f2 = open(path2, "r")
g = open("diff", "w")

conjunto1 = set([i.rstrip() for i in f1.readlines()])
conjunto2 = set([i.rstrip() for i in f2.readlines()])

conjunto3 = conjunto1 - conjunto2

for estrella in conjunto3:
    g.write(estrella + '\n')

f1.close()
f2.close()
g.close