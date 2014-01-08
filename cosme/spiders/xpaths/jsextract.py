import json
from BeautifulSoup import BeautifulSoup


def jsPrice(responseBody):
	soup = BeautifulSoup(responseBody)
	findall = soup.findAll('script')
		
