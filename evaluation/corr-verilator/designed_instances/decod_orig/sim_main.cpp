#include "verilated.h"
#include <iostream>
#include "Vdecod_orig.h"

#define ITERATION 32

int main(){
  Vdecod_orig* top = new Vdecod_orig;
  for(unsigned i=0; i<ITERATION; i++){
    top->a = (i&(1<<0))>>0;
    top->b = (i&(1<<1))>>1;
    top->c = (i&(1<<2))>>2;
    top->d = (i&(1<<3))>>3;
    top->e = (i&(1<<4))>>4;
    top->eval();
    unsigned re = 0;
    re |= ((top->f)&1)<<0;
    re |= ((top->g)&1)<<1;
    re |= ((top->h)&1)<<2;
    re |= ((top->i)&1)<<3;
    re |= ((top->j)&1)<<4;
    re |= ((top->k)&1)<<5;
    re |= ((top->l)&1)<<6;
    re |= ((top->m)&1)<<7;
    re |= ((top->n)&1)<<8;
    re |= ((top->o)&1)<<9;
    re |= ((top->p)&1)<<10;
    re |= ((top->q)&1)<<11;
    re |= ((top->r)&1)<<12;
    re |= ((top->s)&1)<<13;
    re |= ((top->t)&1)<<14;
    re |= ((top->u)&1)<<15;
    std::cout<<"input: "<<i
      <<", output: "<<re<<"\n";
  }
  delete top;
  return 0;
}
