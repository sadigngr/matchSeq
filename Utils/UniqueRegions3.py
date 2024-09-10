from concurrent.futures import ThreadPoolExecutor
from Hashing.Hash import Hasher

def hamming_distance(seq1, seq2):
    """Hamming mesafesini hesaplar."""
    if len(seq1) != len(seq2):
        raise ValueError("Diziler aynı uzunlukta olmalı.")

    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))

def hash_sequence(sequence, region_size):
    """Hash tüm 30 bazlık bölgeleri önceden hesaplar."""
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
        best_match_ratio_seq2 = region_size

        for j, hash2 in hashed_seq2:
            if hash1 == hash2:
                continue

            region_seq2 = seq2[j:j + region_size]
            hamming_dist = hamming_distance(region_seq1, region_seq2)

            if hamming_dist < best_match_ratio_seq2:
                best_match_ratio_seq2 = hamming_dist

        if best_match_ratio_seq2 > similarity_threshold * region_size:
            unique_regions_seq1.append((i, region_seq1))

    for i, hash2 in hashed_seq2:
        region_seq2 = seq2[i:i + region_size]
        best_match_ratio_seq1 = region_size

        for j, hash1 in hashed_seq1:
            if hash1 == hash2:
                continue

            region_seq1 = seq1[j:j + region_size]
            hamming_dist = hamming_distance(region_seq2, region_seq1)

            if hamming_dist < best_match_ratio_seq1:
                best_match_ratio_seq1 = hamming_dist

        if best_match_ratio_seq1 > similarity_threshold * region_size:
            unique_regions_seq2.append((i, region_seq2))

    return unique_regions_seq1, unique_regions_seq2

def findRegions(seq1, seq2, region_size, similarity_threshold):
    hashed_seq1 = hash_sequence(seq1, region_size)
    hashed_seq2 = hash_sequence(seq2, region_size)

    if "N" not in seq1 and "N" not in seq2:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(find_unique_regions, seq1, seq2, hashed_seq1, hashed_seq2, region_size, similarity_threshold)
            unique_seq1, unique_seq2 = future.result()

        return unique_seq1, unique_seq2
    else:
        return None,None

if __name__ == "__main__":
    region_size = 30
    similarity_threshold = 50

    with open("/Users/sadi/Desktop/sonuclar.txt.nosync.txt", "r") as f:
        try:
            while True:
                match1, len1 = f.readline()[1:].split("-")
                loc1, loc2 = f.readline()[1:].split("_")
                match2, len2 = f.readline()[1:].split("-")
                loc3, loc4 = f.readline()[1:].split("_")
                seqid = f.readline()
                seq1 = f.readline().strip()
                f.readline()
                seq2 = f.readline().strip()
                f.readline()

                process_sequences(seqid, seq1, seq2, region_size, similarity_threshold)

        except ValueError:
            print("Dosya Sonu")
