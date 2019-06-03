#include "verilated.h"
#include <iostream>
#include "V7x1.h"

#define ITERATION 16384

int main(){
  V7x1* top = new V7x1;
  for(unsigned i=0; i<ITERATION; i++){
    top->in = i;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
  }
  return 0;
}
