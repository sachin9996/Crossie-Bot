from crossie_bot import is_new_message, get_clues_from_message
from pprint import pprint

messages = []
solved_clues = []

def get_enum_from_clue(clue):
	result = 0
	if clue[-2].isdigit():
		result += int(clue[-2])
	if clue[-3].isdigit():
		result += 10 * int(clue[-2])
	return result

def check_match(clue, answer):
	enum = get_enum_from_clue(clue)
	if enum is None:
		return False
	if len(answer) == 0:
		return False
	if len(answer) > 3 * enum:
		return False
	if answer[0].isdigit():
		answer = answer.partition(' ')[2]
	answer = answer.strip('?!. ()').partition(' ')[0]
	return len(answer) == enum


with open('chats/new_chat.txt') as f:
	for line in f:
		line = line.strip()
		if is_new_message(line):
			msg = line.partition(': ')[2].strip()
			messages.append(msg)

n = len(messages)
for i in range(n):
	print(i, n)
	clues = get_clues_from_message(messages[i])
	if clues != []:
		for c in clues:
			for j in range(i + 1, n):
				if check_match(c, messages[j]):
					solved_clues.append((c, messages[j]))
					break

pprint(solved_clues)
