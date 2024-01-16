#include <tbb/tbb.h>
#include <iostream>

// Function to swap two elements
void swap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

// Partition function for QuickSort
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }

    swap(arr[i + 1], arr[high]);
    return i + 1;
}

// Parallel QuickSort function
void parallelQuickSort(int arr[], int low, int high) {
    // If the array has more than one element
    if (low < high) {
        // Partition the array and get the pivot index
        int pi = partition(arr, low, high);

        // Recursively sort the two subarrays in parallel
        tbb::parallel_invoke(
            [&]() { parallelQuickSort(arr, low, pi - 1); },
            [&]() { parallelQuickSort(arr, pi + 1, high); }
        );
    }
}

int main() {
    const int n = 9;
    int arr[] = {14, 3, 4, 8, 7, 52, 1, 23, 67};

    // Call the parallel QuickSort function
    parallelQuickSort(arr, 0, n - 1);

    // Print the sorted array
    std::cout << "Sorted array: ";
    for (int i = 0; i < n; i++) {
        std::cout << arr[i] << " ";
    }

    return 0;
}
