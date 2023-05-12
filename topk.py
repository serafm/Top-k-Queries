# Serafeim Themistokleous 4555
import sys


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


def topK(k):

    R = read_scores("data/rnd.txt")

    # Count how many lines have been read from both files seq1 and seq2
    counter = 0

    # Top-k objects
    Wk = dict()

    # Objects(ID's) read
    seen_objects = []

    terminate = False

    # Start reading the files seq1.txt and seq2.txt alternately
    with open('data/seq1.txt', 'r') as seq1, open('data/seq2.txt', 'r') as seq2:
        for seq1_object, seq2_object in zip(seq1, seq2):

            # Check for termination
            if terminate:
                break

            seq1_value_id, seq1_value = seq1_object.split()
            seq1_value_id = int(seq1_value_id)
            seq1_value = float(seq1_value)

            # Sum up scores of object in seq1
            R[seq1_value_id] += seq1_value

            # Add object's ID into seen objects
            seen_objects.append(seq1_value_id)

            counter += 1

            seq2_value_id, seq2_value = seq2_object.split()
            seq2_value_id = int(seq2_value_id)
            seq2_value = float(seq2_value)

            # Sum up scores of object in seq2
            R[seq2_value_id] += seq2_value

            # Add object's ID into seen objects
            seen_objects.append(seq2_value_id)

            counter += 1

            # Add score and id into Wk
            if len(Wk) < k:
                Wk[seq1_value_id] = round(R[seq1_value_id], 2)
            if len(Wk) < k:
                Wk[seq2_value_id] = round(R[seq2_value_id], 2)
            else:
                for id in Wk:
                    # If seq1 score is greater than an object's score in Wk then replace
                    if R[seq1_value_id] > Wk[id]:
                        del Wk[id]
                        Wk[seq1_value_id] = round(R[seq1_value_id], 2)
                        break
                for id in Wk:
                    # If seq2 score is greater than an object's score in Wk then replace
                    if R[seq2_value_id] > Wk[id]:
                        del Wk[id]
                        Wk[seq2_value_id] = round(R[seq2_value_id], 2)
                        break

            # Threshold update value
            T = seq1_value + seq2_value + 5.0

            # Check if T is greater than max value in Wk if true continue reading the files else stop
            if max(Wk.values()) < T:
                continue
            else:
                for x in seen_objects:
                    if x not in Wk.items() and (R[x] + seq2_value) > max(Wk.values()):
                        continue
                    else:
                        terminate = True

    print("Number of sequential accesses= ", counter)
    print("Top k objects:")
    Wk = dict(sorted(Wk.items(), key=lambda item: item[1], reverse=True))
    for id in Wk:
        print(id, ":", Wk[id])


if __name__ == "__main__":
    print("Enter k:")
    input = input()
    topK(int(input))
