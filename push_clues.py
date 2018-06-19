import gspread
from oauth2client.service_account import ServiceAccountCredentials
from matplotlib import pyplot as plt
import re

clues = []

######### Where all the magic happens ########

prog = re.compile(r""".* # The clue could be any string
	\( # Opening parenthesis
	[0-9]* # Single number for enum
	(,(\ *)[0-9]*)* # Potentially more numbers in enum
	\) # Close parenthesis
	""", re.VERBOSE)

##############################################
######## A couple of helper functions ########
##############################################

def isnewmessage(line):
	if len(line) < 10:
		return False
	if ',' not in line:
		return False
	date = line.split(',')[0]
	if len(date.split('/')) == 3:
		return True
	return False

def get_clue(message):
	match = prog.match(message.strip())
	if any([char in message for char in '}{[]']):
		return None
	if match is not None:
		return match.group()
	return None

##############################################
############## Extracting clues ##############
##############################################

print('Extracting clues')

with open('chat') as f:
	for line in f:
		line = line.strip()
		if isnewmessage(line):
			date = line.split(',')[0].strip()
			line = ','.join(line.split(',')[1:])
			time = line.split('-')[0].strip()
			line = '-'.join(line.split('-')[1:])
			person = line.split(':')[0].strip()
			line = ':'.join(line.split(':')[1:])
			message = line.strip()
			clue = get_clue(message)
			if clue is not None:
				clues.append((date, time, person, clue))

n_clues = len(clues)

# ##############################################
# ########## Pushing to Google sheets ##########
# ##############################################

print('Connecting to Google Sheets')

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("Crossie clues")
sheet = wks.sheet1

print('Connection successful')
print('Pushing clues to Google sheets')

row_f = 2
row_l = 1 + n_clues
col_f = 1
col_l = 4

cell_range = sheet.range(row_f, col_f, row_l, col_l)

for cell in cell_range:
	i = cell.row - 2
	j = cell.col - 1
	cell.value = clues[i][j]
	
print('Making updates')
sheet.update_cells(cell_range)