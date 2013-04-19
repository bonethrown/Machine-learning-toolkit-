from utils import utils
from cosme.pipes.default import AbstractSite
from cosme.pipes.utils.utils import get_http_response
from cosme.spiders.xpaths.xpath_registry import XPathRegistry

class BelezanaWeb(AbstractSite):

    def __init__(self):
        self.siteModule = XPathRegistry().getXPath('belezanaweb')
    
    def process(self, item,spider,matcher):
        if item['url']:
            item['url'] = item['url'].lower()					
    
        if item['price']: 
            # tempPrice = re.search(r'[\d.,]+',str(item['price']))
            # tempPrice = tempPrice.group().replace(',','.')
            # item['price'] = float(tempPrice)
            item['price'] = utils.extractPrice(item['price'])
    
        if item['brand']:
            tempBrand = item['brand']
            tempBrand = tempBrand[0]
            tempBrand = utils.extractBrand(tempBrand)
            item['brand'] = tempBrand
    
        if item['name']:
            tempName = item['name']
            tempName = tempName[0]
            item['name'] = utils.cleanChars(tempName)
    
        if item['category']:
            tempCat = item['category']
            item['category'] = tempCat[0]
        if item['image']:
            temp = item['image'] 
            temp = temp[0]
            item['image'] = temp
        if item['sku']: 
            temp = item['sku']
            temp = temp[0]
            item['sku'] = utils.extractSku(temp)
        if item['comments']:
            comment_html = item['comments']
            item['comments'] = self.get_comments(comment_html, item['url'])

        return item


    def get_comments(self, comment_html, url):
        hxs = get_http_response(comment_html[0], url)
        comments = hxs.select(self.siteModule.get_comments()['commentList'])
        result = []
        for comment in comments:
            commentDict = dict()
            commentDict['star'] = self.get_star(comment, 
                                                    self.siteModule.get_comments()['commentStar'],
                                                    self.siteModule.get_comments()['commentStar2'])
            if commentDict['star'] is None:
                continue
            commentDict['name'] = comment.select(self.siteModule.get_comments()['commenterName']).extract()
            if len(commentDict['name']) == 0:
                commentDict['name'] = comment.select(self.siteModule.get_comments()['commenterName2']).extract()
            commentDict['date'] = self.get_date(comment, self.siteModule.get_comments()['commentDate'])
            commentText = comment.select(self.siteModule.get_comments()['commentText']).extract()
            if len(commentText) == 0:
                commentText = comment.select(self.siteModule.get_comments()['commentText2']).extract()
            commentDict['comment'] = commentText[0].strip()
                
            
            result.append(commentDict)
        return result
    
    def get_date(self, comment, pattern):
        datestr  = ''.join(comment.select(pattern).extract()).strip()
        needle= 'em'
        idx = datestr.find(needle)
        if idx > -1:
            return datestr[idx + len(needle):].strip()
        else:
            return datestr

    def get_star(self, comment, pattern, pattern2):
            possiblestars  = comment.select(pattern).extract()
            if len(possiblestars) == 0:
                possiblestars  = comment.select(pattern2).extract()
            return len(possiblestars)    
