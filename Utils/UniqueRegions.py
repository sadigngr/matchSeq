from Hashing.Hash import Hasher

def similarity_ratio(seq1, seq2):
    matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
    return matches / len(seq1)


def findRegions(seq1, seq2, region_size, similarity_threshold):
    unique_regions_seq1 = []
    unique_regions_seq2 = []

    for i in range(0, len(seq1) - region_size + 1):
        if "N" in seq1 or "N" in seq2:
            continue
        region_seq1 = seq1[i:i + region_size]
        best_match_ratio_seq2 = 0
        best_match_region_seq2 = None

        for j in range(0, len(seq2) - region_size + 1):
            region_seq2 = seq2[j:j + region_size]

            if Hasher(region_seq2,0) == Hasher(region_seq1,0):
                continue

            similarity = similarity_ratio(region_seq1, region_seq2)

            if similarity > best_match_ratio_seq2:
                best_match_ratio_seq2 = similarity
                best_match_region_seq2 = (j, region_seq2)

        if best_match_ratio_seq2 < similarity_threshold:
            unique_regions_seq1.append((i, region_seq1))
            if best_match_region_seq2 is not None:
                unique_regions_seq2.append(best_match_region_seq2)

    for i in range(0, len(seq2) - region_size + 1):
        if "N" in seq1 or "N" in seq2:
            continue

        region_seq2 = seq2[i:i + region_size]
        best_match_ratio_seq1 = 0
        best_match_region_seq1 = None

        for j in range(0, len(seq1) - region_size + 1):
            region_seq1 = seq1[j:j + region_size]
            if Hasher(region_seq2,0) == Hasher(region_seq1,0):
                continue
            similarity = similarity_ratio(region_seq2, region_seq1)

            if similarity > best_match_ratio_seq1:
                best_match_ratio_seq1 = similarity
                best_match_region_seq1 = (j, region_seq1)

        if best_match_ratio_seq1 < similarity_threshold:
            unique_regions_seq2.append((i, region_seq2))
            if best_match_region_seq1 is not None:
                unique_regions_seq1.append(best_match_region_seq1)

    return unique_regions_seq1, unique_regions_seq2

if __name__ == "__main__":

    region_size = 30
    similarity_threshold = 0.5

    with open("/Users/sadi/Desktop/sonuclar.txt.nosync.txt","r") as f:
        try:
            while True:
                match1,len1 = f.readline()[1:].split("-")
                loc1,loc2 = f.readline()[1:].split("_")
                match2,len2 = f.readline()[1:].split("-")
                loc3,loc4 = f.readline()[1:].split("_")
                seqid = f.readline()
                seq1 = f.readline()
                f.readline()
                seq2 = f.readline()
                f.readline()

                unique_seq1, unique_seq2 = findRegions(seq1, seq2, region_size, similarity_threshold)
                if unique_seq1 and unique_seq2:
                    print(seqid)
                    print("Seq1 Ozgun Bolgeler:")
                    for idx, region in unique_seq1:
                        print(f"Index {idx}: {region}")
                    print("\nSeq2 Ozgun Bolgeler::")
                    for idx, region in unique_seq2:
                        print(f"Index {idx}: {region}")

        except ValueError:
            print("Dosya Sonu")

