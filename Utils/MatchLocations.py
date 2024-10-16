from Utils.locs import findSimilarMatches

from Hashing.IO import _read
from Hashing.newTables import HashTable,makeTable
from Hashing.Hash import Hasher

import sys

def matchLocs(locFile1,locFile2,buffer1,buffer2):
    sayac = 0
    #locList = findSimilarMatches(locFile1,locFile2)
    locList = [[100666695, 18858009], [100666674, 18857988], [90101336, 8683463], [90109637, 8692043], [90101142, 8683269], [100666671, 18857985], [100666680, 18857994], [100666696, 18858010], [90109636, 8692042], [90101300, 8683427], [90101138, 8683265], [90101298, 8683425], [90101333, 8683460], [100666677, 18857991], [90100230, 8682356], [90109593, 8691999]]
    matchTable = HashTable(64)
    tables1 = []
    tables2 = []

    for b in locList:
            tables1.append(makeTable(buffer1[b[0]-250:b[0]+250],b[0]-250,3,64))
            tables2.append(makeTable(buffer2[b[1]-250:b[1]+250],b[1]-250,3,64))

    for table1 in tables1:
        for table2 in tables2:
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

    print(matchLocs("1","2",buffer1,buffer2))
