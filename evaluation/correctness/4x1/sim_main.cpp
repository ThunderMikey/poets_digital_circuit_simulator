#include "verilated.h"
#include <iostream>
#include "V4x1.h"

#define ITERATION 256

int main(){
  V4x1* top = new V4x1;
  for(unsigned i=0; i<ITERATION; i++){
    top->in = i;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
  }
  return 0;
}
