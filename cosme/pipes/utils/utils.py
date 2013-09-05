"""
Module containing some helpful utility functions
"""
import re,datetime,time
from dateutil.parser import parse
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
import logging
import numpy
from numpy import mean
import hashlib
import unidecode
#convert format "13:13" to minutes
logger = logging.getLogger(__name__)

def createKey(cosmeItem):
	key = ""
	key = cosmeItem['site'] + "_" + cosmeItem['brand'].replace(" ","-") + "_" + cosmeItem["name"].replace(" ","-") + "_"+str(cosmeItem['volume'][0]).replace(",","-").replace(".","-")
	out = key.encode('ascii', 'replace')	
	out = hashlib.md5(out).hexdigest()	

	return out

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

def checkVolume(vol):
	if isinstance(vol, list):
		check = vol[0]
		check = extractVolume(check)
	elif isinstance (vol, str):
		check = extractVolume(vol)
	elif isinstance (vol, unicode):
		check = extractVolume(vol)
		
	if check == 'NA':
		return False
	else:
		return True	


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

def greadyVolume(inputstring, suffixpattern='ml'):
	inputstring = inputstring.lower()
	pattern = '\d+%s' % suffixpattern
	volArray = re.findall(pattern, inputstring)
	if len(volArray)!= 0:
		return volArray


#Gram extractor looks for gr with and without space 

def extractGram(inputstring):
    pattern  = r'\d+g(?=[r\s-]|$)'
    gram = re.search(pattern,inputstring, re.I)
    if gram is not None:
        gram = gram.group()
        return gram
    else:
	suffixpattern = ' g(?=[r\s-]|$)'
    	pattern  = r'\d+%s' % suffixpattern
    	gram = re.search(pattern,inputstring, re.I)
	if gram is not None:
		gram = gram.group()
		return gram
	else:
		return None 

def extractVolume(inputstring, suffixpattern='ml'):
    pattern  = r'\d+%s' % suffixpattern
    vol = re.search(pattern,inputstring, re.I)
    if vol is not None:
        vol = vol.group()
        return vol
    else:
	suffixpattern = ' ml'
	pattern = r'\d+%s' % suffixpattern 
        vol = re.search(pattern, inputstring, re.I)
	if vol is not None:
		vol = vol.group()
		vol = vol.replace(" ","")
		return vol
	else:
		vol = extractGram(inputstring)
		if vol is not None:
			return vol
		else:
			return 'NA'
    
    
def extract_ML(inputstring, suffixpattern='ML'):
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
		temp = extractVolume(e)
		if not temp:
			e = extract_ML(e) 
			if e:
				out.append(e)
		elif temp:
			out.append(temp)	
			
	return out
def cleanSkuArray(array, strOrFloat):
	out = []
	for e in array:
		e = extractSku(e)
 		if strOrFloat == "float":
			e = strToFloat(e)
			out.append(e)
		else:
			e =str(e)
			out.append(e)
	return out
def arrayStringToFloat(array):
	out = []
	for e in array:
		e= strToFloat(e)
		out.append(e)
	return out

def cleanNumberArray(array, strOrFloat):
	out = []
	for e in array:
		e = findPrice(e)
		e = cleanPrice(e)
		print e
		if strOrFloat == "float":
			e = strToFloat(e)		
			out.append(e)
		else:
			out.append(e)
				
	return out

def cleanNumberArray2(array, strOrFloat):
	out = []
	if strOrFloat =="float":
		for e in array:
			e = findPrice(e)
			e = cleanPrice(e)
			e = strToFloat(e)
			out.append(e)
			return out
	else:
		for e in array:
			e = findPrice(e)
			e = cleanPrice(e)
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
		toClean = toClean.replace(val, "").strip()
	return toClean

def cleanSymbols(toClean):
 
    badChars = ["\\r","\\t","\\n",":","%",",","(",")","'","!",]
    stopWords = ["views","category","likes","added","pornstars","add","pornstar","ago","duration","sec","votes"]
    toClean = toClean.lower().strip()
    for val in badChars:
        toClean = toClean.replace(val,"")
    for word in stopWords:
        toClean = toClean.replace(word,"")    
    if toClean:
        return toClean.strip()

def cleanChars(toClean):
 
    badChars = ["\\r","\\t","\\n",":","%",",","(",")","'"]
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
def isEqualAvg(element, array):
	#numpy dependent
	b= mean(array)
	
	if float(element) / round(b, 2) == 1:
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
def extractRawPrice(string):
    tempPrice = unidecode.unidecode(string)
    tempPrice = re.search(r'R\$\s(\d+.\d+)', tempPrice).group()
    return tempPrice	


def findPrice(string):
   if isinstance(string, str) or isinstance(string, unicode): 
	    tempPrice = unidecode.unidecode(string)
	    tempPrice = re.search(r'R\$\s(\d+.\d+)', tempPrice)
	    if tempPrice is not None:
		    tempPrice = tempPrice.group()
		    if isDotAndComma(tempPrice):
			tempPrice = tempPrice.replace('.','')
			tempPrice = tempPrice.replace(',','.').strip()
		    else:
			tempPrice = tempPrice.replace(',','.').strip()
		    return tempPrice
	    else:
		    if isDotAndComma(string):
			tempPrice = string
			tempPrice = tempPrice.replace('.','')
			tempPrice = tempPrice.replace(',','.').strip()
		    else:
			tempPrice = string
			tempPrice = tempPrice.replace(',','.').strip()
		    return tempPrice
   else:
	print 'Utils find price got NON string Price'
	return string
	

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




