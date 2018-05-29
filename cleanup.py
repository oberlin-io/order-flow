'''
Input order tracking csv
Output cleaned up 'orders.csv', from which other programs run on
'''

import raygun as rg


orders = rg.array('orders.csv')


# Append N to empty FHA attributes
for r in orders:

	if len(r) <= 9:
	
		orders[orders.index(r)].append('N')
		

rg.csv(orders, 'orders')

rg.hTable(orders, 'orders', True)	

