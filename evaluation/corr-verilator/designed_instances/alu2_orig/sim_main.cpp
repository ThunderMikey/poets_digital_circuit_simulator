#include "verilated.h"
#include <iostream>
#include "Valu2_orig.h"

#define ITERATION 1024

int main(){
  Valu2_orig* top = new Valu2_orig;
  for(unsigned i=0; i<ITERATION; i++){
    top->a = (i&(1<<0))>>0;
    top->b = (i&(1<<1))>>1;
    top->c = (i&(1<<2))>>2;
    top->d = (i&(1<<3))>>3;
    top->e = (i&(1<<4))>>4;
    top->f = (i&(1<<5))>>5;
    top->g = (i&(1<<6))>>6;
    top->h = (i&(1<<7))>>7;
    top->i = (i&(1<<8))>>8;
    top->j = (i&(1<<9))>>9;
    top->eval();
    unsigned re = 0;
    re |= ((top->k)&1)<<0;
    re |= ((top->l)&1)<<1;
    re |= ((top->m)&1)<<2;
    re |= ((top->n)&1)<<3;
    re |= ((top->o)&1)<<4;
    re |= ((top->p)&1)<<5;
    std::cout<<"input: "<<i
      <<", output: "<<re<<"\n";
  }
  delete top;
  return 0;
}
