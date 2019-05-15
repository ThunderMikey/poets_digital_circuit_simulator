#include "Vour.h"
#include "verilated.h"

int main (){
  Vour* top = new Vour;
  top->clk=1;
  while (!Verilated::gotFinish()) {
    top->clk = !top->clk;
    top->eval();
  }
  delete top;
  exit(0);
}
