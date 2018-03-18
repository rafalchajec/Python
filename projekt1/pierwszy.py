import sys
import json
from pathlib import Path

# czy istnieje plik
if Path(sys.argv[1]).is_file() == 0:
    print("PLIK NIE ISTENIEJE!")
    exit(1)

# ---------------------
print("WARTOSCI PRZED SORTOWANIEM")
# ---------------------

# wczytanie
tab = []
with open(sys.argv[1]) as plik_json:
    data = json.load(plik_json)
    for i in data["input_list"]:
        tab.append(i)
        print(i)

# ---------------------
print("")
# ---------------------

# sortowanie

posortowane = False
while posortowane == False:
    posortowane = True
    for i in range(len(tab) - 1):
        if tab[i] > tab[i + 1]:
            posortowane = False
            zamiana = tab[i]
            tab[i] = tab[i + 1]
            tab[i + 1] = zamiana

# ---------------------

print("POSORTOWANE WARTOSCI:")
# ---------------------
for i in tab:
    print(i)
print("")
