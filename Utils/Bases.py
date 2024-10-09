_bases = {'A': 1, 'T': 2, 'G': 3, 'C': 4,"N" : 0}

reverse_bases ={0 : "N",1 : "A", 2 : "T", 3 : "G", 4 : "C"}

def _reverse_bases(pattern):
    x = ""
    for i in str(pattern):
        x += reverse_bases[int(i)]

    return x

_ambigious_bases = {'R': 0, 'Y': 0, 'W': 0, 'S': 0, 'M': 0, 'K': 0, 'H': 0, 'B': 0, 'V': 0, 'D': 0, 'N': 0}

