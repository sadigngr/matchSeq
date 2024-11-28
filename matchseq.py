helpPage = """

Usage : matchseq --filter(optional) --seqFiles [path-to-first-seqFile] [path-to-second-seqFile] --coords(optional) [path-to-coordsFile] 

Arguments : 

    -h or --help : Shows this page.

    -s or --seqFiles : Takes the necessary sequence files.

    -c or --coords : Takes the coords table from NUCMER. It is optional.

    -f or --filter : Filters the raw data for spesific locations.

    WARNING : You can't use NUCMER coords files and filtering at the same time.

"""

#TODO argparse ile daha düzgün bir argument parsing yapılacak.

import sys
from Hashing.IO import _read

from Utils.Errors import BadArgsError
from Utils.Bases import _reverse_bases
from Utils.UniqueRegions4 import findFrequency

from Utils.MatchWithCoords import matchCoords
from Utils.MatchWithoutCoords import matchWCoords
from Utils.MatchLocations import matchLocs


def main():
    seq_len_max = 300
    seq_len_min = 150
    path1,path2,coords,locations = None,None,None,False
    argsList = ["-h","--help","-s","--seqFiles","-c","--coords","-f","--filter"]
    
    for i in sys.argv[1:]:
        if i not in argsList:
            raise BadArgsError()
    try:
        if sys.argv[1] == "-h" or "--help" and len(sys.argv) == 2:
            print(helpPage)
            exit()
    except IndexError:
        print(helpPage)
        print("No arguments have been given. Quitting...\n")
        exit()
    for i,j in enumerate(sys.argv):
        if j == "-s" or j == "--seqFiles":
            path1,path2 = sys.argv[i+1],sys.argv[i+2]
        elif j  == "-c" or j == "--coords":
            coords = sys.argv[i+1]
        elif j == "-f" or j == "--filter":
            locations = True

        # Custom Error, Utils.Errors modulunun icinde yer aliyor.
    
    if path1 is not None and path2 is not None and coords is None and locations != True:
        buffer1,buffer2 = _read(path1,path2)
        matchTable = matchWCoords(buffer1,buffer2)
        print(matchTable)
   
    elif path1 and path2 and coords:
        buffer1,buffer2 = _read(path1,path2)
        matchTable = matchCoords(coords,buffer1,buffer2)
 
    elif path1 and path2 and locations == True: #IN PROGRESS DENEY ASAMASINDA
        
        buffer1,buffer2 = _read(path1,path2)
        loc1 = "1.locs"
        loc2 = "2.locs"
        #findFrequency(buffer1,loc1)
        #findFrequency(buffer2,loc2)
        matchTable = matchLocs("./sonuc.txt","./sonuc1.txt",buffer1,buffer2)
        
    
    
    locList = []
    seqSayac = 1
    seqSayac1 = 1
     
    with open("sonuclar.txt","w") as f:
        for _key in range(64):
            try:
                for i in matchTable.getHash(_key):
                    locs = matchTable.getValue(i)
                    
                    start1 = locs[0][0]
                    end1 = locs[0][1]
                    start2 = locs[0][2]
                    end2 = locs[0][3]

                    #f.writelines(f"SEKANS : {_reverse_bases(i)}, UZUNLUK : {len(str(i))}, KONUM VERILERI ---> CHR11 : {start1} - {end1} CHR21 : {start2} - {end2} \n\n")
                    locList.append([i,start1,start2])

                    for j in locList:
                        if abs(start1 - j[1]) < seq_len_max and abs(start2 - j[2]) < seq_len_max and abs(start1 -j[1]) > seq_len_min and abs(start2 - j[2]) > seq_len_min:

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

                            unique1,unique2 = [1],[2]


                            #print(f"SEKANS IKILISI ---> {_reverse_bases(j[0])}, UZUNLUK : {len(str(j[0]))}, KONUM VERILERI ---> CHR11 : {_start1} - {_end1} CHR21 : {_start2} - {_end2}\n              {_reverse_bases(i)}, UZUNLUK : {len(str(i))}, KONUM VERILERI ---> CHR11 : {start1} - {end1} CHR21 : {start2} - {end2} \n ARADAKI UZAKLIK ---> CHR11 : {abs(start1 - j[1])} CHR21 : {abs(start2 - j[2])} \n SEQ1 : {seq1} \n SEQ2 : {seq2}\n\n")
                            seqSayac1 += 1
                            if unique1 and unique2 and "N" not in seq1 and "N" not in seq2:
                                print(seqSayac1)
                                print(f"@{_reverse_bases(j[0])}-{len(str(j[0]))}\n!{_start1}-{_end1}_{_start2}-{_end2}\n@{_reverse_bases(i)}-{len(str(i))}\n!{start1}-{end1}_{start2}-{end2}\n>Seq{seqSayac}\n{seq1}\n#{unique1}\n>Seq{seqSayac}.1\n{seq2}\n#{unique2}\n+\n")
                                f.writelines(f"@{_reverse_bases(j[0])}-{len(str(j[0]))}\n!{_start1}-{_end1}_{_start2}-{_end2}\n@{_reverse_bases(i)}-{len(str(i))}\n!{start1}-{end1}_{start2}-{end2}\n>Seq{seqSayac}\n{seq1}\n#{unique1}\n>Seq{seqSayac}.1\n{seq2}\n#{unique2}\n+\n")
                                seqSayac += 1

            except TypeError:
                pass

        # DOSYA OKUNUSU :
        # @ = EXACT MATCH OLAN SEKANSLARI VE UZUNLUGUNU IFADE EDER
        # ! = KONUM VERILERINI IFADE EDER, IKI KROMOZOM ARASINDA _ BULUNUR.
        # >SeqX = EXACT MATCHLER VE ARASINDA KALAN BOLGEYI IFADE EDER ALT SATIRDA SEKANS BULUNUR. ART ARDA IKI TANE YAZDIRIR
        # + = YENI ORNEGE GECISI IFADE EDER
        # # UNIQUE BOLGELERIN BIR LISTESINI IFADE EDER


if __name__ == "__main__" : 
    main()

