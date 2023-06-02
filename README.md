# Top-k Queries

This Python script implements the TopK algorithm for finding the top-k objects based on their scores. It reads scores from input files, calculates lower bounds and final scores for each object, and maintains a heap of top-k objects.

## Prerequisites

- Python 3.x

## Getting Started

1. Clone the repository:

 ```shell
 git clone <repository-url>
 ```
 
2. Install the required dependencies:
 ```shell
 pip install heapq
 ```
 
3. Place your input files in the data directory with the following names:

  + rnd.txt - contains scores for each object
  + seq1.txt - contains object IDs and scores
  + seq2.txt - contains object IDs and scores

## Usage
Run the script using the following command:
  ```shell
  python3 topk.py <k>
  ```
  Replace <k> with the desired value for k, which represents the number of top objects to retrieve. 
  The script will print the top-k objects along with their scores.
  
## Algorithm Overview

   1. Read the scores from the rnd.txt file and store them in an array.
   2. Initialize a heap (Wk) to store the top-k objects.
   3. Read object IDs and scores alternately from seq1.txt and seq2.txt.
   4. Calculate lower bounds and final scores for each object based on the scores from rnd.txt and the input files.
   5. Update the top-k heap (Wk) with the current object's ID and score if necessary.
   6. Check a threshold value based on the sum of the current object's score and 5.0.
   7. If the minimum lower bound in Wk is smaller than the threshold, continue reading the files. Otherwise, terminate the algorithm.
   8. Sort the Wk heap in descending order of scores and print the top-k objects.  
