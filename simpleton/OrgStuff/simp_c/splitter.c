#include <stdio.h>
#include <string.h>

int main()
{
//	char str[] = "strtok [needs] {to be called several times to split a string}";
	char str[] = "apple[n]{the round fruit of a tree of the rose family, which typically has thin red or green skin and crisp flesh}";
	int init_size = strlen(str);
	char delim[] = "[]{}";

	char *ptr = strtok(str, delim);

	while(ptr != NULL)
	{
		printf("'%s'\n", ptr);
		ptr = strtok(NULL, delim);
	}

	/* This loop will show that there are zeroes in the str after tokenizing */
	for (int i = 0; i < init_size; i++)
	{
		printf("%d ", str[i]); /* Convert the character to integer, in this case
							   the character's ASCII equivalent */
	}
	printf("\n");

	return 0;
}