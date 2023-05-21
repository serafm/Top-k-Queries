import heapq
import sys

# Command-line argument for k
print("Input k=", end="")
k = int(input())

# Read rnd.txt and store object scores in R array
R = []
with open('data/rnd.txt', 'r') as rnd_file:
    for line in rnd_file:
        _, score = map(float, line.strip().split())
        R.append(score)

# Initialize variables and data structures
Wk = []
seen_objects = {}
serial_accesses = 0

# Function to update the top-k objects
def update_topk(object_id, score):
    # Check if object is already seen
    if object_id in seen_objects:
        # Calculate total score
        total_score = seen_objects[object_id] + score
        # Update the lower bound of the object's total score
        seen_objects[object_id] = total_score
        # Check if object is in Wk
        for i, (obj_score, obj_id) in enumerate(Wk):
            if obj_id == object_id:
                # Update the total score in Wk
                Wk[i] = (total_score, obj_id)
                heapq.heapify(Wk)
                break
    else:
        # Calculate the lower bound of the object's total score
        total_score = score + R[object_id]
        seen_objects[object_id] = total_score
        # Check if the object qualifies for Wk
        if len(Wk) < k:
            heapq.heappush(Wk, (total_score, object_id))
        elif total_score > Wk[0][0]:
            heapq.heapreplace(Wk, (total_score, object_id))

# Process seq1.txt and seq2.txt alternately
with open('data/seq1.txt', 'r') as seq1_file, open('data/seq2.txt', 'r') as seq2_file:
    while len(Wk) < k:
        # Read from seq1.txt
        line = seq1_file.readline()
        if not line:
            break  # seq1.txt is exhausted
        serial_accesses += 1
        object_id, score = map(float, line.strip().split())
        update_topk(int(object_id), score)

        # Read from seq2.txt
        line = seq2_file.readline()
        if not line:
            break  # seq2.txt is exhausted
        serial_accesses += 1
        object_id, score = map(float, line.strip().split())
        update_topk(int(object_id), score)

    # Continue reading until termination condition is met
    if len(Wk) == k:
        termination_score = Wk[0][0]
        while True:
            # Read from seq1.txt
            line = seq1_file.readline()
            if not line:
                break  # seq1.txt is exhausted
            serial_accesses += 1
            object_id, score = map(float, line.strip().split())
            if score + termination_score + 5.0 <= Wk[0][0]:
                break  # Terminate if termination condition is met
            update_topk(int(object_id), score)

            # Read from seq2.txt
            line = seq2_file.readline()
            if not line:
                break  # seq2.txt is exhausted
            serial_accesses += 1
            object_id, score = map(float, line.strip().split())
            if score + termination_score + 5.0 <= Wk[0][0]:
                break  # Terminate if termination condition is met
            update_topk(int(object_id), score)

# Sort the final Wk in descending order based on
print("Number of sequential accesses= ", serial_accesses)
print("Top k objects:")
Wk = sorted(Wk, reverse=True)
for id in Wk:
    print(id)
