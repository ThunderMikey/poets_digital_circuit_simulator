#include "verilated.h"
#include <iostream>
#include "V6x1.h"

#define ITERATION 4096

int main(){
  V6x1* top = new V6x1;
  for(unsigned i=0; i<ITERATION; i++){
    top->in = i;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
  }
  return 0;
}
