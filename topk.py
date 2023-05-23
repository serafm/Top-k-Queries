# Serafeim Themistokleous 4555
import time


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


# Update the top k objects (Check if a new score is greater than the minimum)
def updateTopK(Wk, scores, x_id, k):
    if len(Wk) == k:
        key = min(Wk, key=Wk.get)
        if scores[x_id] > Wk[key]:
            del Wk[key]
            Wk[x_id] = round(scores[x_id], 2)
    else:
        Wk[x_id] = round(scores[x_id], 2)


def topK(k, R, filename2, filename3):

    # Lower Bound / Final  dictionaries
    lower_bounds = dict()
    final_scores = dict()

    # Count how many lines have been read from both files seq1 and seq2
    counter = 0

    # Top-k objects
    Wk = dict()

    # Objects(ID's) have been read
    seen_objects = []

    # Boolean for termination of the topK
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
            seq1_value = round(float(seq1_value), 2)
            counter += 1

            # Sum up scores if lower bound OR final score of object in seq1
            if seq1_value_id in seen_objects:
                final_scores[seq1_value_id] = round(lower_bounds[seq1_value_id] + seq1_value, 2)
            else:
                lower_bounds[seq1_value_id] = round(R[seq1_value_id] + seq1_value, 2)

            # Update Wk values (Top-k)
            if seq1_value_id in seen_objects:
                updateTopK(Wk, final_scores, seq1_value_id, k)
            else:
                updateTopK(Wk, lower_bounds, seq1_value_id, k)

            # Add object's ID into seen objects
            seen_objects.append(seq1_value_id)

            # Read seq2.txt
            seq2_value_id, seq2_value = seq2_object.split()
            seq2_value_id = int(seq2_value_id)
            seq2_value = round(float(seq2_value), 2)
            counter += 1

            # Sum up scores if lower bound OR final score of object in seq2
            if seq2_value_id in seen_objects:
                final_scores[seq2_value_id] = round(lower_bounds[seq2_value_id] + seq2_value, 2)
            else:
                lower_bounds[seq2_value_id] = round(R[seq2_value_id] + seq2_value, 2)

            # Update Wk values (Top-k)
            if seq2_value_id in seen_objects:
                updateTopK(Wk, final_scores, seq2_value_id, k)
            else:
                updateTopK(Wk, lower_bounds, seq2_value_id, k)

            # Add object's ID into seen objects
            seen_objects.append(seq2_value_id)

            # Threshold
            T = round(seq1_value + seq2_value + 5.0, 2)

            # If Wk minimum lower bound is smaller than threshold we continue reading the files
            if min(Wk.values()) < T:
                continue
            else:
                for x in seen_objects:
                    # For every seen object we check if the object is not in Wk
                    if x not in Wk.keys():
                        # If it's not in the Wk we calculate its upper bound
                        upper_bound = round(lower_bounds[x] + seq2_value, 2)
                        # If it's upper bound is greater than the minimum value of the Wk then we continue reading the files
                        if upper_bound > min(Wk.values()):
                            terminate = False
                            break
                        else:
                            # Else ser the terminate value to True for termination
                            # The top k scores have been read so no need to continue
                            terminate = True

    print("Number of sequential accesses= ", counter)
    print("Top k objects:")
    Wk = dict(sorted(Wk.items(), key=lambda item: item[1], reverse=True))
    for id in Wk:
        print(id, ":", Wk[id])


if __name__ == "__main__":

    # Create array R with the rnd.txt scores
    R = read_scores('data/rnd.txt')

    while True:
        print("For exit press enter")
        print("Input k=", end="")
        k = input()

        if k == "":
            break

        start = time.time()
        topK(int(k), R, 'data/seq1.txt', 'data/seq2.txt')
        end = time.time()
        final = round(end - start, 2)
        print("Time:", final, "ms")
        print("\n")
