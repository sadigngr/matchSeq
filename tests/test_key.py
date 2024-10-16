import sys

from Hashing.Hash import Hasher
from Hashing.newTables import HashTable,makeTable

from Hashing.IO import _read


def testKey(key,buffer1,buffer2,table1,table2):
    matchTable = HashTable(64)

    if table1.getHash(key) is not None and table2.getHash(key) is not None:
        for _hash in table1.getHash(key):
            locs1 = table1.getValue(_hash)
            locs2 = table2.getValue(_hash) 

            if locs1 is None or locs2 is None:
                continue

            for loc1 in locs1:
                l = 3
                for loc2 in locs2:
                    l1 = loc1
                    l2 = loc2

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
    return matchTable

if __name__ == "__main__":

    buffer1,buffer2 = _read(sys.argv[1],sys.argv[2])
    table1 = makeTable(buffer1,1,3,64)
    table2 = makeTable(buffer2,1,3,64)

    print(testKey(1,buffer1,buffer2,table1,table2))

