#include "verilated.h"
#include <iostream>
#include "Vf51m_orig.h"

#define ITERATION 256

int main(){
  Vf51m_orig* top = new Vf51m_orig;
  for(unsigned i=0; i<ITERATION; i++){
    top->__031 = (i&(1<<0))>>0;
    top->__032 = (i&(1<<1))>>1;
    top->__033 = (i&(1<<2))>>2;
    top->__034 = (i&(1<<3))>>3;
    top->__035 = (i&(1<<4))>>4;
    top->__036 = (i&(1<<5))>>5;
    top->__037 = (i&(1<<6))>>6;
    top->__038 = (i&(1<<7))>>7;
    top->eval();
    unsigned re = 0;
    re |= ((top->__0344)&1)<<0;
    re |= ((top->__0345)&1)<<1;
    re |= ((top->__0346)&1)<<2;
    re |= ((top->__0347)&1)<<3;
    re |= ((top->__0348)&1)<<4;
    re |= ((top->__0349)&1)<<5;
    re |= ((top->__0350)&1)<<6;
    re |= ((top->__0351)&1)<<7;
    std::cout<<"input: "<<i
      <<", output: "<<re<<"\n";
  }
  delete top;
  return 0;
}
