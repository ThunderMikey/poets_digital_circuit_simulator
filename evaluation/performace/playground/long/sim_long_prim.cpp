#include "verilated.h"
#include <iostream>
#include "Vlong_prim.h"

#define ITERATION 16

int main(){
  Vlong_prim* top = new Vlong_prim;
  for(unsigned i=0; i<ITERATION; i++){
    top->in = i;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
  }
  return 0;
}
