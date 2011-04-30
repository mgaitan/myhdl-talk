#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import unittest
import random
from myhdl import Signal, delay, Simulation, intbv

from ejemplo1 import mux

# <demo> auto

class MuxTest(unittest.TestCase):
        
    def setUp(self):
        self.channels = [Signal(intbv(random.randint(0, 255))[32:]) for i in range(2)]
        self.O = Signal(intbv(0)[32:])
        self.S = Signal(intbv(0, min=0, max=2))
        self.mux_inst = mux(self.S, self.O, self.channels[0], self.channels[1])

# <demo> auto 

    def test_starts_in_channel_0(self):
        yield delay(1)
        Simulation( self.mux_inst )
        self.assertEqual(self.channels[0].val, self.O.val)  

    def test_channel_1_when_select_is_1(self):
        self.S.next = intbv(1)
        yield delay(1)
        Simulation( self.mux_inst )
        self.assertEqual(self.channels[1].val, self.O.val)  

# <demo> auto
  
if __name__ == '__main__':
    unittest.main()
