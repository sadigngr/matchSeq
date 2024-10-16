from Hashing.Hash import Hasher
from Hashing.newTables import HashTable, makeTable

from Utils.Bases import _reverse_bases

import sys 

def findFrequency(buffer,fileName):

    fTable = makeTable(buffer,1,9,65003)

    with open(fileName,"w") as f:
        for i in fTable.getLocs():
            if len(i[1]) > 200:
                pass
            else:
                f.writelines(">" + _reverse_bases(str(i[0])) + "\n")
                for j in i[1]:
                    f.writelines(str(j)+",")
                f.writelines("\n")
                f.writelines("+\n")

if __name__ == "__main__":
    with open(sys.argv[1],"r") as f:
        f.readline()
        buffer = f.read().replace("\n","")
    findFrequency(buffer,"sonuc.txt")
    