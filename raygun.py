'''
2D Array Functions

Terminology

table (2D array):
header:          feature   | feature   | feature
row:             attribute | attribute | attribute
row:             attribute | attribute | attribute

Main Functions:

* array(csv_file) parses CSV lines and appends rows to a 2D array
* csv(table, file_name) writes an array to a CSV file
* strip(table, feature, string, replace) removes or replaces a character or string among all feature's attributes
* get(table, lookup_feat, lookup_attrib, get_feat, all) returns attributes for particular features and rows
* min_max(table, lookup_feat, minORmax, attribORrow) returns attribute or row of a min or max feature
* hTable(table, file_name, header) wraps a 2D array in table HTML

'''



def parse(line, row_list):
	'''
	Recursive string splicing
	'''
	
	for char in line:
	
		if ',' in line:
		
			if char == '\"':
			
				end = line[1:].index(char) + 1
					
				q_sec = line[1:end]
				
				row_list.append(q_sec)
				
				# Plus 2 to clear the quote and comma (",)
				line = line[end + 2:]
				
				parse(line, row_list)
				
				break
				
			elif char == ',':
				
				end = line.index(char)

				row_list.append(line[:end])

				# Plus 1 to clear the comma (,)
				line = line[end + 1:]
				
				parse(line, row_list)
				
				break
				
			else:
			
				pass

		# In the case the line ends with no comma
		else:
		
			if char == '\"':
			
				end = line[1:].index(char) + 1
					
				q_sec = line[1:end]
				
				row_list.append(q_sec)
				
				break
		
			else:
			
				row_list.append(line)
			
				break



def array(csv_file):
	'''
	CSV file to embedded 2D array (table)
	CSV Formatting:

	header, header, header
	attribute, "att, ri, bute", attribute
	'''
				
	with open(csv_file, 'r') as f:
		csv = f.read()

	csv = csv.splitlines()

	table = []

	for line in csv:

		row = []

		parse(line, row)

		table.append(row)

	return table

	
	
def csv(table, file_name):
	'''
	Write array to CSV file.
	Does not accept double quotes.
	
	table: some 2D array
	file_name: name of new CSV file, without .csv extension
	'''
	
	# Check for double quotes
	err = False
	
	for row in table:
		
		for attrib in row:
		
			# The Python array attribute may be non-string
			if type(attrib) == str:
		
				if '\"' in attrib:
				
					err = True
					
					break
					
				else:
				
					pass
					
			else:
			
				pass
			
	if err == False:			

		txt = ''
		
		for row in table:
			
			for attrib in row:
			
				# The Python array attribute may be non-string
				if type(attrib) == str:
				
					if ',' in attrib:
				
						txt += '\"' + attrib + '\"'
				
					else:
					
						txt += attrib
					
					if row.index(attrib) != len(row) - 1:
					
						txt += ','
					
					else:
					
						pass
				
				# For non-string attributes
				else:
				
					txt += str(attrib)
				
					if row.index(attrib) != len(row) - 1:
					
						txt += ','
					
					else:
					
						pass
					
			txt += '\n'
		
		with open(file_name + '.csv', 'w') as f:
	
			f.write(txt)

	else:
	
		print 'Error: Double quotes found. Remove double quotes from data. Try strip().'

		

def strip(table, feature, string, replace):
	'''
	Strips or replaces a character (or any string) from a feature's attributes (ie a column's data).
	For example, strip '$' and/or ',' from number strings to be able to convert to integers or floats.
	To strip, replace = ''.
	'''
	
	f_dx = table[0].index(feature)

	for row in table:
	
		if string in row[f_dx]:
		
			attribute = row[f_dx]
			
			row_dx = table.index(row)
			
			table[row_dx][f_dx] = attribute.replace(string, replace)	

	
	
def get(table, lookup_feat, lookup_attrib, get_feat, all):
	'''
	Returns an attribute for a particular feature for a particular row(s).
	Table must have headers/features row at index 0.
	
	0  Name | Age | Fav Color
	1  Yahya| 80  | black
	2  Ruby | 43  | grey
	3  Ruby | 75  | purple
	
	lookup_feat: feature by which you want to select the row(s), eg 'Name'
	lookup_attrib: attribute by which you want to select the row(s), eg 'Ruby'
	get_feat: feature by which you want to select the particular attribute in row, eg 'Fav Color'
	all: True returns all matches in an array, eg ['grey','purple']. False returns first match, eg 'grey'.
	'''
	
	# Check that features are present
	if lookup_feat in table[0]:
		if get_feat in table[0]:
	
			lookup_dx = table[0].index(lookup_feat)
			get_dx = table[0].index(get_feat)
			
			all_ = []
			
			# Set nonmatch counter
			nonmatch = 0
			
			for row in table:
			
				if row[lookup_dx] == lookup_attrib:
					
					# In the case we want a list of all matches
					if all == True:
						
						all_.append(row[get_dx])
					
					# Or we want the first match only as string
					else:
					
						return row[get_dx]
						
						# Match found, so cut the iteration
						break
				
				else:
					
					nonmatch += 1
			
			# If all rows have nonmatches
			if nonmatch == len(table):
			
				print 'There is no match for ' + lookup_attrib + ' under feature ' + lookup_feat
				
				return ''
				
			else:
			
				if all == True:
							
					return all_
					
				else:
					
					pass
		else:
		
			print '\"' + get_feat + '\" is not a feature.'
			
			return ''
			
	else:
	
		print '\"' + lookup_feat + '\" is not a feature.'
		
		return ''

		
		
def min_max(table, lookup_feat, minORmax, attribORrow):
	'''
	Returns minimum or maximum value of column. Excludes row 0 (header row).
	
	table: some 2D array
	lookup_feat: feature of attributes to compare
	minORmax: to return min, set to 0, or max = 1
	attribORrow: to return the attribute, set to 0, or row as arrway = 1
	
	May send error if attribute cannot be converted to float. Try first preparing data with strip().
	Add: try/except error when cell cannot be float()
	'''

	if lookup_feat in table[0]:
	
		lookup_dx = table[0].index(lookup_feat)
		
		# Find minimum
		if minORmax == 0:
		
			# Set the variable
			min_val = ''
		
			for row in table:
			
				# Exclude header row
				if table.index(row) != 0:
				
					# Add try exception in cases attribute cannot be changed to type float
				
					# To set min to the first possible attribute that can be converted to float
					if min_val == '':
					
						min_val = float(row[lookup_dx])
						
						min_row = row
					
					else:
					
						if min_val > float(row[lookup_dx]):
						
							min_val = float(row[lookup_dx])
					
							min_row = row
						
				else:
				
					pass
			
			# Return value only
			if attribORrow == 0:
			
				return min_val
			
			# Or return entire row as an array
			else:
			
				return min_row

		else:
		
			# Set the variable
			max_val = ''
		
			for row in table:
			
				# Exclude header row
				if table.index(row) != 0:
				
					# Add try exception in cases attribute cannot be changed to type float
				
					# To set max to the first possible attribute that can be converted to float
					if max_val == '':
					
						max_val = float(row[lookup_dx])
						
						max_row = row
					
					else:
					
						if max_val < float(row[lookup_dx]):
						
							max_val = float(row[lookup_dx])
					
							max_row = row
						
				else:
				
					pass
			
			# Return value only
			if attribORrow == 0:
			
				return max_val
			
			# Or return entire row as an array
			else:
			
				return max_row

	else:
	
		print '\"' + lookup_feat + '\" is not a feature.'
		
		return ''

		
		
def hTable(table, file_name, header):
	'''
	Takes 2D array (a table), outputs HTML table in new file.
	header = True/False
	'''
	
	r_markup = ''
	
	for row in table:
	
		if header == True:
		
			r_markup += '\n		<tr>\n'
		
			if table.index(row) == 0:
				
				for feature in row:			
					r_markup += '			<th>%s</th>\n' % (feature)
			
			else:
	
				for feature in row:	
				
					r_markup += '			<td>%s</td>\n' % (feature)
			
			r_markup += '		</tr>'
			
		else:
		
			r_markup += '\n		<tr>\n'
			
			for attribute in row:	
		
				r_markup += '			<td>%s</td>\n' % (attribute)
					
			r_markup += '		</tr>'


	markup = '''<html>
<head>
	<style>
		table {
			border-collapse: collapse;
		}
        tr:nth-child(odd) {
            background-color: #f5f5f5;
        }
		th {
			background-color: grey;
			border: 1px solid black;
		}
		td {
			border: 1px solid grey;
		}
		th,td {
			padding: 2px;
			text-align: right;
			font-family: monospace;
		}
	</style>
</head>
<body>
	<table>%s
	</table>
</body>
</html>''' % (r_markup)

	
	with open(file_name+'.html', 'w') as f:
	
		f.write(markup)




