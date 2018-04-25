# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from orpi.items import OrpiItem

import json


class OrpiSpider(scrapy.Spider):
	name= "orpi"
	start_urls = ["https://www.orpi.com/agences-immobilieres/recherche"]

	def parse(self, response):
		agencies = response.xpath('//script').re(r'agencies:\s*(.*)')
		agencies = json.loads(''.join(agencies).encode('utf-8')[:-1])
		for agence in agencies:
			item = OrpiItem()
			item['name_agence'] = agence['slug']
			item['phone_agence'] = agence["phone"]
			item['email_agence'] = agence["email"]
			item['address_agence'] = agence["address1"]
			item['city_agence'] = agence["city"]
			item['lat_agence'] = agence["latitude"]
			item['lon_agence'] = agence["longitude"]
			item['ad_number'] = agence["id"]
			r1 = scrapy.Request("https://www.orpi.com/"+str(agence["slug"])+"/", callback=self.parse_agence)
			r1.meta['item'] = item
			yield r1
			
	def parse_agence(self, response):
		item = response.meta['item']
		item['rating_agence'] = response.xpath('//span[contains(@itemprop, "ratingValue")]//text()').extract_first()
		item['description_agence'] = response.xpath('//div[@class="agencyHeader-text"]//p//text()').extract_first()
		item['agent_number'] = response.xpath('//div[@class="stat-item"]//span[@class="dblock"]//text()').extract()[6]
		item['sells_number_agence'] = response.xpath('//div[@class="stat-item"]//span[@class="dblock"]//text()').extract()[2]
		item['location_number_agence'] = response.xpath('//div[@class="stat-item"]//span[@class="dblock"]//text()').extract_first()
		item['name_agent'] = response.xpath('//div[@class="teamItem-content"]//span[@class="teamItem-name"]//text()').extract_first()
		item['title_agent'] = response.xpath('//div[@class="teamItem-content"]//span[@class="teamItem-job"]//text()').extract_first()
		item['email_agent'] = response.xpath('//div[@class="teamItem-contact"]//a[@class="textColorLink textColorLink--candy prefixed-icon"]//@href').extract_first().split(":")[1]
		if item['name_agent'].encode('ascii','ignore') in response.xpath('//div[@class="teamItem-contact"]//a[@class="phone textColorLink textColorLink--candy prefixed-icon"]').extract()[1].decode('unicode_escape').encode('ascii','ignore'):
			item['phone_agent'] = response.xpath('//div[@class="teamItem-contact"]//a[@class="phone textColorLink textColorLink--candy prefixed-icon"]//text()').extract()[1]
		else:
			item['phone_agent'] = response.xpath('//div[@class="teamItem-contact"]//a[@class="phone textColorLink textColorLink--candy prefixed-icon"]//text()').extract()[0]
		r2 = scrapy.Request("https://www.orpi.com/recherche/buy?agency="+str(item["name_agence"])+"/", callback=self.parse_general_annonce)
		r2.meta['item'] = item
		yield r2

	def parse_general_annonce(self, response):
		item = response.meta['item']
		annonces = response.xpath('//script').re(r'items: (.*),')[0]
		annonces = json.loads(''.join(annonces).encode('utf-8'))
		for annonce in annonces:
			r3 = scrapy.Request("https://www.orpi.com/annonce-vente-"+str(annonce["slug"])+"/?agency=" + item["name_agence"] +"/", callback=self.parse_annonce)
			r3.meta['item'] = item
			r3.meta['annonce'] = annonce
			yield r3

	def parse_annonce(self, response):
		item = response.meta['item']
		annonce = response.meta['annonce']
		item['url_annonce'] = response.url
		item['title_annonce'] = ''.join(response.xpath('//h1[@class="h1 cap"]//span[@class="text"]//text()').extract())
		item['type_annonce'] = annonce['type']
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'Nombre de pi' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				item['room_number_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2]
				break
			else:
				item['room_number_annonce'] = None
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'Nombre de chambre' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				item['bedroom_number_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2]
				break
			else:
				item['bedroom_number_annonce'] = None
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'bain' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				item['bathroom_number_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2]
				break
			else:
				item['bathroom_number_annonce'] = None
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'Ann' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				item['construction_year_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2]
				break
			else:
				item['construction_year_annonce'] = None
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'Surface<' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				item['area_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2].split(' ')[0]
				break
			else:
				item['area_annonce'] = None
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'tage<' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				item['storey_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2].split(' ')[0]
				break
			else:
				item['storey_annonce'] = None
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'tage(s)<' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i] or 'immeuble<' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				item['total_storey_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2].split(' ')[0]
				break
			else:
				item['total_storey_annonce'] = None
		item['description_annonce'] = response.xpath('//div[@class="paragraphs-textcell"]//p//text()').extract_first()
		if 'GES' in str(response.xpath('//div[@class="estate-diagnostic-content"]').extract()):
			item['ges_annonce'] = response.xpath('//div[@class="estate-diagnostic-content"]//text()').extract()[6]
		else:
			item['ges_annonce'] = None
		if 'DPE' in str(response.xpath('//div[@class="estate-diagnostic-content"]').extract()):
			item['energy_annonce'] = response.xpath('//div[@class="estate-diagnostic-content"]//text()').extract()[2]
		else:
			item['energy_annonce'] = None
		item['location_annonce'] = response.xpath('//span[@class="c-vignette__address"]//text()').extract_first()
		item['local_id_annonce'] = response.xpath('//div[@class="estateNeighborhood__ref"]//text()').extract_first().split(" : ")[1].split("\n")[0]
		item['images_annonce'] = annonce['images']
		yield item