#include <tbb/tbb.h>
#include <iostream>
#include <vector>
#include <cmath>

// Function to find the maximum number in the array
int getMax(int arr[], int n) {
    int max = arr[0];
    for (int i = 1; i < n; i++)
        if (arr[i] > max)
            max = arr[i];
    return max;
}

// A utility function to do counting sort of arr[] according to
// the digit represented by exp.
void countSort(int arr[], int n, int exp) {
    const int range = 10;
    std::vector<int> output(n);
    int count[range] = {0};
    // Store count of occurrences in count[]
    for (int i = 0; i < n; i++)
        count[(arr[i] / exp) % 10]++;
    // Change count[i] so that count[i] contains actual
    // position of this digit in output[]
    for (int i = 1; i < range; i++)
        count[i] += count[i - 1];
    // Build the output array
    for (int i = n - 1; i >= 0; i--) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }
    // Copy the output array to arr[], so that arr[] now
    // contains sorted numbers according to the current digit
    for (int i = 0; i < n; i++)
        arr[i] = output[i];
}

// The main function to that sorts 'n' digits using Radix Sort
void radixSort(int arr[], int n) {
    // Find the maximum number to know the number of digits
    int max = getMax(arr, n);
    // Do counting sort for every digit
    for (int exp = 1; max / exp > 0; exp *= 10) {
        tbb::parallel_for(tbb::blocked_range<int>(0, n),
            [&](const tbb::blocked_range<int>& r) {
                for (int i = r.begin(); i != r.end(); ++i) {
                    countSort(arr, n, exp);
                }
            }
        );
    }
}

int main() {
    const int n = 9;
    int arr[] = {14, 3, 4, 8, 7, 52, 1, 23, 67};

    // Call the parallel RadixSort function
    radixSort(arr, n);

    // Print the sorted array
    std::cout << "Sorted array: ";
    for (int i = 0; i < n; i++) {
        std::cout << arr[i] << " ";
    }

    return 0;
}
