import sys

#TODO argparse ile daha düzgün bir argument parsing yapılacak.

from Hashing.IO import _read

from Utils.Errors import BadArgsError
from Utils.Bases import _reverse_bases
from Utils.UniqueRegions2 import findRegions
from Utils.MatchWithCoords import matchCoords

def main():
    path1,path2,coords = None,None,None

    if sys.argv[1] == "-h" or "--help" and len(sys.argv) == 2:
        print("Usage : python3 matchTable.py --seqFiles [path-to-first-seqFile] [path-to-second-seqFile] --coords [path-to-coordsFile]")
        print()
        print("-h or --help : Shows this page")
        print()
        print("-s or --seqFiles : Takes the necessary sequence files.")
        print()
        print("-c or --cords : Takes the coords table from NUCMER.")
        print()
        exit()

    for i,j in enumerate(sys.argv):
        if j == "-s" or "--seqFiles":
            path1,path2 = sys.argv[i+1],sys.argv[i+2]
        elif j  == "-c" or "--coords":
            coords = sys.argv[i+1]
    if path1 is None or path2 is None or coords is None:
        raise BadArgsError()
        # Custom Error, Utils.Errors modulunun icinde yer aliyor.
    buffer1,buffer2 = _read(path1,path2)
    matchTable = matchCoords(coords,buffer1,buffer2)
    locList = []
    seqSayac = 1
    seqSayac1 = 1

    for key in range(64):

        for _ in matchTable.getHash(key):
            _hash = str(_)
            if "1" in _hash and "2" in _hash and "3" in _hash and "4" in _hash:
                pass
            else:
                matchTable.deleteHash(_)
    with open("sonuclar.txt","w") as f:
        for _key in range(64):
            for i in matchTable.getHash(_key):
                locs = matchTable.getValue(i)
                start1 = locs[0][0]
                end1 = locs[0][1]
                start2 = locs[0][2]
                end2 = locs[0][3]
                #f.writelines(f"SEKANS : {_reverse_bases(i)}, UZUNLUK : {len(str(i))}, KONUM VERILERI ---> CHR11 : {start1} - {end1} CHR21 : {start2} - {end2} \n\n")
                locList.append([i,start1,start2])

                for j in locList:
                    if abs(start1 - j[1]) < 300 and abs(start2 - j[2]) < 300 and abs(start1 -j[1]) > 150 and abs(start2 - j[2]) > 150:

                        locs = matchTable.getValue(j[0])
                        _start1 = locs[0][0]
                        _end1 = locs[0][1]
                        _start2 = locs[0][2]
                        _end2 = locs[0][3]
                        if start1 < _start1:
                            s1 = start1 - 1
                            e1 = _end1 - 1
                        else:
                            s1 = _start1 - 1
                            e1 = end1 - 1

                        if start2 < _start2:
                            s2 = start2 - 1
                            e2 = _end2 - 1
                        else:
                            s2 = _start2 - 1
                            e2 = end2 - 1

                        seq1 = buffer1[s1:e1]
                        seq2 = buffer2[s2:e2]

                        unique1,unique2 = findRegions(seq1,seq2,30,0.5)

                        #print(f"SEKANS IKILISI ---> {_reverse_bases(j[0])}, UZUNLUK : {len(str(j[0]))}, KONUM VERILERI ---> CHR11 : {_start1} - {_end1} CHR21 : {_start2} - {_end2}\n              {_reverse_bases(i)}, UZUNLUK : {len(str(i))}, KONUM VERILERI ---> CHR11 : {start1} - {end1} CHR21 : {start2} - {end2} \n ARADAKI UZAKLIK ---> CHR11 : {abs(start1 - j[1])} CHR21 : {abs(start2 - j[2])} \n SEQ1 : {seq1} \n SEQ2 : {seq2}\n\n")
                        seqSayac1 += 1
                        if unique1 and unique2:
                            print(seqSayac1)
                            print(f"@{_reverse_bases(j[0])}-{len(str(j[0]))}\n!{_start1}-{_end1}_{_start2}-{_end2}\n@{_reverse_bases(i)}-{len(str(i))}\n!{start1}-{end1}_{start2}-{end2}\n>Seq{seqSayac}\n{seq1}\n#{unique1}\n>Seq{seqSayac}.1\n{seq2}\n#{unique2}\n+\n")
                            f.writelines(f"@{_reverse_bases(j[0])}-{len(str(j[0]))}\n!{_start1}-{_end1}_{_start2}-{_end2}\n@{_reverse_bases(i)}-{len(str(i))}\n!{start1}-{end1}_{start2}-{end2}\n>Seq{seqSayac}\n{seq1}\n#{unique1}\n>Seq{seqSayac}.1\n{seq2}\n#{unique2}\n+\n")
                            seqSayac += 1

        # DOSYA OKUNUSU :
        # @ = EXACT MATCH OLAN SEKANSLARI VE UZUNLUGUNU IFADE EDER
        # ! = KONUM VERILERINI IFADE EDER, IKI KROMOZOM ARASINDA _ BULUNUR.
        # >SeqX = EXACT MATCHLER VE ARASINDA KALAN BOLGEYI IFADE EDER ALT SATIRDA SEKANS BULUNUR. ART ARDA IKI TANE YAZDIRIR
        # + = YENI ORNEGE GECISI IFADE EDER
        # # UNIQUE BOLGELERIN BIR LISTESINI IFADE EDER


if __name__ == "__main__" : 
    main()
