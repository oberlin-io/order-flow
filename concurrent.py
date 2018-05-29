import raygun as rg
import datetime as dt

#!! Run cleanup.py first

orders = rg.array('orders.csv')


### Number orders concurrent for each order
for r in orders:
	
	# Exclude header
	if orders.index(r) != 0:
	
		# Exclude those orders not completed
		if r[orders[0].index('Completed')] != '':
		
			ord_date = dt.datetime.strptime(r[orders[0].index('Ordered')], "%Y-%m-%d")
			
			com_date = dt.datetime.strptime(r[orders[0].index('Completed')], "%Y-%m-%d")
			
			# Set concurrent counter
			conc = 0
				
			# Compare ordered and completed dates with all orders
			for row in orders:
			
				if orders.index(row) != 0:
			
					ord_date_ = dt.datetime.strptime(row[orders[0].index('Ordered')], "%Y-%m-%d")
					
					# Cases in which comparison orders are completed
					if row[orders[0].index('Completed')] != '':
					
						com_date_ = dt.datetime.strptime(row[orders[0].index('Completed')], "%Y-%m-%d")
					
						# If the comparison order's ordered date_ is eq/greater than order's
						# and eq/less than the order's completed date,
						# then add 1 to concurrent tally
						#if ord_date >= ord_date_ <= com_date:
						
						if ord_date_ <= com_date:
						
							if com_date_ >= ord_date:
							
								conc += 1
								#print row
								
							else:
								pass
						
						else:
							pass
					
					# Cases in which orders are not completed (ie, no colmpleted date, currently active)
					else:
						
						if ord_date_ <= com_date:
						
							conc += 1
							#print row
						
						else:
							pass
					
				else:
					pass
			
			# Add number concurrent to the order's row
			orders[orders.index(r)].append(conc)
	
		else:
		
			orders[orders.index(r)].append('NA')
	
	# Add feature to header row
	else:
		
		orders[orders.index(r)].append('Concurrent')
	
			
	#print '\n'
	
	
rg.hTable(orders, 'concurrent', True)			
	
	
d = raw_input('')