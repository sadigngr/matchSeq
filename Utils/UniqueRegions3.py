import time

from Hashing.newTables import HashTable,makeTable
from Hashing.Hash import Hasher

from Utils.Bases import _reverse_bases

def FindRegions(seq1,seq2):
    if "N" in seq1 or "N" in seq2:
        return 0 
    table1 = makeTable(seq1,1,5,64)
    table2 = makeTable(seq2,1,5,64)

    for i in range(64):
        try:
            for _ in table1.getHash(i):
                if _ in table2.getHash(i):
                    table1.deleteHash(_)
                    table2.deleteHash(_)
        except TypeError:
            pass

    liste = []

    for i in range(64):
        try:
            for _ in table1.getHash(i):
                liste.append(_reverse_bases(str(_)))

        except TypeError:
            pass

    if len(liste) > 5:

        locList = []
        _locList = []

        for loc in table1.getLocs():
            for loc1 in loc[1]:
                for loc2 in locList:
                    if abs(loc1 - loc2) < 3:
                        if loc1 not in _locList: 
                            _locList.append(loc1)
                        if loc2 not in _locList:
                            _locList.append(loc2)
                locList.append(loc1)

        print(seq1,seq2)
        print(table1)
        print(liste)
        print("LOKASYONLAR : ", sorted(_locList))

if __name__ == "__main__":
    time1 = time.time()
    with open("/home/sadi/sonuclar.txt","r") as f:
        while True: 
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            f.readline()
            seq1 = f.readline().replace("\n","")
            f.readline()
            f.readline()
            seq2 = f.readline().replace("\n","")
            f.readline()
            f.readline()

            FindRegions(seq1,seq2)
    time2 = time.time()

    print(f"Islem {time2 - time1} saniye surdu.")         
