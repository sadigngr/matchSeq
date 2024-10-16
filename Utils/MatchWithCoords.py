from Hashing.newTables import HashTable,makeTable
from Hashing.Hash import Hasher


from Utils.locs import getLocsList

def matchCoords(coords,buffer1,buffer2):
    locs = getLocsList(coords)
    
    matchTable = HashTable(64)

    for pairs in locs:

        start1 = int(pairs[0][0])
        end1 = int(pairs[0][1])
        start2 = int(pairs[1][0])
        end2 = int(pairs[1][1])
        table1 = makeTable(buffer1[start1:end1],start1,3,64)
        table2 = makeTable(buffer2[start2:end2],start2,3,64)
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
