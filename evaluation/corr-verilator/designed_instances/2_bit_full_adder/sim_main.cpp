#include <verilated.h>
#include <iostream>
#include "V2_bit_full_adder.h"

int main (int argc, char** argv, char** env){
  Verilated::commandArgs(argc, argv);
  V2_bit_full_adder* top = new V2_bit_full_adder;
  for(int i=0; i<8; i++){
    top->x = i & 1;
    top->y = (i & 2)>>1;
    top->cin=(i & 4)>>2;
    top->eval();
    unsigned output = 0;
    output |= top->A & 1;
    output |= (top->cout &1)<<1;
    std::cout<<"input: "<<unsigned(i)
      <<", output: "<<unsigned(output)<<"\n";
  }
  top->final();
  delete top;
  return 0;
}
