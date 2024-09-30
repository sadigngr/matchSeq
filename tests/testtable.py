from concurrent.futures import ThreadPoolExecutor
from Hashing.newTables import HashTable, makeTable
from Hashing.Hash import Hasher
from Hashing.IO import _read
from Utils.Bases import _reverse_bases
import os

def process_key(key, table1, table2, buffer1, buffer2):
    matchTable = HashTable(64)
    
    # Anahtarların geçerli olup olmadığını kontrol et
    hashes1 = table1.getHash(key)
    hashes2 = table2.getHash(key)
    if not hashes1 or not hashes2:
        return matchTable
    
    for _hash in hashes1:
        locs1 = table1.getValue(_hash)
        locs2 = table2.getValue(_hash)

        if not locs1 or not locs2:
            continue

        for loc1 in locs1:
            for loc2 in locs2:
                l = 3
                l1 = loc1
                l2 = loc2

                if buffer1[l1-l-9:l1+8] != buffer2[l2-l-9:l2+8]:
                    continue

                # Dizi eşleştirme döngüsü
                while True:
                    try:
                        h1_prev, h1_next = buffer1[l1 - l - 1], buffer1[l1]
                        h2_prev, h2_next = buffer2[l2 - l - 1], buffer2[l2]
                    except IndexError:
                        break

                    if h1_prev + h1_next == h2_prev + h2_next and "N" not in h1_prev + h1_next:
                        l += 2
                        l1 += 1
                        l2 += 1
                    else:
                        break

                # Eşleşen bölgeyi kontrol et
                if 17 < l < 30:
                    ex = buffer1[l1 - l:l1 - 1]
                    matchHash = Hasher(ex, 0)
                    matchTable.insert(matchHash._hash, [l1 - l + 1, l1, l2 - l + 1, l2])

    return matchTable

def matchSeq(buffer1, buffer2):
    matchTable = HashTable(64)
    table1 = makeTable(buffer1, 1, 64)
    table2 = makeTable(buffer2, 1, 64)
    print("Tablolar Olusturuldu!")
    
    max_workers = min(64, os.cpu_count())  # CPU çekirdek sayısına göre thread sayısını ayarla
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_key, key, table1, table2, buffer1, buffer2) for key in range(64)]
        
        for future in futures:
            result = future.result()
            for i in range(64):
                if result.getHash(i):
                    for j in result.getHash(i):
                        matchTable.insert(i, j)

    return matchTable

if __name__ == "__main__":
    buffer1, buffer2 = _read("/home/sadi/Data/Homo_sapiens.GRCh38.dna.chromosome.11.fa.masked", "/home/sadi/Data/Homo_sapiens.GRCh38.dna.chromosome.21.fa.masked")
    hashTable = matchSeq(buffer1, buffer2)

