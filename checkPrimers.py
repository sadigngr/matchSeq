import subprocess
liste = []
with open("sonuclar.txt","r") as f:
    while True:
        primer1 = f.readline()[1:-4]
        f.readline()
        primer2 = f.readline()[1:-4]
        print(primer1,primer2)
            print("BULDU!")
        for i in range(8):
            f.readline()

