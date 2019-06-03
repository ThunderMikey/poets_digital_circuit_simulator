#include "verilated.h"
#include <iostream>
#include "V3x1.h"

#define ITERATION 64

int main(){
  V3x1* top = new V3x1;
  for(unsigned i=0; i<ITERATION; i++){
    top->in = i;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
  }
  return 0;
}
