from cosme.pipes.utils import db 
from pymongo import Connection
import os,sys,urllib2



def cleanVolume(db):
	
	for item in db.find():
		print item['volume']
		if item['volume'] is None:
			item['volume'] = 'NA'
			toDb(item,db)
			print 'was None %s' % item['key']
		if item['volume'] == '':
			item['volume'] = 'NA'
			toDb(item,db)
			print 'item was empty string %s' % item['key']
		elif len(item['volume']) == 0:
			item['volume'] = 'NA'
			toDb(item,db)
			print 'item was empty ARRAY %s' % item['key']
		elif item['volume'] == ['NA']:
			item['volume'] = 'NA'
			toDb(item,db)
			print 'item was empty ARRAY %s' % item['key']
			
def toDb(item, db):
	try:
		db.testLalina.update( {'key': item['key']}, item, safe = True)
	except Exception, e:
		print e	
		


def main(spray):
	connection = Connection()
	
	lalina = connection.production
	lalina = lalina[spray]
	print lalina
	cleanVolume(lalina)


if __name__ == "__main__":

    #first argument: batch size
    #second argument: dmp or feed
    #third argument : filename
    main(str(sys.argv[1]))
