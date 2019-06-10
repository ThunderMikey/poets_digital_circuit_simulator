#include "verilated.h"
#include <iostream>
#include "VT_PROG.h"

#define ITERATION T_ITERATION

int main(){
  VT_PROG* top = new VT_PROG;
  for(unsigned i=0; i<ITERATION; i++){
    top->in = i;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
  }
  return 0;
}
