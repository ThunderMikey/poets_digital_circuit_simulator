#include "verilated.h"
#include <iostream>
#include "Vz4ml_orig.h"

#define ITERATION 128

int main(){
  Vz4ml_orig* top = new Vz4ml_orig;
  for(unsigned i=0; i<ITERATION; i++){
    top->__031 = (i&(1<<0))>>0;
    top->__032 = (i&(1<<1))>>1;
    top->__033 = (i&(1<<2))>>2;
    top->__034 = (i&(1<<3))>>3;
    top->__035 = (i&(1<<4))>>4;
    top->__036 = (i&(1<<5))>>5;
    top->__037 = (i&(1<<6))>>6;
    top->eval();
    unsigned re = 0;
    re |= ((top->__0324)&1)<<0;
    re |= ((top->__0325)&1)<<1;
    re |= ((top->__0326)&1)<<2;
    re |= ((top->__0327)&1)<<3;
    std::cout<<"input: "<<i
      <<", output: "<<re<<"\n";
  }
  delete top;
  return 0;
}
