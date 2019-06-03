#include "verilated.h"
#include <iostream>
#include "V8x1.h"

#define ITERATION 65536

int main(){
  V8x1* top = new V8x1;
  for(unsigned i=0; i<ITERATION; i++){
    top->in = i;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
  }
  return 0;
}
