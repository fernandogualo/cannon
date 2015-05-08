#!/usr/bin/python # -*- mode:python; coding:utf-8; tab-width:4 -*-

import sys
import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
import Cannon
from processor import ProcessorI
from frontend import FrontendI
from matrix_utils import matrix_multiply,print_matrix


class cliente(Ice.Application):
	def run(self, argv):
		prxFrontend = self.communicator().stringToProxy(argv[1])
		frontend = Cannon.FrontendPrx.checkedCast(prxFrontend)
		
        if not frontend:
                raise RuntimeError("Invalid proxy frontend")                
                
		A_last = 400 * 400
        A400 = Cannon.Matrix(400, range(1, 1 + A_last))
        B400 = Cannon.Matrix(400, range(1 + A_last, 1 + A_last * 2))

		res400=frontend.multiply(A400,B400)
		res400dir=matrix_multiply(A400,B400)

		if(res400 == res400dir):
			print("Ok en matrix 400x400")
			print_matrix(res400)
		else:
			print("Error en matrix 400x400")

		
		A_last = 600 * 600
        A600 = Cannon.Matrix(600, range(1, 1 + A_last))
        B600 = Cannon.Matrix(600, range(1 + A_last, 1 + A_last * 2))
        res600=frontend.multiply(A600,B600)
		res600dir=matrix_multiply(A600,B600)
		
		if(res600 == res600dir):
			print("Ok en matrix 600x600")
			print_matrix(res600)
		else:
			print("Error en matrix 600x600")
			
		A_last = 1000 * 1000
        A1000 = Cannon.Matrix(600, range(1, 1 + A_last))
        B1000 = Cannon.Matrix(600, range(1 + A_last, 1 + A_last * 2))
        res1000=frontend.multiply(A1000,B1000)
		res1000dir=matrix_multiply(A1000,B1000)
		
		if(res1000 == res1000dir):
			print("Ok en matrix 1000x1000")
			print_matrix(res1000)
		else:
			print("Error en matrix 1000x1000")
		  		
					
		return 0
		
		

        
if __name__ == '__main__':
    sys.exit(cliente().main(sys.argv))
