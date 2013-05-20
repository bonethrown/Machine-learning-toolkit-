import httplib2
import sunburnt
TEST_URL = 'http://localhost:8080/solr/cosmeTest/'
SOLR_URL = 'http://localhost:8080/solr/cosme0/'
SOLR_CACHE = "solr_cache"
SOLR_UPDATE = "http://localhost:8080/solr/cosme0/update?json"

#Get connection to solr instance
def getConnection(url=SOLR_URL, cache=SOLR_CACHE):
    h = httplib2.Http(cache = cache)
    solr_interface = sunburnt.SolrInterface(url=url ,http_connection=h)
    return solr_interface


def ping():
    #TODO return true if solr is alive
    pass
