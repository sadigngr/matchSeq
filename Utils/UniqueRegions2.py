from concurrent.futures import ThreadPoolExecutor
from Hashing.Hash import Hasher

def similarity_ratio(seq1, seq2):
    matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
    return matches / len(seq1)

def hash_sequence(sequence, region_size):
    hashes = []
    for i in range(len(sequence) - region_size + 1):
        region = sequence[i:i + region_size]
        hash_value = Hasher(region, 0)
        hashes.append((i, hash_value))
    return hashes

def find_unique_regions(seq1, seq2, hashed_seq1, hashed_seq2, region_size, similarity_threshold):
    unique_regions_seq1 = []
    unique_regions_seq2 = []

    for i, hash1 in hashed_seq1:
        region_seq1 = seq1[i:i + region_size]
        best_match_ratio_seq2 = 0

        for j, hash2 in hashed_seq2:
            if hash1 == hash2:
                continue

            region_seq2 = seq2[j:j + region_size]
            similarity = similarity_ratio(region_seq1, region_seq2)

            if similarity > best_match_ratio_seq2:
                best_match_ratio_seq2 = similarity

        if best_match_ratio_seq2 < similarity_threshold:
            unique_regions_seq1.append((i, region_seq1))

    for i, hash2 in hashed_seq2:
        region_seq2 = seq2[i:i + region_size]
        best_match_ratio_seq1 = 0

        for j, hash1 in hashed_seq1:
            if hash1 == hash2:
                continue

            region_seq1 = seq1[j:j + region_size]
            similarity = similarity_ratio(region_seq2, region_seq1)

            if similarity > best_match_ratio_seq1:
                best_match_ratio_seq1 = similarity

        if best_match_ratio_seq1 < similarity_threshold:
            unique_regions_seq2.append((i, region_seq2))

    return unique_regions_seq1, unique_regions_seq2

def findRegions(seq1, seq2, region_size, similarity_threshold):
    hashed_seq1 = hash_sequence(seq1, region_size)
    hashed_seq2 = hash_sequence(seq2, region_size)

    if "N" not in seq1 and "N" not in seq2:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(find_unique_regions, seq1, seq2, hashed_seq1, hashed_seq2, region_size, similarity_threshold)
            unique_seq1, unique_seq2 = future.result()

        return unique_seq1,unique_seq2
    else:
        return None,None

if __name__ == "__main__":
    region_size = 30
    similarity_threshold = 0.5

    seq1 = "ATGCTATATAGCTAGCTGATCGATGCTAGCTGAGCTAGCTAGATCGAAAAAAAAATTTTTTGGCGCGCGCTATATGAATCGATAGC"
    seq2 = "CTAGCCGCGATGCGCGCGCGCGGCGCGCTAGCATAGCGCGATGGGGCTCGAGCTGATCGCTAGCTGCTAGCTAGCTAGCTAGGGCCGCGCGGCTAGCGT"

    u1,u2 = findRegions(seq1,seq2,region_size,similarity_threshold)
    print(u1,u2)
    with open("rast.txt","w") as f:
        f.writelines(">Seq1\n")
        f.writelines(seq1 + "\n")
        f.writelines(str(u1) + "\n")
        f.writelines(">Seq2\n")
        f.writelines(seq2 + "\n")
        f.writelines(str(u2) + "\n") 
        



