/*
	genRand.c
		Testbed for generating a lot of randomw numbers
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void main()
{
	srand(time(NULL)); // Seed rand
	
	int aLen = 30;
	int rArr[aLen];
	int r = rand();	
	int smallerR = r / 4096;
	
	for (int i = 0; i < aLen; i++)
	{
		rArr[i] = (rand()) / 4096;
		printf("i: %d value: %d\n", i, rArr[i]);
	}
	
	

}
