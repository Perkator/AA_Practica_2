#include <tbb/tbb.h>
#include <iostream>

void merge(int arr[], int left, int middle, int right) {
    // Calculate the sizes of the two subarrays to be merged
    int n1 = middle - left + 1;
    int n2 = right - middle;
    // Create temporary arrays to hold the left and right subarrays
    int* leftArr = new int[n1];
    int* rightArr = new int[n2];
    // Copy data to temporary arrays left and right
    for (int i = 0; i < n1; i++)
        leftArr[i] = arr[left + i];
    for (int j = 0; j < n2; j++)
        rightArr[j] = arr[middle + 1 + j];
    // Merge the two sorted subarrays back into the original array arr[]
    int i = 0; // Index of the left subarray
    int j = 0; // Index of the right subarray 
    int k = left; // Index of the merged subarray
    while (i < n1 && j < n2) {
        // Compare elements from both subarrays and merge them in order
        if (leftArr[i] <= rightArr[j]) {
            arr[k] = leftArr[i];
            i++;
        } else {
            arr[k] = rightArr[j];
            j++;
        }
        k++;
    }
    // Copy the elements of left
    while (i < n1) {
        arr[k] = leftArr[i];
        i++;
        k++;
    }
    // Copy the elements of right
    while (j < n2) {
        arr[k] = rightArr[j];
        j++;
        k++;
    }
}

// Parallel scan operation for calculating prefix sums
void parallelScan(int arr[], int left, int right, int temp[]) {
    tbb::parallel_scan(
        tbb::blocked_range<int>(left, right + 1), // range
        0, // id
        // body
        [&](const tbb::blocked_range<int>& r, int sum, bool is_final_scan) {
            int tmp = sum;
            for (int i = r.begin(); i < r.end(); ++i) {
                tmp += arr[i];
                if (is_final_scan)
                    temp[i] = tmp;
            }
            return tmp;
        },
        // reduce
        [](int left, int right) {
            return left + right;
        }
    );
}

// Parallel implementation of the merge sort algorithm
void parallelMergeSort(int arr[], int left, int right, int temp[]) {
    if (left < right) {
        int middle = left + (right - left) / 2;
        // Perform a parallel scan to calculate prefix sums
        parallelScan(arr, left, right, temp);
        // Parallelize the recursive calls to merge sort
        tbb::parallel_invoke(
            [&]() { parallelMergeSort(arr, left, middle, temp); },
            [&]() { parallelMergeSort(arr, middle + 1, right, temp); }
        );
        // Merge the two sorted halves of the array
        merge(arr, left, middle, right);
    }
}

int main() {
    const int n = 9;
    int arr[] = {14, 3, 4, 8, 7, 52, 1, 23, 67};
    int temp[n]; // Temporary array for storing prefix sums during scan
    // Call the parallel merge sort function
    parallelMergeSort(arr, 0, n - 1, temp);
    // Print the sorted array
    std::cout << "Sorted array: ";
    for (int i = 0; i < n; i++) {
        std::cout << arr[i] << " ";
    }
    return 0;
}