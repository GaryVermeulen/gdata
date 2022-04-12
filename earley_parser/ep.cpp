#include <fstream>
#include <iostream>
#include <string>
 
#include "grammar.hpp"
#include "earley.hpp"
 
int main()
{
//    std::string filename = "earley.dat";
	std::string filename = "simp2x.cfg";
//    std::string filename = "simp.cfg";
    std::ifstream ifs(filename);
    if (ifs) {
        MB::grammar grammar(ifs);
//        std::string sentence[] = {"John", "called", "Mary", "from", "Denver"};
		std::string sentence[] = {"Mary", "walked", "Pookie", "in", "the", "park"};
        const size_t len = sizeof(sentence) / sizeof(sentence[0]);
        bool success = MB::earley_parser(grammar).parse(sentence, sentence + len, std::cout);
        std::cout << "Success: " << std::boolalpha << success << '\n';
    }
    else {
        std::cerr << "Couldn't open " << filename << " for reading\n";
    }
}