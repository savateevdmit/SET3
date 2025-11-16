#include <vector>
#include <random>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <fstream>
#include <iostream>

class ArrayGenerator {
    int max_size;
    const int value_range = 6000;
    std::mt19937 rng;

    std::vector<int> random_array;
    std::vector<int> reversed_array;
    std::vector<int> almost_sorted_array;

    void generateRandomArray() {
        random_array.resize(max_size);
        std::uniform_int_distribution<int> dist(0, value_range);
        for (int i = 0; i < max_size; ++i) {
            random_array[i] = dist(rng);
        }
    }

    void generateReversedArray() {
        reversed_array.resize(max_size);
        for (int i = 0; i < max_size; ++i) {
            reversed_array[i] = max_size - i;
        }
    }

    void generateAlmostSortedArray() {
        almost_sorted_array.resize(max_size);
        for (int i = 0; i < max_size; ++i) {
            almost_sorted_array[i] = i;
        }

        std::uniform_int_distribution<int> dist(0, max_size - 1);
        const int swaps = max_size / 100;
        for (int i = 0; i < swaps; ++i) {
            int idx1 = dist(rng);
            int idx2 = dist(rng);
            std::swap(almost_sorted_array[idx1], almost_sorted_array[idx2]);
        }
    };

public:
    explicit ArrayGenerator(int size)
        : max_size(size), rng(std::random_device{}()) {
        generateRandomArray();
        generateReversedArray();
        generateAlmostSortedArray();
    }

    std::vector<int> getRandomSubarray(int size) {
        return std::vector(random_array.begin(), random_array.begin() + size);
    }

    std::vector<int> getReversedSubarray(int size) {
        return std::vector(reversed_array.begin(), reversed_array.begin() + size);
    }

    std::vector<int> getAlmostSortedSubarray(int size) {
        return std::vector(almost_sorted_array.begin(), almost_sorted_array.begin() + size);
    }
};


class SortTester {
    const int NUM_RUNS = 5;

    // merge sort
    void merge(std::vector<int> &arr, int left, int mid, int right, std::vector<int> &temp) {
        int i = left;
        int j = mid + 1;
        int k = left;

        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) {
                temp[k++] = arr[i++];
            } else {
                temp[k++] = arr[j++];
            }
        }

        while (i <= mid) temp[k++] = arr[i++];
        while (j <= right) temp[k++] = arr[j++];

        for (i = left; i <= right; i++) arr[i] = temp[i];
    }

    void mergeSort(std::vector<int> &arr, int left, int right, std::vector<int> &temp) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            mergeSort(arr, left, mid, temp);
            mergeSort(arr, mid + 1, right, temp);
            merge(arr, left, mid, right, temp);
        }
    }

    // insertion Sort
    void insertionSort(std::vector<int> &arr, int left, int right) {
        for (int i = left + 1; i <= right; i++) {
            int key = arr[i];
            int j = i - 1;
            while (j >= left && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }

    // hybrid sort
    void hybridMergeSort(std::vector<int> &arr, int left, int right, std::vector<int> &temp, int threshold) {
        if (right - left + 1 <= threshold) {
            insertionSort(arr, left, right);
            return;
        }

        if (left < right) {
            int mid = left + (right - left) / 2;
            hybridMergeSort(arr, left, mid, temp, threshold);
            hybridMergeSort(arr, mid + 1, right, temp, threshold);
            merge(arr, left, mid, right, temp);
        }
    }

    long long measureStandard(std::vector<int> arr) {
        std::vector<int> temp(arr.size());
        auto start = std::chrono::high_resolution_clock::now();
        mergeSort(arr, 0, arr.size() - 1, temp);
        auto end = std::chrono::high_resolution_clock::now();
        return std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
    }

    long long measureHybrid(std::vector<int> arr, int threshold) {
        std::vector<int> temp(arr.size());
        auto start = std::chrono::high_resolution_clock::now();
        hybridMergeSort(arr, 0, arr.size() - 1, temp, threshold);
        auto end = std::chrono::high_resolution_clock::now();
        return std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
    }

public:
    void runExperiments(ArrayGenerator &generator, const std::vector<int> &sizes,
                        const std::vector<int> &thresholds) {

        std::ofstream file_standard;
        file_standard.open("../SET3/A2/standard_results.csv");

        std::ofstream file_hybrid;
        file_hybrid.open("../SET3/A2/hybrid_results.csv");

        file_standard << "size,type,time\n";
        file_hybrid << "size,type,threshold,time\n";

        const char *types[3] = {"random", "reversed", "almost_sorted"};

        for (int size: sizes) {
            std::cout << "size processing: " << size << std::endl;

            for (int type = 0; type < 3; type++) {
                std::vector<long long> times;
                for (int run = 0; run < NUM_RUNS; run++) {
                    std::vector<int> arr;
                    if (type == 0) arr = generator.getRandomSubarray(size);
                    else if (type == 1) arr = generator.getReversedSubarray(size);
                    else arr = generator.getAlmostSortedSubarray(size);

                    times.push_back(measureStandard(arr));
                }
                std::sort(times.begin(), times.end());
                long long median = times[NUM_RUNS / 2];
                file_standard << size << "," << types[type] << "," << median << "\n";
            }

            for (int threshold: thresholds) {
                for (int type = 0; type < 3; type++) {
                    std::vector<long long> times;
                    for (int run = 0; run < NUM_RUNS; run++) {
                        std::vector<int> arr;
                        if (type == 0) arr = generator.getRandomSubarray(size);
                        else if (type == 1) arr = generator.getReversedSubarray(size);
                        else arr = generator.getAlmostSortedSubarray(size);

                        times.push_back(measureHybrid(arr, threshold));
                    }
                    std::sort(times.begin(), times.end());
                    long long median = times[NUM_RUNS / 2];
                    file_hybrid << size << "," << types[type] << "," << threshold << "," << median << "\n";
                }
            }
        }

        file_standard.close();
        file_hybrid.close();
        std::cout << "save in A2" << std::endl;
    }
};

int main() {
    ArrayGenerator generator = ArrayGenerator(100000);


    std::vector<int> sizes;
    for (int size = 500; size <= 100000; size += 100) {
        sizes.push_back(size);
    }

    std::vector thresholds = {5, 10, 15, 20, 25, 30, 35, 40, 45, 50};

    SortTester tester;
    tester.runExperiments(generator, sizes, thresholds);

    return 0;
}
