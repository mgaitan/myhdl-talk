MyHDL, de Python al silicio
===========================

.. image::  img/Afiche.png
   :align: right

| por Martín Gaitán
|
| PyCon Argentina 2012
|
| https://mgaitan.github.com/
| @tin_nqn_


Quien soy
=========

- Martín Gaitán
- Ingeniero en Computación - UNC
- Hincha de Boca Jr.
- Python desde 2007, Django desde 2010, MyHDL un mes de 2011
- Creando Phasety y trabajando en Machinalis
- Feliz miembro de Python Argentina

El desafío
===========

* Gente que sabe de hardware pero no sabe Python (?)
* Gente que sabe de Python (mucho!) pero no de hardware
* Yo, argentino
* En una charla de 40 minutos

 .. image::  img/miedo.jpg
    :align: center


A modo de intro
===============

¿Dónde estamos?
---------------

.. image:: img/esta_aqui.jpg
   :align: right


Programar HW != diseñar HW
==========================

* Hw con funcionamiento y prestaciones predefinidas.
* Ejemplo: Arduino se programa sobre un uC que tiene un firmware.

* Bomba:

    Desde el diseño, el ASM es un lenguaje de *alto nivel*


Pero... ¿cómo se diseña un micro?
==================================


* Con ustedes los HDL (Hardware Description Language)

    Electrónica digital a través software

* VHDL y Verilog son los más típicos

.. class:: hide-title

.
=

¿Software? No era hardware?
---------------------------

FPGAs: Field Programmable Gates Array

.. epigraph::

     El camaleón mamá,
     el camaleón,
     cambia de colores
     según la ocasión...

     --  Chico Novarro

Por ejemplo
-----------

.. image:: img/fpga.jpg
   :align: center


Sólo para probar?
=================

* Originalmente sólo eran para prototipar.
* Ahora son baratas, se usan en producción!
* > escala, se fabrican chips `ASIC (Application-specific integrated circuit)`
* con (casi) el mismo HDL!


.. class:: hide-title

.
=

La burocracia
--------------

.. image:: img/flow.jpg
   :align: center

Contras
-------

- Muchos lenguajes
- Distintos equipos
- Alto nivel: Matlab
- RTL: System C, Verilog, VHDL
- Testing lento y malo


Un workflow pythonico
=====================

.. image:: img/flow-myhdl.png
   :align: center


.. class:: hide-title

.
=

Y qué corno es MyHDL ?
-----------------------

.. image:: img/myhdl_logo_256.png
   :align: center

Veamos
------

- Es un framework HDL en Python
- Incluye tipos de datos, helpers, conversores y simulador
- Permite unificar algoritmo, RTL y verificación en un mismo entorno!
- Convierte (con restricciones) a VHDL o Verilog sintetizable
- Permite cosimular Verilog (VHDL en desarrollo)
- Gratis y Libre (LGPL)
- Buena documentación y comunidad
- Y es Python, the glue language!

.. class:: hide-title

.
=

Ejemplo
--------

Un multiplexor de dos canales

.. image:: img/mux.png
   :align: center


VHDL
-----

The ugly way

.. class:: prettyprint lang-vhdl

::

    library ieee ;
    use ieee . std logic 1164 . all ;

    entity mux is
        port (
        a, b : in std logic vector (3 downto 0);
        s : in std logic ;
        o : out std logic vector (3 downto 0));
    end mux;
    architecture behavior of mux is
    begin behavior
        o <= a when s = '0' else b;
    end behavior

Contras
-------

- Requiere declarar la "entidad" (entradas y salidas) y comportamiento
- Tipado estático: requiere declarar tipo de entradas
- Verbósico
- Sintáxis horrible
- No ortogonal
- No hay testing fácil


.. class:: hide-title

.
=

Myhdl's way
------------

.. class:: prettyprint lang-python

::

    def mux(s, o, a, b):
        """
        2-channels N-bits multiplexor

        a, b: generic bits input channels
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

Pros
-----

- La entidad se determina por introspección (cuando se instancia)
- Python es dinámico ;-)
- *Simple is better than complex*

Expliquemos
============

* "módulo" (bloque) de HW => Función Python: ``mux``
* En una función interna se define el comportamiento: ``logic``
* Se decora con magia para ser un generador

Los generadores
===============

* Los generadores guardan un estado interno
* Esto permite la concurrencia y la simulación
* El decorador determina el tipo de sensibilidad. Predefinidos:

@always_comb
        cuando cambie cualquier señal de entrada
@always
        cuando cambie las que le indiquemos
@instance
        generador adhoc (se usa en testbench)


.. class:: hide-title

.
=

Bueno, enchufemos!
------------------

¿Y cómo echufamos?

Signal (a.k.a "cablecitos")

.. class:: prettyprint lang-python

::

     >>> bus = Signal(0)
     >>> bus.val
     0
     >>> bus.next = 1
     >>>

Pero ...
--------

El hardware es duro: tiene límites físicos
¿cuántos bits tiene ese bus?

.. class:: prettyprint lang-python

::

   >>> val = intbv(1, min=0, max=15)
   >>> len(val)
   4
   >>> bus = Signal(val)

Ahora sí, enchufemos!
=====================

Cómo ? Hagamos un *testbench*

.. class:: prettyprint lang-python

::

    def testBench():

    I0, I1 = [Signal(intbv(random.randint(0, 255))[32:]) for i in range(2)]
    O = Signal(intbv(0)[32:])
    S = Signal(intbv(0, min=0, max=2))

    mux_inst = mux (S, O, I0, I1)

    @instance
    def stimulus():
        header =  "%-6s|%-6s|%-6s|%-6s|%-6s" % ('time', 'I0', 'I1', 'S', 'O')
        print header + '\n' + '-' * len(header)
        while True:
            S.next = intbv(random.randint(0, 1))[1:]
            I0.next, I1.next = [intbv(random.randint(0, 255))[32:]
                                for i in range(2)]
            print "%-6s|%-6s|%-6s|%-6s|%-6s" % (now(), I0, I1, S, O)
            yield delay(5)

    return mux_inst, stimulus


Y simulemos
=============

.. class:: prettyprint lang-python

::

    sim = Simulation(testBench())
    sim.run(20)

- Simulation recibe como parámetros los "módulos"
- con el método run se ejecuta, indicando cuantos ciclos (timesteps) se correrá

Acá es cuando no funciona
=========================

Demo
-----

- en Ipython::

    %run run.py
    %run ejemplo1.py



El resultado
============

::


    time  |I0    |I1    |S     |O
    ----------------------------------
    0     |35    |96    |0     |0
    5     |164   |254   |1     |254
    10    |132   |60    |0     |132
    15    |32    |138   |0     |32
    20    |15    |112   |1     |112
    <class 'myhdl._SuspendSimulation'>: Simulated 20 timesteps

.. class:: hide-title

.
=

Pero entonces...
------------------

¿Se verifica con prints? Buuhh!

Un print sofisticado: generar formas de onda (*.vcd*)

.. class:: prettyprint lang-python

::

    tb_4_sim = traceSignals(testBench)
    sim = Simulation(tb_4_sim)
    sim.run(20)

Y se ven
---------

Con GTKWave (por ejemplo)

.. image:: img/vcd.png
 :align: center


Pero mejor es hacer test de verdad!
===================================

- Unittesting querido, el pueblo está contigo

.. class:: prettyprint lang-python

::

    class MuxTest(unittest.TestCase):

        def setUp(self):
            self.channels = [Signal(intbv(random.randint(0, 255))[32:]) for i in range(2)]
            self.O = Signal(intbv(0)[32:])
            self.S = Signal(intbv(0, min=0, max=2))
            self.mux_inst = mux(self.S, self.O, self.channels[0], self.channels[1])

        def test_starts_in_channel_0(self):
            yield delay(1)
            Simulation( self.mux_inst )
            self.assertEqual(self.channels[0].val, self.O.val)

        def test_channel_1_when_select_is_1(self):
            self.S.next = intbv(1)
            yield delay(1)
            Simulation( self.mux_inst )
            self.assertEqual(self.channels[1].val, self.O.val)



Convirtiendo pa'sintetizar
==========================

- A VHDL

.. class:: prettyprint lang-python

::

   mux_inst = toVHDL(mux, S, O, I0, I1)

- A Verilog

.. class:: prettyprint lang-python

::

   mux_inst = toVerilog(mux, S, O, I0, I1)


Un proyectito
=================

Para mi última materia: hice un procesador DLX/MIPS en 3 semanas

https://github.com/mgaitan/pymips

.. image:: img/dlx.png
   :align: center


Conclusiones
============


.. class:: fragment

- MyHDL es una opción seria

  - ... aunque su nombre no ayude a transmitirlo

.. class:: fragment

- Algoritmia, RTL, simulación y tests: Python FTW!

.. class:: fragment

- La inferencia de patrones para conversion es pura magia

.. class:: fragment

- Unittests (y TDD) => diseño de hardware ágil y bien

.. class:: fragment

- Y de nuevo: es **python** !

Preguntas ?
============

.. class:: prettyprint lang-python

::

    for p in preguntas:
        try:
            responder(p)
        except NiPutaIdea:
            sonreir_y_hacerse_el_gil()


La hora referí
===============

- Gracias, y vamo'a tomar un café


Esta y otras charlas están en...

|
| https://mgaitan.github.com/charlas.html


