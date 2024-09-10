# matchSeq

İki kromozom arasındaki eşsiz bölgeler içeren, başı ve sonu %100 aynı olan sekansları bulur.

Örn.

CHR1 : ATGC----------------Unique_Base_30nt------------GCTA Locations : 1234 - 1534, Length -> 300 


CHR2 : ATGC----Unique_Base_30nt-----------------------------GCTA Locations : 10234 - 10484, Length -> 250


KULLANIM : 

python3 matchseq2.py -seqFiles [Sekans Dosyaları] -coords [NUCMER'in oluşturduğu coords dosyası]

Çalışması bittikten sonra program sonuclar.txt adında bir dosya oluşturacaktır. Bu dosya %100 eşleşen 18-30 bazlık ikili sekansları, bu sekanslar arasında kalan birbiri arasında eşsiz bölgeleri ve sonuçta oluşturulan ve yukarıdakilerin hepsini içeren 250-300 bazlık bölgeleri içerir.

Örnek olarak 

ATGC------ATTCG(Eşsiz Bölge)-------------AGTC(Eşsiz Bölge)-------------CTGGA 

ve

ATGC------------AAGC(Eşsiz Bölge)-------------------------CTGGA

sekansları kullanılacaktır. 

Her bir sekans için dosyada 11 satır ayrılmıştır. Satır satır olmak üzere dosya şu şekilde okunur:

1. Satır : @ ile başlar, bulunan birinci %100 eşleşmeye sahip 18-30 bazlık bölgeyi ve uzunluğunu ifade eder. Örn. @ATGC-4

2. Satır : ! ile başlar, üst satırdaki %100 eşleşmeye sahip 18-30 bazlık bölgenin verilen iki kromozom örneğindeki konumlarını ifade eder. Her bir kromozom için başlangıç ve sonlar "-" işareti ile ayrılırken, diğer kromozoma geçildiğini belirtmek için "_" kullanılır.  Örn. !1230-1234_15305_15309

3. Satır : @ ile başlar, bulunan ikinci %100 eşleşmeye sahip 18-30 bazlık bölgeyi ve uzunluğunu ifade eder. Örn. @CTGGA-5

4. Satır : ! ile başlar, yine üst satırdaki %100 eşleşmeye sahip 18-30 bazlık bölgenin verilen iki kromozom örneğindeki konumlarını ifade eder. Örn. !1530_1534_15336_15340

5. Satır : > ile başlar, birinci sekansı ve örnek numarasını belirtir. Örn. >Seq121

6. Satır : Birinci sekansı içerir. Örn. ATGC-------ATTCG(Eşsiz Bölge)------------AGTC(Eşsiz Bölge)-------------CTGGA

7. Satır : # ile başlar, birinci sekanstaki eşsiz bölgeleri ve sekansın içindeki konumlarını verir. Örn. [(51, 'ATTCG'),(210, 'AGTC')]

8. Satır : > ile başlar, ikinci sekansı belirtir, örnek numarasının yanına ".1" koyarak oluşturulur. Örn. >Seq121.1

9. Satır : İkinci Sekansı içerir. Örn .  ATGC------------AAGC(Eşsiz Bölge)-------------------------CTGGA

10. Satır : # ile başlar, ikinci sekanstaki eşsiz bölgeleri ve sekansın içindeki konumlarını verir. Örn. [(124, 'AAGC')]

11. Satır : + işareti içerir, okunan örneğin bittiğini ve yeni örneğe geçildiğini belirtir.