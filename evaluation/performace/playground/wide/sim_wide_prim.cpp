#include "verilated.h"
#include <iostream>
#include "Vwide_prim.h"

int main(){
  Vwide_prim* top = new Vwide_prim;
  // 0-1 = 2^32-1
  for(unsigned i=0; i<-1; i++){
    top->in = i;
    top->eval();
    /*
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->out)<<"\n";
      */
  }
  return 0;
}
