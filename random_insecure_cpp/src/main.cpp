#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <thread>

constexpr int MAX_RANGE = 32768;

class Random
{
public:
    int get_random_number()
    {
        return rand() % MAX_RANGE;
    }

    int get_seed()
    {
        return time_val;
    }
    Random()
    {
        this->time_val = 996;
        srand(time_val);
    }
    ~Random() {}

private:
    int time_val;
};

class BruteForce
{
public:
    std::atomic<int> found_seed;

    BruteForce(std::vector<int> &numbers, int start, int end) : numbers(numbers), start(start), end(end), found_seed(0) {}

    void guess(int start, int end)
    {
        for (int seed = start; seed <= end; seed++)
        {
            srand(seed);
            bool match = true;
            for (int i = 0; i < numbers.size(); i++)
            {
                if (rand() % MAX_RANGE != numbers[i])
                {
                    match = false;
                    break;
                }
            }
            if (match)
            {
                found_seed = seed;
                break;
            }
        }
    }

    void run()
    {
        std::vector<std::thread> threads;
        const int num_threads = std::thread::hardware_concurrency();
        int range = (end - start) / num_threads;
        for (int i = start; i <= end; i += range)
        {
            threads.emplace_back(&BruteForce::guess, this, i, i + range);
        }
        for (auto &thread : threads)
        {
            thread.join();
        }
    }

    BruteForce() {}
    ~BruteForce() {}

private:
    std::vector<int> numbers;
    int start, end;
};

int main()
{
    Random rand_gen;
    std::vector<int> random_numbers;

    for (auto i = 0; i < 1024; i++)
    {
        random_numbers.push_back(rand_gen.get_random_number());
    }

    std::cout << "Seed: " << rand_gen.get_seed() << std::endl;

    BruteForce bf(random_numbers, 0, MAX_RANGE);
    bf.run();

    if (bf.found_seed != 0)
    {
        std::cout << "Seed found: " << bf.found_seed << std::endl;
    }
    else
    {
        std::cout << "Seed not found" << std::endl;
    }
    return 0;

    return 0;
}
