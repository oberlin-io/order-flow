#!/usr/bin/python


print '''Content-type: text/html

<html>
'''

print '''<head>
	<title>DB Processing</title>
	<link href="https://fonts.googleapis.com/css?family=Aldrich|Bungee" rel="stylesheet">
	<style>
		body {
			background-color: #000;
			color: #fff;
			font-family: 'Aldrich', sans-serif;
			opacity: .25;
		}
		h1 {
			font-family: 'Bungee', sans-serif;
		}
	</style>
</head>
<h1>Database Processing</h1>'''




### IMPORT LIBS ###

import os
import raygun as rg
import datetime as dt
from cookielib import CookieJar
from urllib2 import build_opener, HTTPCookieProcessor




### GET SOURCE DATA ###

opener = build_opener(HTTPCookieProcessor(CookieJar()))

# OAS Order Tracking
resp = opener.open('https://docs.google.com/spreadsheet/ccc?key=1mL8_Hew8NkZevZvi-MdASqARb-q-MkJUE9zSQD7BcRc&output=csv')

# Copy of Order Tracking
#resp = opener.open('https://docs.google.com/spreadsheet/ccc?key=1xLFwiAKP8GB45swIG2L1doMUPlCAbYpdLOvN09Oc-40&output=csv')

data = resp.read()


#with open('data.csv', 'w') as f:
#	f.write(data)

print '<p>Obtained source CSV data from Google Sheets.'




### PARSE CSV TO 2D ARRAY ###

table = []

for line in data.splitlines():

	if line != '':

		row = []

		rg.parse(line, row)

		table.append(row)

print '<p>Parsed CSV data to 2D array.'




### SCRUB DATA ###

# Remove canceled records
pack_dx = table[0].index('Packet')
rem = 0

for r in table[1:]:	

	if r[pack_dx] == 'Canc':
	
		table.remove(r)
		rem += 1
		
	else:
		pass

print "<p>Orders marked as 'Canc' removed: %s" % rem


# Remove records of orders done by other appraisers.
appr_dx = table[0].index('Appr')
rem = 0

for r in table[1:]:	

	if r[appr_dx] != '':
	
		# Just in case there's a space
		if r[appr_dx] != ' ':
	
			table.remove(r)
			rem += 1
		
		else:
			pass
	else:
		pass
		
print '<p>Orders assigned to other appraisers removed: %s' % rem




### CALCULATE ORDERS ACTIVE PER DAY ###

print '<br><h3>Calculating Orders Per Day</h3>'

# Additional scrub, removing orders without Ordered field
ord_dx = table[0].index('Ordered')
rem = 0

for r in table[1:]:

	if r[ord_dx] == '':
	
		table.remove(r)
		rem += 1
		
print '<p>Orders removed due to empty Ordered field: %s' % rem


# Calculate the range of days from earliest Ordered entry, ie minimum, to today
def min_max(table, lookup_feat, minORmax, attribORrow):
	'''
	FROM RAYGUN. ALTERED FOR DATETIME OBJECTS
	
	Returns minimum or maximum value of column. Excludes row 0 (header row).
	
	table: some 2D array
	lookup_feat: feature of attributes to compare
	minORmax: to return min, set to 0, or max = 1
	attribORrow: to return the attribute, set to 0, or row as arrway = 1
	'''

	if lookup_feat in table[0]:
	
		lookup_dx = table[0].index(lookup_feat)
		
		# Find minimum
		if minORmax == 0:
		
			# Set the variable
			min_val = ''
		
			for row in table[1:]:
			
				# Set min to the first iterable
				if min_val == '':
				
					min_val = dt.datetime.strptime(row[lookup_dx], "%a, %b %d, %Y" )
					
					min_row = row
				
				else:
				
					if min_val > dt.datetime.strptime(row[lookup_dx], "%a, %b %d, %Y" ):
					
						min_val = dt.datetime.strptime(row[lookup_dx], "%a, %b %d, %Y" )
				
						min_row = row
			
			# Return value only
			if attribORrow == 0:
			
				return min_val
			
			# Or return entire row as an array
			else:
			
				return min_row

		else:
		
			# Set the variable
			max_val = ''
		
			for row in table[1:]:
				
				# Set max to the first iterable
				if max_val == '':
				
					max_val = dt.datetime.strptime(row[lookup_dx], "%a, %b %d, %Y" )
					
					max_row = row
				
				else:
				
					if max_val < dt.datetime.strptime(row[lookup_dx], "%a, %b %d, %Y" ):
					
						max_val = dt.datetime.strptime(row[lookup_dx], "%a, %b %d, %Y" )
				
						max_row = row
			
			# Return value only
			if attribORrow == 0:
			
				return max_val
			
			# Or return entire row as an array
			else:
			
				return max_row

	else:
	
		print '<p>Error: \"' + lookup_feat + '\" is not a feature.'
		
		return ''
	

earliest = min_max(table, 'Ordered', 0, 0)

print '<p>Earliest Ordered date found: %s' % earliest

today = dt.datetime.today()

print '<p>Today\'s date: %s' % today

# Should 1 day be added (or even +2?). Run db-process and check final entry on active-per-day.csv. It should be today's date.
d_range = (today - earliest).days

print '<p>Range of days processing: %s' % d_range


# Per date, count number of orders that are active during date
def dateCheck(table, dat, count):
	'''
	Takes orders table, date in iteration, and count at 0
	Returns count of orders that overlap with date in iteration
	'''

	# Skip header row [0]
	for row in table[1:]:
		
		list = [] # For printing checking only
		
		comp_ord = dt.datetime.strptime( row[table[0].index('Ordered')], "%a, %b %d, %Y" )
		
		if dat >= comp_ord:
		
			# Some orders are not completed, ie have no completed date
			if row[table[0].index('Completed')] != '':
			
				comp_com = dt.datetime.strptime( row[table[0].index('Completed')], "%a, %b %d, %Y" )
				
				if dat <= comp_com:
				
					# The comparison order overlaps the date, so count it
					count += 1
					list.append(row)
				
				else:
				
					# Comparison order was ordered before AND completed before date in iteration
					pass

			else:
			
					# Comparison order is currently active, ie has no completed date
					# and was ordered before our date in iteration
					count += 1
					list.append(row)
					
		else:
		
					# Comparison order was ordered after our date in iteration
					pass
	
	return count


# Set per day table
per_d = []

# Run dateCheck() to count active for each day
for day in range(d_range):

	count = 0

	# Set first day date as the earliest dat in data
	if day == 0:
	
		dat = earliest
		count = dateCheck(table, dat, 0)
		
	# For rest of iterations, add day to start date
	else:
	
		dat += dt.timedelta(days=1)
		count = dateCheck(table, dat, 0)
	
	# Reformat datetime object to string
	ref_dat = dt.datetime.strftime(dat,'%a, %b %d, %Y')
	
	per_d.append([ref_dat, count])


# Get average Active, and splice out dates until reach average
# (because the first few days do not count orders from before start date, showing 1 or 2 active, which is inaccurate)
sum = 0.0
for r in per_d:
	sum += r[1]

avg = sum / float(len(per_d))

print '<p>Average active per day: %s' % avg

for r in per_d:
	if r[1] >= avg:
		per_d = per_d[per_d.index(r):]
		break

# Insert header row
per_d.insert(0,['Date','Active'])


# Write ouput to CSV file
# For online
#rg.csv(per_d, '/home1/joberlin/public_html/active-per-day')

# For testing local
rg.csv(per_d, 'C:/Users/John/Desktop/master-nonmedia/projects/github-mirror/push/orders/orders/active-per-day')

print '<p>active-per-day.csv updated.'




### CURRENTLY ACTIVE ORDERS ###

print '<br><h3> Calculating Current Active Orders</h3>'

active = []

com_dx = table[0].index('Completed')
file_dx = table[0].index('File')
insp_dx = table[0].index('Insp')
tat_dx = table[0].index('TAT/Wk')

for r in table:

	if r[com_dx] == '':
	
		# Add auditor URL http://ddti.starkcountyohio.gov/Results.aspx?SearchType=QuickSearch&Criteria1=2307+wale
		# Get file, regex digits separate from letters
	
		active.append( [r[file_dx], r[ord_dx], r[insp_dx], r[tat_dx],] )

active.insert(0, ['order', 'ordered', 'inspection', 'tat'] )
		
# Write ouput to CSV file
# For online
#rg.csv(active, '/home1/joberlin/public_html/current-active')

# For testing local
rg.csv(active, 'C:/Users/John/Desktop/master-nonmedia/projects/github-mirror/push/orders/orders/current-active')

print '<p>current-active.csv updated.'




### TIME INVOLVED (X) FEE (Y) PLOT WITH LABELS 'FORM, CLIENT' ###

print '<br><h3>Time-Fee Calculation Per Form and Client</h3>'

amnt_dx = table[0].index('Amount')
fee_dx = table[0].index('Fee') # amount / fee = time spent on order
form_dx = table[0].index('Form')
client_dx = table[0].index('Client')

time_fee = []
empty = 0

for r in table[1:]:
	
	try:
	
		t = float(r[amnt_dx]) / float(r[fee_dx]) # time involved in order
		time_fee.append( [r[form_dx], r[client_dx], t, r[fee_dx],] )
		
	except ValueError:
	
		if r[amnt_dx] == '':
		
			empty += 1
			
		else:
		
			pass
	



	
print '<p>Orders not included in calculation due to empty Amount field: %s' % empty

print '<p>Orders included in time-fee calculation: %d' % len(time_fee)

time_fee.insert(0, ['form','client','time','fee'])

#for r in time_fee:

	


# Write ouput to CSV file
# For online
#rg.csv(active, '/home1/joberlin/public_html/current-active')






print '''<h2>Close this window and refresh Orders Dashboard.</h2>
</body>
</html>'''