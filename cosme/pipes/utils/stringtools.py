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