/* quick1.c  
	Simple quick sort implmentation
*/
#include <stdio.h>

# define NELEMS(x)  (sizeof(x) / sizeof((x)[0]))

void qsort(int v[], int left, int right)
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
	qsort(v, left, last - 1);
	qsort(v, last + 1, right);
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
	int a[] = {4,78,33,2,53,24,67,22,9};
	size_t n = NELEMS(a);
	
	printf("Before sort:\n");
	printArray(a, n);
	
	qsort(a, 0, n -1);
	
	printf("After sort:\n");
	printArray(a, n);
	

}
