#include "verilated.h"
#include <iostream>
#include "Vmajority_orig.h"

#define ITERATION 32

int main(){
  Vmajority_orig* top = new Vmajority_orig;
  for(unsigned i=0; i<ITERATION; i++){
    top->a = (i&(1<<0))>>0;
    top->b = (i&(1<<1))>>1;
    top->c = (i&(1<<2))>>2;
    top->d = (i&(1<<3))>>3;
    top->e = (i&(1<<4))>>4;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->f)<<"\n";
  }
  delete top;
  return 0;
}
