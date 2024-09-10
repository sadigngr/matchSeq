


def testKey(hashTable,_hashTable,_key):
    print("######################KEY : ",_key)
    if hashTable.getHash(_key) is not None:
        for _hash in hashTable.getHash(_key):
            locs11 = hashTable.getValue(_hash)
            locs21 = _hashTable.getValue(_hash)

            if locs11 is None or locs21 is None:
                continue

            for loc11 in locs11:
                for loc21 in locs21:
                    l = 3
                    l11 = loc11
                    l21 = loc21
                    while True:
                        h11_prev = buffer[l11 - l -1]
                        h21_prev = _buffer[l21 - l - 1]
                        try:
                            h11_next = buffer[l11]
                            h21_next = _buffer[l21]
                        except IndexError:
                            ex = "INDEXERROR"
                            break

                        h11 = h11_prev + h11_next
                        h21 = h21_prev + h21_next

                        if h11 == h21 and "N" not in h11 and "N" not in h21:
                            l += 2
                            l11 += 1
                            l21 += 1
                        elif l > 17:
                            ex = buffer[l11-l:l11 - 1 ]

                            ex_loc11 = l11 - l + 1
                            ex_loc21 = l21 - l + 1
                            print(f"SEKANS : {ex}, CHR11 KONUMU {ex_loc11} - {l11} CHR21 KONUMU : {ex_loc21} - {l21}")

                            pts.append([ex,ex_loc11,l11,ex_loc21, l21])
                            break
                        else:
                            break
    return pts


