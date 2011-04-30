#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# <demo> auto

from myhdl import Signal, delay, always_comb, always, Simulation, \
                  intbv, bin, instance, now, toVHDL, toVerilog, traceSignals
import random

# <demo> auto

def mux(s, o, a, b):
    """
    2-channels N-bits multiplexor

    a, b: generic bits input vectors
    o: output vector
    s: channel selector
    """
    @always_comb
    def logic():
        if s == 0:
            o.next = a
        else:
            o.next = b
    return logic

# <demo> stop

def testBench():

    I0, I1 = [Signal(intbv(random.randint(0, 255))[32:]) for i in range(2)]
    O = Signal(intbv(0)[32:])
    S = Signal(intbv(0, min=0, max=2))
   
    mux_inst = mux (S, O, I0, I1)
 
    @instance
    def stimulus():
        while True:
            S.next = intbv(random.randint(0, 1))[1:]
            I0.next, I1.next = [intbv(random.randint(0, 255))[32:] for i in range(2)]
            print "%s: Inputs: %i %i | S: %i | Output: %i" % (now(), I0, I1, S, O)
            yield delay(5)

    return mux_inst, stimulus

# <demo> demo

if __name__ == '__main__':
    tb_4_sim = testBench()
    sim = Simulation(tb_4_sim)
    sim.run(20)


