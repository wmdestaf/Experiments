#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>  //link with -lm

/**
	Prompt the user to enter a double variable greater than 0.
	On failure, repeat the prompt again, and re-scan the user.
	@param prompt The prompt to display
	@return the parsed double
*/
double get_double(char *prompt) {
	char *buf;
	size_t n;  
	double res;
	
	buf = NULL;
	
	do {
		free(buf), buf = NULL; //ok to do, as free(NULL) is a NOP by ISO
		printf("%s",prompt);
		getline(&buf,&n,stdin);
		if(sscanf(buf,"%lf",&res) != 1) res = 0;
	} while(res <= 0);
	
	free(buf);
	return res;
}

/**
	Computes heron's formula on three double triangle side lengths
	@param a The first  side
	@param b The second side
	@param c The third  side
	@return The area of the represented triangle
*/
double heron(double a, double b, double c) {
	double s, A;
	s = (a + b + c) / 2.0;
	A = s * (s-a) * (s-b) * (s-c);
	return sqrt(s);
}

/**
	Driver program. Supports either 3 arguments (automatic computation,
	return EXIT_FAILURE on failure to parse args), or no arguments,
	after which the arguments should be presented interactively.
	@param argc arg count
	@param argv arg array
*/
int main(int argc, char **argv) {
	if(argc == 4) { //non-interactive
		double a, b, c;
		if(!(a=atof(argv[1]))) return EXIT_FAILURE;
		if(!(b=atof(argv[2]))) return EXIT_FAILURE;
		if(!(c=atof(argv[3]))) return EXIT_FAILURE;
		
		printf("%.5lf\n",heron(a,b,c));
	}
	else if(argc == 1) { //interactive
		double a, b, c, s, A;
		a = get_double("Side 1: ");
		b = get_double("Side 2: ");
		c = get_double("Side 3: ");
		printf("%.5lf\n",heron(a,b,c));
		
		printf("Press any key to continue . . .");
		getchar();
	}
	else 
		fprintf(stderr,"%s\n","usage: heron\nusage: heron side1 side2 side3");
		return EXIT_FAILURE;
	
	return EXIT_SUCCESS;
}