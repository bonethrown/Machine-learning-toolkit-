"""
Module containing some helpful utility functions
"""
import re,datetime,time
from dateutil.parser import parse
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
import logging
#convert format "13:13" to minutes
logger = logging.getLogger(__name__)

def createKey(cosmeItem):
	key = ""
	key = cosmeItem['site'] + "_" + cosmeItem['brand'].replace(" ","-") + "_" + cosmeItem['name'].replace(" ","-") + "_"+str(cosmeItem['price'][0]).replace(",","-").replace(".","-")
	return key

def convertTime(time):
    timeInSeconds = 0
    if time.find(":")>0:
        min,sec = time.split(":")
    elif time.find("m")>0:
         min,sec = time.split("m")
         sec = sec.replace("s","")
    else:
        min = 0
        sec = 0
    min = int(min)
    sec = int(sec)       
    return (min*60)+sec
    
def convertDate(toConvert):
    dateSplit = toConvert.split(" ")


def get_volume(name, pattern='ML'):
    volume = ''
    if len(name) >= 1:
        actualname = name[0]
    else:
        actualname = name
    actualname = actualname.strip()
    if actualname.endswith(pattern):
        idx = actualname.rfind(' ')
        volume=actualname[idx:]
    return volume
    
def extractVolume(inputstring, suffixpattern='ml'):
    pattern  = '\d+%s' % suffixpattern
    vol = re.search(pattern,inputstring)
    if vol is not None:
        vol = vol.group()
        return vol
    else: 
        return None

def getElementVolume(volArray):
	out = []
	for e in volArray:
		e = extractVolume(e)
		if e is not None:
			out.append(e)
	return out
def cleanSkuArray(array, strOrFloat):
	out = []
	for e in array:
		e = extractSku(e)
 		if strOrFloat == "float":
			e = strToFloat(e)
			out.append(e)
		else:
			out.append(e)
	return out

def cleanNumberArray(array, strOrFloat):
	out = []
	for e in array:
		e = findPrice(e)
		e = cleanPrice(e)
		if strOrFloat == "float":
			e = strToFloat(e)		
			out.append(e)
		else:
			out.append(e)
				
	return out

def cleanElementChars(array):
	out = []
	for e in array:
		e = cleanChars(e)
	    	out.append(e)
	return out
def isDotAndComma(string):
	dot = "."
	com = ","
	if string.find(dot) > 0 and string.find(com) > 0:
		return True
	else:
		return False

def cleanPrice(toClean):
	badChars = ["R","r","$"]
	toClean = toClean.strip()
	for val in badChars:
		toClean = toClean.replace(val, "")
	return toClean

def cleanChars(toClean):
 
    badChars = ["\\r","\\t","\\n",":","%",",","(",")"]
    stopWords = ["views","category","likes","added","pornstars","add","pornstar","ago","duration","sec","votes"]
    toClean = toClean.lower().strip()
    for val in badChars:
        toClean = toClean.replace(val,"")
    for word in stopWords:
        toClean = toClean.replace(word,"")    
    if toClean:
        return toClean.strip()
    
def cleanHtmlTags(strArr):
    p = re.compile(r'<.*?>')
    pm = re.compile(r'\([^)]*\)')
    cleanArr = map(lambda x: p.sub('',x),strArr)
    return map(lambda x: pm.sub('',x),cleanArr)
    
 #TODO finish and test
 
def dateDeltaToIso(dateStr):

    today = datetime.datetime.today()
    
    dateTimeDelta = datetime.datetime.today()
    #we should have ["9","months"]
    dateNumeric,datePeriod =  dateStr.split(" ")
    dateNumeric = int(dateNumeric)
    if datePeriod == "years" or datePeriod == "year" :
        dateTimeDelta =  datetime.timedelta(days = dateNumeric *366)
    if datePeriod == "months" or datePeriod == "month":
        dateTimeDelta =  datetime.timedelta(days = dateNumeric * 30)
    if datePeriod == "weeks" or datePeriod == "week":
        dateTimeDelta =  datetime.timedelta(days = dateNumeric *7)
    if datePeriod == "days" or datePeriod == "days":
        dateTimeDelta =  datetime.timedelta(days = dateNumeric)
    if datePeriod == "hours" or datePeriod == "hour":
	#if today don't worry about it
    	return today.isoformat()+"Z"
    
    newDate = today - dateTimeDelta
    return newDate.isoformat()+"Z"
def isEqualAvg(item, array):
	a = sum(array)
	b = a / len(array)
	if item == b:
		return True
	else:
		return False    
# Ecpected format is "August 15, 2012"
def convertDateClass(toConv):
    date =  parse(toConv)
    return date.isoformat()+"Z"

#return the first in array
def getFirst(array):
    if isinstance(array,list):
            return array.pop()
    return array
#return the last item in array
def getLast(array):
    if isinstance(array,list):
        return array[len(array)-1]
    return array

def convertDateClassOBJ(toConv):
    date =  parse(toConv)
    return date

def extractSku(string):
    temp = str(string)
    temp = re.search(r'[\d]+', temp)
    temp = temp.group()
    temp = int(temp)
    return temp

def findPrice(string):
    tempPrice = str(string)
    tempPrice = re.search(r'[\d.,]+', tempPrice).group()
    if isDotAndComma(tempPrice):
	tempPrice = tempPrice.replace('.','')
	tempPrice = tempPrice.replace(',','.')
    else:
	tempPrice = tempPrice.replace(',','.')
   
    return tempPrice

def strToFloat(string):
    tempPrice = float(string)
    return tempPrice

def extractPrice(arrayOrString):
	if isinstance(arrayOrString, list):
		temp = arrayOrString[0]
		price = findPrice(temp)
		return price
	elif isinstance(arrayOrString, str):
		temp = arrayOrString
		price = temp(findPrice)
		return price	

class listMatcher:

    def __init__(self, config):
        self.lookup = []

        try:
            fp = open(config,'r')
            print "loading file"
            for line in fp.readlines():
                self.lookup.append(line.lower().strip())
            fp.close()
        except Exception, e:
            print "###ERROR reading file###"
            print e 
    
    def listMatch(self, toMatch):
        toMatch = " "+toMatch+" "
        for line in self.lookup: 
           # reg = "\s?"
           # regify = reg+"("+line+")"+reg
           # print regify
            line = " "+line+" "
            brand = re.search(line ,toMatch, re.I)
            if brand:
                print "####### match  %s"%line
                print "######match %s"%brand		
                print "######match found "+brand.group()
                return brand.group()


def get_http_response(responseBody, url):
        request = Request(url=url)
        response = HtmlResponse(url=url,
                            request=request,
                            body=responseBody,
                            encoding = 'utf-8')
        hxs = HtmlXPathSelector(response)
        return hxs
    
def extractBrand(toConv):
    toConv  = re.search(r'[\w]+.+', toConv)
    toConv=toConv.group()
    return toConv
def groupItem(toGroup):
    if toGroup:
        myGroup = toGroup.group()
        return myGroup
    else:
        print " is not a string none error"

if __name__ == '__main__':
    print "Testing List matcher"
    a = "imel Fabulash Waterproof - Cor 22 Black - Ulric de Varens"
    print a
    m = listMatcher('brandric.list')
    print m.listMatch(a)




