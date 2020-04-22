#!/usr/bin/python
import decimal
import math
def ddG2activefold(ddG_value):
        '''
--------------------------------------------------------
'cal4activefold' is used to calculate the activity fold according to the ddG value
        usage: cal4acitivefold(ddG_value)
        input : ddG_value - the change of binding energy, decimal format.
        output: output - the activity improvement fold, a float number  
--------------------------------------------------------
'''
	if ddG_value != 'NA':                             #if not 'NA', calculate     
		decimal.getcontext().prec=5
	 	AF = math.exp(decimal.Decimal('-1.6675') * ddG_value)
	else:						  #if 'NA', return 'NA'
		AF = 'NA'

	return AF


if __name__ == '__main__':
	A = ddG2activefold(decimal.Decimal('0.803'))
	print A




def evaluate4level(AF_value):
        '''
--------------------------------------------------------
'evaluate4level' is used to evaluate the level of the activity improvement.
        usage: evaluate4level(AF_value)
        input : AF_value - the activity improvement fold, float format.
        output: output - the level, 0<Low<=1, 1<Middle<=100, High>100 
--------------------------------------------------------
'''
	if AF_value != 'NA':
		if AF_value > 0 and AF_value <= 1:
			Level = 'Low'
		elif AF_value > 1 and AF_value <= 100:
			Level = 'Middle'
		elif AF_value > 100:
			Level = 'High'
	else:
		Level = 'NA'     


	return Level


if __name__ == '__main__':
        B = evaluate4level('NA')
        print B
                         
