#include "verilated.h"
#include <iostream>
#include "V1x1.h"

#define ITERATION 4

int main(){
  V1x1* top = new V1x1;
  for(unsigned i=0; i<ITERATION; i++){
    top->in = i;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
  }
  return 0;
}
