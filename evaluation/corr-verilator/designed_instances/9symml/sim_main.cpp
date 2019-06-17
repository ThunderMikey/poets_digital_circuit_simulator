#include "verilated.h"
#include <iostream>
#include "V9symml.h"

#define ITERATION 512

int main(){
  V9symml* top = new V9symml;
  for(unsigned i=0; i<ITERATION; i++){
    top->__031 = (i&(1<<0))>>0;
    top->__032 = (i&(1<<1))>>1;
    top->__033 = (i&(1<<2))>>2;
    top->__034 = (i&(1<<3))>>3;
    top->__035 = (i&(1<<4))>>4;
    top->__036 = (i&(1<<5))>>5;
    top->__037 = (i&(1<<6))>>6;
    top->__038 = (i&(1<<7))>>7;
    top->__039 = (i&(1<<8))>>8;
    top->eval();
    std::cout<<"input: "<<i
      <<", output: "<<unsigned(top->__0352)<<"\n";
  }
  delete top;
  return 0;
}
