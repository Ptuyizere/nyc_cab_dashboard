import random
import time

from parse_and_store import merge_sort

# timing function
def time_sort(sort_function, data):
    start = time.time()
    sort_function(data[:])
    end = time.time()
    elapsed = end - start
    return elapsed

# Main test
def run_tests():
    sizes = [1000, 2000, 4000, 8000, 16000, 32000, 64000]
    repeats = 3

    print("")
    print("Testing merge_sort performance on random lists...")
    print("")

    for n in sizes:
        total_time = 0.0
        print("Testing list size:", n)
        for r in range(repeats):
            # create dummy list of tuples 
            data = []
            for i in range(n):
                data.append((random.randint(-1000000, 1000000),))
            
            # time the sort
            elapsed = time_sort(merge_sort, data)

            print("  Run", r + 1, "time:", round(elapsed, 6), "seconds")
            total_time += elapsed

        average = total_time / repeats
        print("  Average time for size", n, ":", round(average, 6), "seconds")
        print("")

# Run the test
if __name__ == "__main__":
    random.seed(42)
    run_tests()