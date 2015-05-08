#!/usr/bin/python -u 
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import sys
import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
import Cannon
import threading
import math
import Services
from matrix_utils import (matrix_horizontal_shift,
                          matrix_vertical_shift,
                          matrix_split, matrix_join)


class FrontendI(Cannon.Frontend):
    def __init__(self, processors):
		self.processors = processors
		self.proxyCollector = None
		self.collector=None

    def multiply(self, A, B, current=None):
		self.crear_collector(current.adapter)
				
		self.init_processors()
        self.load_processors(A, B)                
        resultado=self.collector.get_result()       
        
        self.destruir_collector(current.adapter)            
		return resultado
		
	def destruir_collector(self,adapter):
    	adapter.remove(self.proxyCollector.ice_getIdentity())
    	self.collector = None
    	self.proxyCollector= None
    	

	def crear_collector(self,adapter):
    	lenth_processors=len(self.processors)
    	order = int(math.sqrt(lenth_processors))
    	self.collector = CollectorI(order)
    	proxy = adapter.addWithUUID(self.collector)
    	self.proxyCollector = Cannon.CollectorPrx.checkedCast(proxy)    	
	
    def init_processors(self):
		nprocs = len(self.processors)
    	order = int(math.sqrt(nprocs))
    	i=0
    	
    	while i < nprocs:
        	fil = i / order
        	col = i % order        	
        	index=i
        	above =  - order

        	if  fil == 0:
        		above += order ** 2 + col
        	if fil != 0:
        		above += order*fil + col
        	left = i - 1
        	if col == 0:
        		left += order
        	self.processors[i].init(index,order, self.processors[above], self.processors[left]  ,self.proxyCollector)
			i+=1
			
    def load_processors(self, A, B):
		nblocks=len(self.processors)		
		block_order = (int)(A.ncols / math.sqrt(nblocks))
			
    	A_shift = matrix_horizontal_shift(A, block_order)
    	B_shift = matrix_vertical_shift(B, block_order)

    	A_blocks = matrix_split(A_shift, block_order)
    	B_blocks = matrix_split(B_shift, block_order)

    	for i in range(nblocks):
    		self.processors[i].injectA(A_blocks[i],0)
    		self.processors[i].injectB(B_blocks[i],0)    		


class CollectorI(Cannon.Collector):
	
    def __init__(self, order):
		self.mutex= threading.Event()
		self.order=order
		self.nblocks=0
		self.blocks =[None] * (order **2)
		self.tiempo_maximo_espera=None
        

    def inject(self, index, block, current=None):
		
		self.blocks[index]=block
		self.nblocks+=1
		order_aux=self.order
		
		if self.nblocks == order_aux:
			self.mutex.set()
		
	def get_result(self):
		resultado = None
		blocks_limit=self.order**2
		self.mutex.wait(self.tiempo_maximo_espera)
    
		if self.nblocks == blocks_limit:
			resultado = matrix_join(*self.blocks)

		return resultado


class Server(Ice.Application):
    def run(self, argv):        
        broker = self.communicator()
        processors = []
        servant = FrontendI(processors)      
        adapter = broker.createObjectAdapter('FrontendAdapter')
        proxy = adapter.add(servant, broker.stringToIdentity("frontend"))
                
        proxyContainer = broker.stringToProxy(argv[1])
        container = Services.ContainerPrx.checkedCast(proxyContainer)

        if not container:
            raise RuntimeError('Proxy incorrecto')

        proxies=container.list()        
        
        for i in proxies.values():
            processors.append(Cannon.ProcessorPrx.checkedCast(i))

        print(proxy)
        print('found {} processors'.format(len(processors)))
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


if __name__ == '__main__':	
    sys.exit(Server().main(sys.argv))
