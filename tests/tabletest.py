from Hashing.newTables import HashTable,makeTable
from Hashing.Hash import Hasher
from Hashing.IO import _read

from Utils.Bases import _reverse_bases

def matchSeq(buffer1,buffer2):
    matchTable = HashTable(64)
    table1 = makeTable(buffer1,1,64)
    table2 = makeTable(buffer2,1,64)
    print("Tablolar Olusturuldu!")
    for key in range(64):
        if table1.getHash(key) is not None and table2.getHash(key) is not None:
            for _hash in table1.getHash(key):
                locs1 = table1.getValue(_hash)
                locs2 = table2.getValue(_hash)

                if locs1 is None or locs2 is None:
                    continue

                for loc1 in locs1:
                    for loc2 in locs2:
                        l = 3
                        l1 = loc1
                        l2 = loc2

                        if buffer1[l1-l-9:l1+8] != buffer2[l2-l-9:l2+8]:
                            continue

                        while True:
                            h1_prev = buffer1[l1 - l - 1]
                            h2_prev = buffer2[l2 - l - 1]

                            try:
                                h1_next = buffer1[l1]
                                h2_next = buffer2[l2]

                            except IndexError:
                                break

                            h1,h2 = h1_prev + h1_next, h2_prev + h2_next

                            if h1 == h2 and "N" not in h1 and "N" not in h2:
                                l+= 2
                                l1+= 1
                                l2+= 1
                            else:
                                break

                        if l > 17 and l < 30:
                            ex = buffer1[l1-l:l1-1]

                            ex_loc1, ex_loc2 = l1 - l + 1, l2 - l + 1

                            matchHash = Hasher(ex,0)
                            matchTable.insert(matchHash._hash,[ex_loc1,l1,ex_loc2,l2])
                            print(ex,ex_loc1,l1,ex_loc2,l2)

    return matchTable

if __name__ == "__main__":

    buffer1,buffer2 = _read("/home/sadi/Data/Homo_sapiens.GRCh38.dna.chromosome.11.fa.masked","/home/sadi/Data/Homo_sapiens.GRCh38.dna.chromosome.21.fa.masked")

    hashTable = matchSeq(buffer1,buffer2)

    """for i in range(64):
        if hashTable.getHash(i):
            for j in hashTable.getHash(i):
                print(_reverse_bases(j))
"""
    print(hashTable)




