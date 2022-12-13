/*
	testSort.c	Testbed to test sorting algorithms
*/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void fillArray(int arr[], int size)
{	
	for (int i = 0; i < size; i++)
		arr[i] = (rand()) / 4096; // Make the random number some-what smaller
}


void MYqsort(int v[], int left, int right)
{
	int i, last;
	void swap(int v[], int i, int j);
	
	if (left >= right)
		return;
		
	swap(v, left, (left + right)/2);
	last = left;
	
	for (i = left + 1; i <= right; i++)
		if (v[i] < v[left])
			swap(v , ++last, i);
	
	swap(v, left, last);
	MYqsort(v, left, last - 1);
	MYqsort(v, last + 1, right);
}


void swap(int v[], int i, int j)
{
	int temp;
	
	temp = v[i];
	v[i] = v[j];
	v[j] = temp;
}


void printArray(int array[], int size) {
	for (int i = 0; i < size; ++i)
		printf("%d  ", array[i]);

	printf("\n");
}


void bubbleSort(int arr[], int n)
{
	for (int i = 0; i < n- 1; ++i)
	{
		int Swap = 0;
		
		for (int x = 0; x < n - i - 1; ++x)
		{
			if (arr[x] > arr[x + 1])
			{
				int temp = arr[x];
				arr[x] = arr[x + 1];
				arr[x + 1] = temp;
				Swap = 1;
			}
		}
		
		if (Swap == 0)
			break;
	}
}


void swapP(int* a, int* b)
{
	int temp = *a;

	*a = *b;
	*b = temp;
}


void heapify(int arr[], int N, int i)
{
	// Find largest among root, left child and right child

	int largest = i;
	int left = 2 * i + 1;
	int right = 2 * i + 2;

	// If left child is larger than root
	if (left < N && arr[left] > arr[largest])
		largest = left;

	// If right child is larger than largest
	// so far
	if (right < N && arr[right] > arr[largest])
		largest = right;

	// Swap and continue heapifying if root is not largest
	// If largest is not root
	if (largest != i) 
	{
		swapP(&arr[i], &arr[largest]);

		// Recursively heapify the affected
		// sub-tree
		heapify(arr, N, largest);
	}
}


void heapSort(int arr[], int N)
{
	// Build max heap
	for (int i = N / 2 - 1; i >= 0; i--)
		heapify(arr, N, i);

	// Heap sort
	for (int i = N - 1; i >= 0; i--) 
	{
		swapP(&arr[0], &arr[i]);

		// Heapify root element to get highest element at
		// root again
		heapify(arr, i, 0);
	}
}



void main()
{
	srand(time(NULL)); // Seed rand
	
	int aLenSmall = 30;
	int aLenMed   = 3000;
	int aLenLarge = 300000;
	int rArrSm[aLenSmall];
	int rArrMd[aLenMed];
	int rArrLg[aLenLarge];
	
	clock_t start, end;
	double cpu_time_used;
	
	printf("Start\n");
	printf("Heap sort...\n");

	start = clock();

	fillArray(rArrSm, aLenSmall);
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To fill rArrSm took: %f \n", cpu_time_used);
	
	start = clock();
	
	fillArray(rArrMd, aLenMed);
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To fill rArrMd took: %f \n", cpu_time_used);
	
	start = clock();
	
	fillArray(rArrLg, aLenLarge);
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To fill rArrLg took: %f \n\n", cpu_time_used);
	
	start = clock();
	
	heapSort(rArrSm, aLenSmall);	
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To heap sort rArrSm took: %f \n", cpu_time_used);	
	
	start = clock();
	
	heapSort(rArrMd, aLenMed);	
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To heap sort rArrMd took: %f \n", cpu_time_used);	
	
	start = clock();
	
	heapSort(rArrLg, aLenLarge);	
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To heap sort rArrLg took: %f \n", cpu_time_used);	
	
	printf("\nQuick sort...\n");

	start = clock();

	fillArray(rArrSm, aLenSmall);
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To fill rArrSm took: %f \n", cpu_time_used);
	
	start = clock();
	
	fillArray(rArrMd, aLenMed);
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To fill rArrMd took: %f \n", cpu_time_used);
	
	start = clock();
	
	fillArray(rArrLg, aLenLarge);
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To fill rArrLg took: %f \n\n", cpu_time_used);
	
	start = clock();
	
	MYqsort(rArrSm, 0, aLenSmall -1);	
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To quick sort rArrSm took: %f \n", cpu_time_used);	
	
	start = clock();
	
	MYqsort(rArrMd, 0, aLenMed -1);	
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To quick sort rArrMd took: %f \n", cpu_time_used);	
	
	start = clock();
	
	MYqsort(rArrLg, 0, aLenLarge -1);	
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To quick sort rArrLg took: %f \n", cpu_time_used);	

	printf("\nBubble sort...\n");

	start = clock();

	fillArray(rArrSm, aLenSmall);
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To fill rArrSm took: %f \n", cpu_time_used);
	
	start = clock();
	
	fillArray(rArrMd, aLenMed);
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To fill rArrMd took: %f \n", cpu_time_used);
	
	start = clock();
	
	fillArray(rArrLg, aLenLarge);
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To fill rArrLg took: %f \n\n", cpu_time_used);
	
	start = clock();
	
	bubbleSort(rArrSm, aLenSmall);	
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To bubble sort rArrSm took: %f \n", cpu_time_used);	
	
	start = clock();
	
	bubbleSort(rArrMd, aLenMed);	
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To bubble sort rArrMd took: %f \n", cpu_time_used);	
	
	start = clock();
	
	bubbleSort(rArrLg, aLenLarge);	
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To bubble sort rArrLg took: %f \n", cpu_time_used);	
	
	printf("FIN\n");
}
