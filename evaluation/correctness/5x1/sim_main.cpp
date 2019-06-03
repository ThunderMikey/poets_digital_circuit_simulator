#include "verilated.h"
#include <iostream>
#include "V5x1.h"

#define ITERATION 1024

int main(){
  V5x1* top = new V5x1;
  for(unsigned i=0; i<ITERATION; i++){
    top->in = i;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
  }
  return 0;
}
