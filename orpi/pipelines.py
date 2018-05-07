# -*- coding: utf-8 -*-

import pymongo

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log

from .items import AgenceItem, AnnonceItem

class OrpiPipeline(object):

	def __init__(self):
		connection = pymongo.MongoClient("mongo", 27017)
		connection.drop_database('orpi')
		self.db = connection['orpi']

	def process_item(self, item, spider):
		if isinstance(item, AgenceItem):
			self.collection = self.db['agence']
			valid = True
			for data in item:
				if not data:
					valid = False
					raise DropItem("Missing {0}!".format(data))
			if valid:
				self.collection.insert(dict(item))
				log.msg("Agence added to MongoDB database!", level=log.DEBUG, spider=spider)
			return item

		elif isinstance(item, AnnonceItem):
			self.collection = self.db['annonce']
			valid = True
			for data in item:
				if not data:
					valid = False
					raise DropItem("Missing {0}!".format(data))
			if valid:
				self.collection.insert(dict(item))
				log.msg("Annonce added to MongoDB database!", level=log.DEBUG, spider=spider)
			return item
