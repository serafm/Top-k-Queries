# Serafeim Themistokleous 4555
import sys
import time
import heapq


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


class MinHeap:
    def __init__(self):
        self.heap = []  # Initialize an empty list to store the heap elements
        self.index = 0  # Initialize an index to track the insertion order of elements

    def push(self, item):
        # Add an item to the heap
        # Use the second element of the tuple as the sorting key
        heapq.heappush(self.heap, (item[1], self.index, item))
        self.index += 1

    def pop(self):
        # Remove and return the minimum item from the heap
        return heapq.heappop(self.heap)[2]

    def min(self):
        # Get the minimum value in the heap
        if len(self.heap) > 0:
            return self.heap[0][0]
        else:
            raise IndexError("minHeap is empty")

    def keys(self):
        # Return a list of keys (first elements) from all the tuples in the heap
        return [item[2][0] for item in self.heap]

    def is_empty(self):
        # Check if the heap is empty
        return len(self.heap) == 0

    def sort(self):
        # Sort the tuples in the heap based on the second element in descending order
        sorted_tuples = []
        while not self.is_empty():
            sorted_tuples.append(self.pop())
        sorted_tuples.sort(key=lambda x: x[1], reverse=True)
        return sorted_tuples

    def size(self):
        # Return the size of the heap
        return len(self.heap)


# Update the top k objects (Check if a new score is greater than the minimum in heap)
def updateTopK(Wk, scores, x_id, k):
    if Wk.size() == k:
        if scores[x_id] > Wk.min():
            Wk.pop()
            Wk.push((x_id, round(scores[x_id], 2)))
    else:
        # Initialize the first 5 objects into the Wk heap
        Wk.push((x_id, round(scores[x_id], 2)))


def topK(k, R, filename1, filename2):
    # Lower Bound / Final  dictionaries
    lower_bounds = dict()
    final_scores = dict()

    # Count how many lines have been read from both files seq1 and seq2
    counter = 0

    # Top-k objects
    Wk = MinHeap()

    # Objects(ID's) have been read
    seen_objects = []

    # Boolean for termination of the topK
    terminate = False

    # Start reading the files seq1.txt and seq2.txt alternately
    with open(filename1, 'r') as seq1, open(filename2, 'r') as seq2:
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
            if Wk.min() < T:
                continue
            else:
                for x in seen_objects:
                    # For every seen object we check if the object is not in Wk
                    if x not in Wk.keys():
                        # If it's not in the Wk we calculate its upper bound
                        upper_bound = round(lower_bounds[x] + seq2_value, 2)

                        # If it's upper bound is greater than the minimum value of the Wk then we continue reading the files
                        if upper_bound > Wk.min():
                            terminate = False
                            break
                        else:
                            # Else ser the terminate value to True for termination
                            # The top k scores have been read so no need to continue
                            terminate = True

    print("Number of sequential accesses= ", counter)
    print("Top k objects:")
    Wk = Wk.sort()
    for tup in Wk:
        print(tup[0], ":", tup[1])


def brute_force(k, filename1, filename2):
    # Top-k objects
    Wk = MinHeap()

    # Create array R with the rnd.txt scores
    R_scores = read_scores('data/rnd.txt')

    # Start reading the files seq1.txt and seq2.txt alternately
    with open(filename1, 'r') as seq1, open(filename2, 'r') as seq2:
        # for seq1_object, seq2_object in zip(seq1, seq2):
        for seq1_object, seq2_object in zip(seq1, seq2):

            # Read seq1.txt
            seq1_value_id, seq1_value = seq1_object.split()
            seq1_value_id = int(seq1_value_id)
            seq1_value = round(float(seq1_value), 2)

            R_scores[seq1_value_id] += seq1_value

            if Wk.size() < k:
                Wk.push((seq1_value_id, round(R_scores[seq1_value_id], 2)))
            elif Wk.size() == k:
                if Wk.min() < R_scores[seq1_value_id]:
                    Wk.pop()
                    Wk.push((seq1_value_id, round(R_scores[seq1_value_id], 2)))

            # Read seq2.txt
            seq2_value_id, seq2_value = seq2_object.split()
            seq2_value_id = int(seq2_value_id)
            seq2_value = round(float(seq2_value), 2)

            R_scores[seq2_value_id] += seq2_value

            if Wk.size() < k:
                Wk.push((seq2_value_id, round(R_scores[seq2_value_id], 2)))
            elif Wk.size() == k:
                if Wk.min() < R_scores[seq2_value_id]:
                    Wk.pop()
                    Wk.push((seq2_value_id, round(R_scores[seq2_value_id], 2)))

    print("Brute Force")
    print("Top k objects:")
    Wk = Wk.sort()
    for tup in Wk:
        print(tup[0], ":", tup[1])


def main():
    # Create array R with the rnd.txt scores
    R = read_scores('data/rnd.txt')

    # Check the number of command line arguments
    if len(sys.argv) > 1:
        # Access the first command line argument
        k = sys.argv[1]
    else:
        print("Please provide a number for top-k.")

    while True:

        start = time.time()
        topK(int(k), R, 'data/seq1.txt', 'data/seq2.txt')
        end = time.time()
        final = round(end - start, 2)
        print("Time:", final, "ms")
        print("\n")

        # Perform brute force to check topK() method correctness
        brute_force(int(k), 'data/seq1.txt', 'data/seq2.txt')
        print()
        print("For exit press enter")

        print("Input k=", end="")
        k = input()

        if k == "":
            break


main()
