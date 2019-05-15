#include <verilated.h>
#include <iostream>
#include "Vfulladder.h"

int main (int argc, char** argv, char** env){
  Verilated::commandArgs(argc, argv);
  Vfulladder* top = new Vfulladder;
  for(int i=0; i<8; i++){
    top->x = i & 1;
    top->y = i & 2;
    top->cin=i & 4;
    top->eval();
    std::cout<<"input: "<<int(top->x)
      <<", A: "<<int(top->A)
      <<", cout: "<<int(top->cout)<<"\n";
  }
  top->final();
  delete top;
  return 0;
}
