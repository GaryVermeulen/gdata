#include <stdio.h>
#include <string.h>

#define MAX_LINE_LENGTH 4096

// char *simpfile = "C:\\GData\\C\\simpleton\\simpfile.txt";
char *simpfile = "/home/gary/src/c/simpleton/simpfile.txt";

int inData(char *filename, char *inword);

int main()
{
    char str1[100];
    char newString[10][10]; 
    int i,j,ctr;
	
    printf("\n\n I am Simpleton:\n");
    printf("---------------------------------------\n");    
 
    printf(" Input a word or phrase : ");
    fgets(str1, sizeof str1, stdin);	
	
	str1[strcspn(str1, "\n")] = 0; // Removes newline '\n'
 
    j=0; ctr=0;
    for(i=0;i<=(strlen(str1));i++)
    {
        // if space or NULL found, assign NULL into newString[ctr]
        if(str1[i]==' '||str1[i]=='\0')
        {
            newString[ctr][j]='\0';
            ctr++;  //for next word
            j=0;    //for next word, init index to 0
        }
        else
        {
            newString[ctr][j]=str1[i];
            j++;
        }
    }
    printf("\n You have entered %d words:\n", ctr);
    for(i=0;i < ctr;i++)
	{
        printf(" %s\n",newString[i]);
		
		// sudo code
		//if inData
		//	return meanings
		//else
		//	enter new meanings
		if(inData(simpfile, newString[i]))
		{
			printf("if inData...\n");
		}
		else
		{
			printf("else inData\n");
		}
		
		// TO DO
		// determine context from meanings
		//
		
	}
    return 0;
}

// sudo code => inData
// while not eof
//	if isWordMatch
//		build list of word meanings
// return
//
int inData(char *filename, char *inword)
{
	FILE *simpfp;
	char *mode = "a+";
	char buf[MAX_LINE_LENGTH] = {0};
	char delim[] = "[]{}";
	int foundIt = 0;
	int ismatch = -1;
	
	simpfp = fopen(filename, mode);
	
	if(simpfp == NULL) {
		fprintf(stderr, "Couldn't open file %s for reading or appending.\n", filename);
		return 0;
	}
	
	printf("   Looking for %s in %s\n", inword, filename);
	
	/* Go until the end of the file. */
	while(fgets(buf, MAX_LINE_LENGTH, simpfp) != NULL)
	{
		char *ptr = strtok(buf, delim);
		
		ismatch = strcmp(inword, ptr);
		
		if(ismatch == 0)
		{
			while(ptr != NULL)
			{
				printf("   '%s'\n", ptr);
				ptr = strtok(NULL, delim);
				foundIt = 1;
			}
		}
		else
		{
			printf("   Nope: %s no match %s\n", ptr, inword);
		}
	}
	fclose(simpfp);
	
	if(foundIt == 1)
		return 1;
	else
		return 0;
}
