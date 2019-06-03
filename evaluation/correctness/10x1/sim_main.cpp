#include "verilated.h"
#include <iostream>
#include "V10x1.h"

#define ITERATION 1048576

int main(){
  V10x1* top = new V10x1;
  for(unsigned i=0; i<ITERATION; i++){
    top->in = i;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
  }
  return 0;
}
