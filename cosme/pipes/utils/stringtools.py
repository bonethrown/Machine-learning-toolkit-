import re
import numpy
import unidecode
from fuzzywuzzy import fuzz
def decodeIsoComments(commentArray):
	out = commentArray
	for item in out:
		if 'comment' in item:
			print '#### IN COMMENT #### %s' % item['comment']
			temp = item['comment']
			temp = temp.encode("utf-8")
			item['comment'] = temp
			print 'COMMET IS HUNG %s' % temp			
	return out

def isNa(price):
	if isinstance(price, list):
		Na = False
		for item in price:
			if item  == 'NA':
				Na = True
		return Na
	elif isinstance(price, str):
		check = price
		if check == 'NA':
			return True
		else:
			return False
	elif isinstance(price, unicode):
		check = price
		if check == 'NA':
			return True
		else:
			return False
	
