# -*- mode:python; coding:utf-8; tab-width:4 -*-

from unittest import TestCase

from doublex import assert_that, Spy, called, ANY_ARG

import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
import Cannon

from processor import ProcessorI

from common import M1, M2,M6


class ProcessorServantTests(TestCase):
    """
    These are NOT remote tests. We directly instantiate servants here.
    """
    def test_processors_1x1_block(self):
        # given
        P0 = ProcessorI()
        collector = Spy()

        A = M1(2)
        B = M1(5)
        C = M1(10)

        # when
        P0.init(0, 1, None, None, collector)
        P0.injectA(A, 0)
        P0.injectB(B, 0)

        # then
        assert_that(collector.inject, called().with_args(0, C, ANY_ARG))

    def test_processors_2x2_block(self):
        # given
        P0 = ProcessorI()
        collector = Spy()

        A = M2(1, 2,
               3, 4)
        B = M2(5, 6,
               7, 8)
        C = M2(19, 22,
               43, 50)

        # when
        P0.init(0, 1, None, None, collector)
        P0.injectA(A, 0)
        P0.injectB(B, 0)

        # then
        assert_that(collector.inject, called().with_args(0, C, ANY_ARG))


	def test_processors_0_block(self):
        # given
        P0 = ProcessorI()
        collector = Spy()

        A = M2(1, 2,
               3, 4)
        B = M2(0, 0,
               0, 0)
        C = M2(0, 0,
               0, 0)

        # when
        P0.init(0, 1, None, None, collector)
        P0.injectA(A, 0)
        P0.injectB(B, 0)

        # then
        assert_that(collector.inject, called().with_args(0, C, ANY_ARG))


	def test_processors_negative_block(self):
        # given
        P0 = ProcessorI()
        collector = Spy()

        A = M2(-1, 2,
               3, 4)
        B = M2(5, -6,
               -999, 3)
        C = M2(-2003, 12,
               -3981, -6)

        # when
        P0.init(0, 1, None, None, collector)
        P0.injectA(A, 0)
        P0.injectB(B, 0)

        # then
        assert_that(collector.inject, called().with_args(0, C, ANY_ARG))

	def test_processors_6x6_block(self):
        # given
        P0 = ProcessorI()
        collector = Spy()

        A = M6( 1 ,2 ,3 ,4 ,5 ,6  	
		,7 ,8 ,9 ,10 ,11 ,12  
		,13 ,14 ,15 ,16 ,17 ,18  
		,19 ,20 ,21 ,22 ,23 ,24  
		,25 ,26 ,27 ,28 ,29 ,30  
		,31 ,32 ,33 ,34 ,35,36 )
        
        B = M6(36 ,35 ,34 ,33 ,32 ,31  	
		,30 ,29 ,28 ,27 ,26 ,25  
		,24 ,23 ,22 ,21 ,20 ,19  
		,18 ,17 ,16 ,15 ,14 ,13  
		,12 ,11 ,10 ,9 ,8 ,7  
		,6 ,5 ,4 ,3 ,2 ,1  )

        C = M6(336 ,315 ,294 ,273 ,252 ,231 	
		,1092 ,1035 ,978 ,921 ,864 ,807 
		,1848 ,1755 ,1662 ,1569 ,1476 ,1383 
		,2604 ,2475 ,2346 ,2217 ,2088 ,1959 
		,3360 ,3195 ,3030 ,2865 ,2700 ,2535 
		,4116 ,3915 ,3714 ,3513 ,3312 ,3111)

        # when
        P0.init(0, 1, None, None, collector)
        P0.injectA(A, 0)
        P0.injectB(B, 0)

        # then
        assert_that(collector.inject, called().with_args(0, C, ANY_ARG))
