import raygun as rg
import datetime as dt		

#!! Run cleanup.py first

### Count orders active per day
# Active orders per date
# 'Univariate time series data analysis'?
# Need to clean orders data per old orders with no completion date

# Import orders table data
orders = rg.array('orders.csv')

def dateCheck(table, dat, count):
	'''
	Takes orders table, date in iteration, and count at 0
	Returns count of orders that overlap with date in iteration
	'''

	# Skip header row [0]
	for row in table[1:]:
		
			comp_ord = dt.datetime.strptime( row[table[0].index('Ordered')], "%Y-%m-%d" )
			
			if dat >= comp_ord:
			
				# Some orders are not completed, ie have no completed date
				if row[table[0].index('Completed')] != '':
				
					comp_com = dt.datetime.strptime( row[table[0].index('Completed')], "%Y-%m-%d" )
					
					if dat <= comp_com:
					
						# The comparison order overlaps the date, so count it
						count += 1
					
					else:
					
						# Comparison order was ordered before AND completed before date in iteration
						pass

				else:
				
						# Comparison order is currently active, ie has no completed date
						# and was ordered before our date in iteration
						count += 1
						
			else:
			
						# Comparison order was ordered after our date in iteration
						pass
						
	return count

						
						

per_d = []


# Create timeline range in days and daily dates
# Count how many orders are active during each date in timeline via function dateCheck()
for day in range(274):

	count = 0

	# Set first day date from orders data
	## Can edit this to start timeline from any date
	if day == 0:
	
		dat = dt.datetime.strptime( orders[1][orders[0].index('Ordered')], "%Y-%m-%d" )
		
		count = dateCheck(orders, dat, 0)
		
	# Other iterations, add day to start date
	else:
	
		dat += dt.timedelta(days=1)
		
		count = dateCheck(orders, dat, 0)
	
	# Append to per day table
	per_d.append([dat, count])


	
# Formatting the per_d table
for d in per_d:
	
	# Reformat datetime object to date
	per_d[per_d.index(d)][0] = dt.datetime.strftime(d[0],'%Y-%m-%d')

	
# Insert header row
per_d.insert(0,['Date','Active'])



# Ouput
	
rg.csv(per_d, 'active-per-day')

rg.hTable(per_d, 'active-per-day', True)	





