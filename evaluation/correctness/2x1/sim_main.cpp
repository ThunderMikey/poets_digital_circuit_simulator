#include "verilated.h"
#include <iostream>
#include "V2x1.h"

#define ITERATION 16

int main(){
  V2x1* top = new V2x1;
  for(unsigned i=0; i<ITERATION; i++){
    top->in = i;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
  }
  return 0;
}
