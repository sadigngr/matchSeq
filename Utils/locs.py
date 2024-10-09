import pandas as pd

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


