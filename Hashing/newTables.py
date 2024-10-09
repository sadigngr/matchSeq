import time

from Hashing.Hash import Hasher

class Seq:

    def __init__(self,_hash : int,_loc : int,_next_node = None):
        self._hash = _hash
        self._loc = [_loc]
        self._next_node = _next_node


class HashTable:

    def __init__(self,max_size):

        self._MAX_SIZE = max_size

        self._table = [None] * self._MAX_SIZE

    def __str__(self):
        table = ""
        table += "{\n"
        for i, val in enumerate(self._table):
            if val:
                llist_string = ""
                node = val
                if node._next_node:
                    while node._next_node:
                        llist_string += (
                            str(node._hash) + " : " + str(node._loc) + " --> "
                        )
                        node = node._next_node
                    llist_string += (
                        str(node._hash) + " : " + str(node._loc) + " --> None"
                    )
                    table +=  f"[{i}] {llist_string}\n"
                else:
                    table += f"[{i}] {val._hash} : {val._loc} --> None\n"
            else:
                table += f"[{i}] {val}\n"
        table += "}\n"

        return table

    def __repr__(self):#TODO Tablo objesini belirtmek icin kullanilacak
        pass

    def __len__(self):
        return self._MAX_SIZE

    def getHash(self,key : int) -> list[int]:
        _hashList = []

        if self._table[key]:
            node = self._table[key]

            while node._next_node:
                _hashList.append(node._hash)
                node = node._next_node

            _hashList.append(node._hash)
            return _hashList
        else:
            return
    def insert(self,_hash : int,_loc : int) -> None:    
        key = _hash%self._MAX_SIZE

        if self._table[key]:
            node = self._table[key]
            while node._next_node:
                if _hash == node._hash:
                    node._loc.append(_loc)
                    return
                node = node._next_node
            if _hash == node._hash:
                node._loc.append(_loc)
            else:
                node._next_node = Seq(_hash,_loc,None)
        else:
            self._table[key] = Seq(_hash,_loc,None)

    def deleteHash(self,_hash) -> None:
        key = _hash%self._MAX_SIZE
        if self._table[key]:
            if _hash == self._table[key]._hash:
                self._table[key] = self._table[key]._next_node
            else:
                node = self._table[key]

                while node._next_node:
                    if _hash == node._next_node._hash:
                        if node._next_node._next_node:
                            node._next_node = node._next_node._next_node
                            break
                        else:
                            node._next_node = None
                            break

                    node = node._next_node

    def deleteIndex(self,key) -> None:
        nodeList = []
        if self._table[key]:

            while self._table[key]._next_node:
                nodeList.append(self._table[key]._next_node)
                self._table[key] = self._table[key]._next_node

            for i in nodeList:
                del i

            del nodeList

            self._table[key] = None

    def getValue(self,_hash : int) -> list[int]:
        key = _hash%self._MAX_SIZE

        if self._table[key]:
            node = self._table[key]
            while node._next_node:
                if _hash == node._hash:
                    return node._loc
                node = node._next_node
            if _hash == node._hash:
                return node._loc
        else:
            return

    def getLocs(self) -> list[list[int]]:
        _list = []
        _llist = []
        for _key in range(self._MAX_SIZE):
            if self._table[_key] is not None:

                node = self._table[_key]
                _list.append(node._hash)
                _list.append(node._loc)
                _llist.append(_list)
                _list = []

                while node._next_node:

                    node = node._next_node
                    _list.append(node._hash)
                    _list.append(node._loc)

                try:
                    if node._loc != _list[-1]:
                        _list.append(node._loc)
                except IndexError:
                    pass

                if _list != []:
                    _llist.append(_list)
            _list = []
        return _llist

def makeTable(buffer,initLoc,hashSize,size):
    hashTable = HashTable(size)
    _hashSize = hashSize - 1

    Hash = Hasher(buffer[:hashSize])
    loc = initLoc + hashSize
    hashTable.insert(Hash._hash,loc)

    for char in buffer[hashSize:]:
        match char:
            case "N":
                loc += 1
                Hash._hash = 0
            case _:
                Hash._rollHash(char)
                print(Hash._hash)
                loc += 1
                if len(str(Hash._hash)) > _hashSize:
                    hashTable.insert(Hash._hash,loc)

        if loc % 10_000 == 0:
            print(loc)
            print(Hash._hash)

    return hashTable

if __name__ == "__main__":
    x = time.time()
    a = HashTable(64)
    a.insert(113,6)
    a.insert(177,9)
    a.insert(113,8)
    a.insert(113,12)
    a.insert(177,10)
    a.insert(241,15)
    a.insert(305,80)
    a.insert(369,81)
    a.insert(70,7)
    a.insert(134,22)
    a.insert(112,10)
    print(a.getValue(177))
    print(a.getHash(49))
    a.deleteHash(369)
    a.deleteHash(177)
    print(a)

    #a.deleteIndex(49)
    #a.print_table()

    #with open("/home/sadi/Data/Homo_sapiens.GRCh38.dna.chromosome.11.fa.masked","r") as f:
        #f.readline()
        #buffer = f.read().replace("\n","")

    #hashTable = makeTable(buffer,1,3,64)

    hashTable1 = makeTable("ANTGC",1,3,64) #TODO : Araya N giren 3'lü KMerlerin arasına N için 0 koyuyor. 
    print(hashTable1)                      #       Sorun olabilir. Mesela ANT için 102 yazıyor. 
    y = time.time()

    print(f"Islem {y - x} saniye surdu.")
