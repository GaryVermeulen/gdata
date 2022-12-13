/* obub.c
	Optimized Implementation of Bubble Sort
*/
#include <stdio.h>

# define NELEMS(x)  (sizeof(x) / sizeof((x)[0]))

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
		{
			break;
		}
	}
}

void printArray(int arr[], int n)
{
	for (int x = 0; x < n; ++x)
	{
		printf("%d ", arr[x]);
	}
	printf("\n");
}

void main()
{
	int data [] = {72, 31, 108, 39, 40, 2, 61, 22};
	size_t n = NELEMS(data);
	
	printf("Before sort:\n");
	printArray(data, n);
	bubbleSort(data, n);
	printf("After sort:\n");
	printArray(data, n);
}
