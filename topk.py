# Serafeim Themistokleous 4555

# Read scores from txt file
def read_scores(filename):
    with open(filename, "r") as rnd:
        # R is an array data structure for rnd.txt file
        R = []

        # Read records in rnd.ttx file
        for record in rnd:
            # Read the line and get only the score value
            score_value = float(record.split()[1])
            # Add value at index value_id
            R.append(score_value)

    return R


def updateTopK(Wk, R, x_id, k):
    if len(Wk) == k:
        for key in Wk:
            if R[x_id] > Wk[key]:
                del Wk[key]
                Wk[x_id] = round(R[x_id], 2)
                break
    else:
        Wk[x_id] = round(R[x_id], 2)


def topK(k, filename1, filename2, filename3):

    R = read_scores(filename1)

    # Count how many lines have been read from both files seq1 and seq2
    counter = 0

    # Top-k objects
    Wk = dict()

    # threshold
    T = 0

    # Objects(ID's) read
    seen_objects = []

    terminate = False

    # Start reading the files seq1.txt and seq2.txt alternately
    with open(filename2, 'r') as seq1, open(filename3, 'r') as seq2:
        # for seq1_object, seq2_object in zip(seq1, seq2):
        for seq1_object, seq2_object in zip(seq1, seq2):
            
            if terminate:
                break

            # Read seq1.txt
            seq1_value_id, seq1_value = seq1_object.split()
            seq1_value_id = int(seq1_value_id)
            seq1_value = float(seq1_value)

            # Sum up scores if lower bound or upper bound of object in seq1
            R[seq1_value_id] += seq1_value
            counter += 1

            # Add object's ID into seen objects
            seen_objects.append(seq1_value_id)

            # Update Wk values
            updateTopK(Wk, R, seq1_value_id, k)

            # Read seq2.txt
            seq2_value_id, seq2_value = seq2_object.split()
            seq2_value_id = int(seq2_value_id)
            seq2_value = float(seq2_value)

            # Sum up scores if lower bound or upper bound of object in seq2
            R[seq2_value_id] += seq2_value
            counter += 1
            
            # Add object's ID into seen objects
            seen_objects.append(seq2_value_id)

            # Update Wk values
            updateTopK(Wk, R, seq2_value_id, k)

            # Update threshold value
            score = seq1_value + seq2_value + 5.0
            T = max(T, score)

            if min(Wk.values()) < T:
                continue
            else:
                for x in seen_objects:
                    if x not in Wk.keys() and (R[x] + seq2_value) > max(Wk.values()):
                        terminate = False
                        break
                    else:
                        terminate = True


    print("Number of sequential accesses= ", counter)
    print("Top k objects:")
    Wk = dict(sorted(Wk.items(), key=lambda item: item[1], reverse=True))
    for id in Wk:
        print(id, ":", Wk[id])


if __name__ == "__main__":
    while True:
        print("For exit press enter")
        print("Input k=", end="")
        k = input()

        if k == "":
            break

        topK(int(k), 'data/rnd.txt', 'data/seq1.txt', 'data/seq2.txt')
        print("\n")
