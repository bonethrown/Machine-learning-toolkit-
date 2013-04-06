from utils import utils

def process(item,spider,matcher):
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
        print "########TEMP DOS  ######### %s", tempBrand
        tempBrand = utils.extractBrand(tempBrand)
        item['brand'] = tempBrand

    if item['name']:
        tempName = item['name']
        tempName = tempName[0]
        item['name'] = utils.cleanChars(tempName)

    if item['category']:
        tempCat = item['category']
        #tampCat = tempCat[0]
        print "##########CATEGORY PIPE ############", tempCat[0]
        item['category'] = tempCat[0]
    if item['image']:
        temp = item['image'] 
        temp = temp[0]
        item['image'] = temp
    if item['sku']: 
        temp = item['sku']
        temp = temp[0]
        item['sku'] = utils.extractSku(temp)

    return item
