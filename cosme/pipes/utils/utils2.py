
def allToString(anything):
	if isinstance(anything, list):
		out = ""
		if len(anything) == 1:
			for item in anything:
				if isinstance(item, unicode):
					string = item.encode('utf-8')
					out = out+string

				else:
					out = anyToString(item)
			return out
		else:
			for item in anything:
				if isinstance(item, unicode):
					string = item.encode('utf-8')
					out = out+"/"+string

				elif isinstance(item,str):
					out = out+"/"+anyToString(item)
			return out
	else:
		out = anyToString(anything)
		return out

def anyToString(anything):
	if isinstance(anything, list):
		for item in anything:
			out = str(item)
		return out

	elif isinstance(anything, int):
		out = str(anything)
		return out

	elif isinstance(anything, float):
		out = str(anything)
		return out

	elif isinstance(anything, unicode):
		return anything

	elif isinstance(anything, str):
		return anything

def arrayToFile(name, array):
                savedoc = open(stringfield+'map', 'wb')
                for item in array:
                        savedoc.write("%s\n" % item.encode('utf-8'))
