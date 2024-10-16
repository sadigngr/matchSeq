import pandas as pd
import sys

from Hashing.newTables import HashTable
from Hashing.Hash import Hasher
from Hashing.IO import _read

from Utils.Bases import _reverse_bases

#Gets the locations from the NUCMER coords table
def getLocsList(_path):
    df = pd.read_fwf(_path)

    ind = len(df) - 3
    x = 0
    y = 0

    z = []
    for i in range(0,ind):
        for j in df.loc[i+3]:
            a = j.split("|")
            for k in a:
                for l in k.strip().split(" "):
                    if l != " " and list(l) != []:
                        z.append(l)
    locs = []
    loc11 = []
    loc21 = []
    for m in z:
        if x < 4:
            if y<2:
                loc11.append(m)
                y+= 1
            else:
                loc21.append(m)
            x+=1
        elif x >= 4 and x < 7:
            x+=1
        elif x == 7:
            x = 0
            y = 0
            locs.append([loc11,loc21])
            loc11,loc21 = [],[]
    return locs

#Gets the program's own locations file.
def findSimilarMatches(_path1,_path2,buffer1,buffer2):
    pathList = [_path1,_path2]
    tableList = []
    locs = []
    locBuffer = []
    for _path in pathList:
        table = HashTable(4096)
        with open(_path,"r") as f:
            data = f.readline().replace("\n","")

            while data:
                if data == "+":
                    hashValue = None
                elif ">" in data:
                    hashValue = Hasher(data[1:])
                else:
                    for i in data.split(","):
                        if i != "":
                            table.insert(hashValue._hash,int(i))
                
                data = f.readline().replace("\n","")
            
            tableList.append(table)
    
    table1,table2 = tableList[0],tableList[1]

    similar = []
    locs = []
    sayac = 0
    locSayac = 0
    for key in range(4096):
        locBuffer = []
        if table1.getHash(key) and table2.getHash(key):
            for x in table1.getHash(key):
                for y in table2.getHash(key):
                    if x == y:
                        sayac += 1
                        locSayac += len(table1.getValue(x)) * len(table2.getValue(x))
                        locBuffer.append([table1.getValue(x),table2.getValue(x)])
                        similar.append(_reverse_bases(x))
        if locBuffer:
            locs.append(locBuffer)
    
    
    print(sayac)
    print(locSayac)

    sayac = 0
    hSayac = 0
    aligned = 0
    alignedLocs = []
    for a in locs:

        for b in a:
            for c in b[0]:
                loc1 = c
                for d in b[1]: 
                    loc2 = d
                    
                    hamming = 0
                    seq1 = buffer1[loc1-250:loc1+250]
                    seq2 = buffer2[loc2-250:loc2+250]
                    
                    for lenin in range(len(seq1)):
                        if seq1[lenin] != seq2[lenin]:
                            hamming += 1

                        if seq1[lenin] == "N":
                            hamming += 1
                        if seq2[lenin] == "N":
                            hamming += 1 
                    sayac += 1
                    if 25 < hamming < 50:
                        hSayac += 1
                        print("HAMMING : ",hSayac)
                        alignedLocs.append([loc1,loc2])

                    if sayac % 1_000 == 0:
                        print(sayac)
                    

                    """
                    for alignment in pairwise2.align.localms(seq1,seq2,2,-1,-2,-0.5):
                        aligned_seq1, aligned_seq2, score, start, end = alignment

                        non_aligned = len(aligned_seq1) - 2000
                        aligned = 2000 - non_aligned

                    if 1000 <= aligned <= 2000:
                        
                        alignedLocs.append([loc1,loc2])
    """
    return alignedLocs
if __name__ == "__main__":
    buffer1,buffer2 = _read(sys.argv[3],sys.argv[4])
    print(findSimilarMatches(sys.argv[1],sys.argv[2],buffer1,buffer2))

    #print(getLocsList(sys.argv[1]))
                

