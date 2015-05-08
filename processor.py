#!/usr/bin/python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import sys
import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
import Services
import Cannon
from matrix_utils import matrix_multiply,matrix_add


class ProcessorI(Cannon.Processor):
    def init(self, index, order, above, left, target, current=None):
        self.resultado=None
		self.step_aux=0
        self.index=index
        self.order=order
        self.above=above
        self.left=left
        self.target=target
        self.matrixA={}
        self.matrixB={}               

    def injectA(self, A, step, current=None):
        self.matrixA[step]=A       
        if self.matrixB.has_key(step):
			self.matrix_check(step)
       
    def injectB(self, B, step, current=None):
        self.matrixB[step]=B        
		if self.matrixA.has_key(step):
			self.matrix_check(step)
            

    def matrix_check(self,step, current=None):
        current_A=self.matrixA[step]
		current_B=self.matrixB[step]
		order_auxiliar=self.order
		multiplicacion=matrix_multiply(current_A, current_B)
		
		self.step_aux += 1

		if self.step_aux == 1:
			self.resultado=multiplicacion

		if self.step_aux != 1:
			self.resultado=matrix_add(self.resultado,multiplicacion)
			
		if step < order_auxiliar-1:
			step += 1
			self.left.injectA(current_A, step)
        	self.above.injectB(current_B, step)
		
		if self.step_aux == order_auxiliar:
			self.target.inject(self.index,self.resultado)

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ProcessorI()

		proxyContainer = broker.stringToProxy(argv[1])
        container = Services.ContainerPrx.checkedCast(proxyContainer)

		if not container:
            raise RuntimeError('Proxy incorrecto')
            
        adapter = broker.createObjectAdapter('ProcessorAdapter')
        proxy = adapter.addWithUUID(servant)
        
        print('New processor ready: "{}"'.format(proxy))
        
        container.link(proxy.ice_getIdentity().name,proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        
        container.unlink(proxy.ice_getIdentity().name)
        
if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))

