import random
import threading

MAX_RANGE = 32768

class Random:
    def __init__(self):
        self.time_val = 996
        random.seed(self.time_val)

    def get_random_number(self):
        return random.randint(0, MAX_RANGE)

    def get_seed(self):
        return self.time_val


class BruteForce:
    def __init__(self, numbers, start, end):
        self.numbers = numbers
        self.start = start
        self.end = end
        self.found_seed = 0

    def guess(self, start, end):
        for seed in range(start, end):
            random.seed(seed)
            match = True
            for i in range(len(self.numbers)):
                if random.randint(0, MAX_RANGE) != self.numbers[i]:
                    match = False
                    break
            if match:
                self.found_seed = seed
                break

    def run(self):
        threads = []
        num_threads = threading.activeCount()
        ourrange = (self.end - self.start) // num_threads
        for i in range(self.start, self.end, ourrange):
            t = threading.Thread(target=self.guess, args=(i, i+ourrange))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()


if __name__ == "__main__":
    rand_gen = Random()
    random_numbers = []

    for i in range(1024):
        random_numbers.append(rand_gen.get_random_number())

    print("Seed: ", rand_gen.get_seed())

    bf = BruteForce(random_numbers, 0, MAX_RANGE)
    bf.run()

    if bf.found_seed != 0:
        print("Seed found: ", bf.found_seed)
    else:
        print("Seed not found")
