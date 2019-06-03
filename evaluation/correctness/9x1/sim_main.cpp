#include "verilated.h"
#include <iostream>
#include "V9x1.h"

#define ITERATION 262144

int main(){
  V9x1* top = new V9x1;
  for(unsigned i=0; i<ITERATION; i++){
    top->in = i;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
  }
  return 0;
}
