import time

from Utils.Bases import _bases

class Hasher:

    def __init__(self,pattern = "",_hash = 0 ):
        self._multiplier = 10
        self._hash = _hash

        self._pattern = pattern

        #Creating the initial hash value if none given
        if self._hash == 0:
            self._pattern_l = len(pattern)
            self._createHash()
        else:
            self._pattern_l = len(str(_hash))

    
    def __eq__(self,other):
        return self._hash == other._hash

    def _createHash(self):
        for i in range(self._pattern_l):
            self._hash += (_bases[self._pattern[i]] * (self._multiplier**(self._pattern_l - (i+1))))

    def _rollHash(self,value):
        self._hash = (self._hash%(self._multiplier**(self._pattern_l - 1))) * self._multiplier + _bases[value]

    def _extendHash(self,_prev,_next):
        self._hash = self._hash * self._multiplier + _bases[_next]
        self._pattern_l += 1
        self._hash = self._hash + _bases[_prev] * (self._multiplier **(self._pattern_l))
        self._pattern_l += 1

    @property
    def multiplier(self):
        return self._multiplier

    @multiplier.setter
    def multiplier(self,value):
        self._multiplier = value
        self._createHash()

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self,value):
        self._hash = value

if __name__ == "__main__":
    with open("/home/sadi/Data/Homo_sapiens.GRCh38.dna.chromosome.11.fa.masked","r") as f:
        f.readline()
        buffer = f.read().replace("\n","")
    x = 0
    a = time.time()
    print("Selam!")
    newHash = Hasher(buffer[:18])
    print(newHash._hash)
    for char in buffer[18:]:
        if char != "N":
            newHash._rollHash(char)
        x += 1
        if x % 1_000_000 == 0:
            print(x)
            print(newHash._hash)

    b = time.time()

    print(f"Islem {b - a} saniye surdu.")    