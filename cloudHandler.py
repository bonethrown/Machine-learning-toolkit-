from pymongo import Connection
import os,sys,urllib2
import time
import json
import logging
from fuzzywuzzy import fuzz
import hashlib
import logging
from cosme.pipes.utils import utils
from nltk import regexp_tokenize, tokenwrap, word_tokenize
import re
import string
import catChecker
import nltk.classify.util
from nltk import classify
from nltk.classify import NaiveBayesClassifier
from catChecker import FieldCreator
import random

INDB = 'matching'
REMOTEDB = 'matching'


class CloudHandler(object):
        def __init__(self, collection):
                self.connection = Connection()
                self.indb = self.connection[INDB]

        def updateInDb(self, item, db):
                try:
                        db.save(item)

                except Exception, e:
                        print 'mongo exception'


        def updateFieldInDb(self, item, field, db):

                try:
                        db.save(item['key'], item[field])

                except Exception, e:
                        print 'mongo exception'

        def insertToDb(self, item, db):
                try:
                        db.insert(item, safe=True)

                except Exception, e:
                        print 'mongo exception'
