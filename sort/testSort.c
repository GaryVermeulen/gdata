/*
	testSort.c	Testbed to test sorting algorithms
*/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void fillArray(int arr[], int size)
{
	printf("Start fillArray\n");
	
	for (int i = 0; i < size; i++)
	{
		arr[i] = (rand()) / 4096; // Make the random number some-what smaller
//		printf("i: %d value: %d\n", i, arr[i]);
	}
	printf("Fin fillArray\n");
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
  for (int i = 0; i < size; ++i) {
    printf("%d  ", array[i]);
  }
  printf("\n");
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

	start = clock();

	fillArray(rArrSm, aLenSmall);
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("rArrSm took: %f \n", cpu_time_used);
	
	start = clock();
	
	fillArray(rArrMd, aLenMed);
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("rArrMd took: %f \n", cpu_time_used);
	
	start = clock();
	
	fillArray(rArrLg, aLenLarge);
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("rArrLg took: %f \n\n", cpu_time_used);
	
//	printArray(rArrSm, aLenSmall);
	
	start = clock();
	
	MYqsort(rArrSm, 0, aLenSmall -1);	
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To sort rArrSm took: %f \n", cpu_time_used);	
//	printArray(rArrSm, aLenSmall);
	
	printf("\n");
	
//	printArray(rArrMd, aLenMed);
	
	start = clock();
	
	MYqsort(rArrMd, 0, aLenMed -1);	
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To sort rArrMd took: %f \n", cpu_time_used);	
//	printArray(rArrMd, aLenMed);
	
	printf("\n");
	
//	printArray(rArrLg, aLenLarge);
	
	start = clock();
	
	MYqsort(rArrLg, 0, aLenLarge -1);	
	
	end = clock();
	cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
	
	printf("To sort rArrLg took: %f \n", cpu_time_used);	
//	printArray(rArrLg, aLenLarge);
	
	
	printf("FIN\n");
}
