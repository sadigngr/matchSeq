from Hashing.newTables import HashTable,makeTable

buffer1 = "ATGCATCGATATGCGC"
buffer2 = "ATGCATGTTGGGATGTGATGT"

table1 = makeTable(buffer1,1,64)
table2 = makeTable(buffer2,1,64)


for i in range(64):
    if table1.getHash(i) and table2.getHash(i):
        for _hash in table1.getHash(i):
            locs1 = table1.getValue(_hash)
            locs2 = table2.getValue(_hash)

            if locs1 is None or locs2 is None:
                continue 
             