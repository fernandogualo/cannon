# -*- mode:python; coding:utf-8; tab-width:4 -*-

import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
import Cannon
import itertools
import math


def matrix_multiply(A, B):
    order = A.ncols
    C = Cannon.Matrix(order, [])

    for i, j in itertools.product(xrange(order), repeat=2):
        C.data.append(
            sum(A.data[i * order + k] * B.data[k * order + j] for k in xrange(order))
        )

    return C
    
def print_matrix(a):
	ncols=a.ncols
	nfils=len(a.data)/ncols
			
	for i in range(nfils):
		print(a.data[i*ncols:(i+1)*ncols])
		
    ############################## ENTREGA 2 ###############################################
def matrix_horizontal_shift(M, block_order):
    order = M.ncols    
    shift = 0 
    retval = Cannon.Matrix(order, [0] * order ** 2)
    i=0
	j=0
    while i<order:
    
        if i % block_order == 0 and i != 0:
            shift += block_order
        pos = order - shift

        for j in range(order):
            if pos == order:
                pos = 0

            retval.data[i*order + pos] = M.data[i*order + j]
            pos += 1
            j+=1
		i+=1
    return retval
    
def matrix_vertical_shift(M, block_order):
    order = M.ncols 
    shift = 0
    retval = Cannon.Matrix(order, [0] * order ** 2)    
    i=0
	j=0
    while i<order:
        if i % block_order == 0 and i != 0:
            shift += block_order
        pos = order - shift

        for j in range(order):        
			if pos == order:
                pos = 0

            retval.data[pos * order + i] = M.data[j * order + i]
            pos += 1
            j+=1
        i+=1
    return retval


def matrix_split(M, block_order):
    matriz_order = M.ncols
    fragments = (matriz_order / block_order) ** 2
    matriz_frag = None
    end = True
    fila_matriz = 0
    columna_matriz = 0    
    bloques = []

    while end:
        if columna_matriz == matriz_order:
			columna_matriz = 0
			fila_matriz += block_order

        if (columna_matriz % block_order) == 0:
            matriz_frag = Cannon.Matrix(block_order, [0] * (block_order ** 2))
            bloques.append(matriz_frag)
            frag_col = 0
		
        frag_fila = 0
		limit=fila_matriz + block_order
		i=fila_matriz
		        
        while i<limit:
            matriz_frag.data[block_order * frag_fila + frag_col] = M.data[matriz_order * i + columna_matriz]
            frag_fila += 1
			i+=1    
        columna_matriz += 1
        frag_col += 1
        
        if len(bloques) == fragments and columna_matriz == matriz_order:
            end = False

    return bloques
    
def list_split(lista,tam_sub):
	i=0
	list_sub=[]
	aux=0
	rango=len(lista)/tam_sub
	
	while i<rango:
		list_sub.append(lista[aux:aux+tam_sub])
		aux=aux+tam_sub
		i+=1
	return list_sub
	
#############################ENTREGA 3###########################################

def matrix_add(A, B):
    filsA = len(A.data) / A.ncols
    colsA = A.ncols    
    filsB = len(B.data) / B.ncols   
    colsB = B.ncols
    C = Cannon.Matrix(colsA, [0] * colsA * filsA)
    i=0
    
    for i in range(colsA * filsA):
        C.data[i] = A.data[i] + B.data[i]
		i+=1
		
    return C
 
def matrix_join(*blocks):
    tamano = 0
    fila = 0
    col = 0
	
    matriz_order = int(math.sqrt(len(blocks) *(blocks[0].ncols ** 2)))
    matrix_joined = Cannon.Matrix(matriz_order, [0] * (matriz_order ** 2))
    subMatrixOrder = blocks[0].ncols
    block_order=matriz_order / subMatrixOrder

    while tamano != matriz_order ** 2:
        if block_order == col:
            col = 0
            fila += 1
            
		col_aux = col * subMatrixOrder
        fila_aux = fila * subMatrixOrder        

        for matrix_fila in range(subMatrixOrder):        
            for matrix_column in range(subMatrixOrder):
                matrix_joined.data[(fila_aux + matrix_fila) * matriz_order + col_aux + matrix_column] = blocks[
                block_order * fila + col].data[matrix_fila * subMatrixOrder + matrix_column]
                tamano += 1        
        col += 1

    return matrix_joined
