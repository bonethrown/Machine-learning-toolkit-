




def arrayToFile(self, name, array):
                savedoc = open(stringfield+'map', 'wb')
                for item in array:
                        savedoc.write("%s\n" % item.encode('utf-8'))
