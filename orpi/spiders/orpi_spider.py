# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from orpi.items import AgenceItem, AnnonceItem

import json


class OrpiSpider(scrapy.Spider):
	name= "orpi"
	start_urls = ['https://www.orpi.com/agences-immobilieres/recherche']

	def parse(self, response):
		agencies = response.xpath('//script').re(r'agencies:\s*(.*)')
		agencies = json.loads(''.join(agencies).encode('utf-8')[:-1])
		listAgence=[]
		agencies = agencies[0:12]
		for agence in agencies:
			agenceItem = AgenceItem()
			agenceItem['name_agence'] = agence['slug']
			agenceItem['phone_agence'] = agence["phone"]
			agenceItem['email_agence'] = agence["email"]
			agenceItem['address_agence'] = agence["address1"]
			agenceItem['city_agence'] = agence["city"]
			agenceItem['lat_agence'] = agence["latitude"]
			agenceItem['lon_agence'] = agence["longitude"]
			agenceItem['ad_number'] = agence["id"]
			r1 = scrapy.Request('https://www.orpi.com/'+str(agence["slug"]), callback=self.parse_agence)
			r1.meta['agenceItem'] = agenceItem
			r1.meta['agencies'] = agencies
			r1.meta['listAgence'] = listAgence
			yield r1
			
	def parse_agence(self, response):
		agencies = response.meta['agencies']
		agenceItem = response.meta['agenceItem']
		listAgence = response.meta['listAgence']
		if len(response.xpath('//span[contains(@itemprop, "ratingValue")]//text()').extract()) > 0:
			agenceItem['rating_agence'] = response.xpath('//span[contains(@itemprop, "ratingValue")]//text()').extract_first()
		else:
			agenceItem['rating_agence'] = None

		if len(response.xpath('//div[@class="agencyHeader-text"]//p//text()').extract()) > 0:	
			agenceItem['description_agence'] = response.xpath('//div[@class="agencyHeader-text"]//p//text()').extract_first()
		else:
			agenceItem['description_agence'] = None

		if len(response.xpath('//div[@class="stat-item"]//span[@class="dblock"]//text()').extract()) > 6:
			agenceItem['agent_number'] = response.xpath('//div[@class="stat-item"]//span[@class="dblock"]//text()').extract()[6]
		else:
			agenceItem['agent_number'] = None

		if len(response.xpath('//div[@class="stat-item"]//span[@class="dblock"]//text()').extract()) > 2:	
			agenceItem['sells_number_agence'] = response.xpath('//div[@class="stat-item"]//span[@class="dblock"]//text()').extract()[2]
		else:
			agenceItem['sells_number_agence'] = None

		if len(response.xpath('//div[@class="stat-item"]//span[@class="dblock"]//text()').extract()) > 0:
			agenceItem['location_number_agence'] = response.xpath('//div[@class="stat-item"]//span[@class="dblock"]//text()').extract_first()
		else:
			agenceItem['location_number_agence'] = None

		if len(response.xpath('//div[@class="teamItem-content"]//span[@class="teamItem-name"]//text()').extract()) > 0:
			agenceItem['name_agent'] = response.xpath('//div[@class="teamItem-content"]//span[@class="teamItem-name"]//text()').extract_first()
		else:
			agenceItem['name_agent'] = None

		if len(response.xpath('//div[@class="teamItem-content"]//span[@class="teamItem-job"]//text()').extract()) > 0:
			agenceItem['title_agent'] = response.xpath('//div[@class="teamItem-content"]//span[@class="teamItem-job"]//text()').extract_first()
		else:
			agenceItem['title_agent'] = None

		if len(response.xpath('//div[@class="teamItem-contact"]//a[@class="textColorLink textColorLink--candy prefixed-icon"]//@href').extract()) > 0:
			agenceItem['email_agent'] = response.xpath('//div[@class="teamItem-contact"]//a[@class="textColorLink textColorLink--candy prefixed-icon"]//@href').extract_first().split(":")[1]
		else:
			agenceItem['email_agent'] = None

	
		listAgence.append(agenceItem)
		if len(listAgence) < len(agencies):
			yield agenceItem
		else:
			for item in listAgence:
				r2 = scrapy.Request('https://www.orpi.com/recherche/buy?agency='+str(item["name_agence"]), callback=self.parse_general_annonce)
				r2.meta['agenceItem'] = item	
				yield r2

	def parse_general_annonce(self, response):
		agenceItem = response.meta['agenceItem']
		annonces = response.xpath('//script').re(r'items: (.*),')[0]
		annonces = json.loads(''.join(annonces).encode('utf-8'))
		for annonce in annonces:	
				annonceItem = AnnonceItem()
				r3 = scrapy.Request('https://www.orpi.com/annonce-vente-'+str(annonce["slug"])+'/?agency=' + agenceItem["name_agence"], callback=self.parse_annonce)
				r3.meta['annonce'] = annonce
				r3.meta['annonceItem'] = annonceItem
				yield r3

	def parse_annonce(self, response):
		annonce = response.meta['annonce']
		annonceItem = response.meta['annonceItem']
		annonceItem['url_annonce'] = response.url

		if len(response.xpath('//div[@class="current-price"]//span[@class="price"]//text()').extract_first()) > 0:
			annonceItem['price_annonce'] = int(response.xpath('//div[@class="current-price"]//span[@class="price"]//text()').extract_first()[0:7].replace(' ',''))
		else:
			annonceItem['price_annonce'] = None
		if len(response.xpath('//div[@class="info"]//p[@class="title"]//a[@class="defaultLink defaultLink--candy"]//@href').extract()) > 0:
			annonceItem['agence_annonce'] = "www.orpi.com" + str(response.xpath('//div[@class="info"]//p[@class="title"]//a[@class="defaultLink defaultLink--candy"]//@href').extract_first())
		else:
			annonceItem['agence_annonce'] = None

		if len(response.xpath('//h1[@class="h1 cap"]//span[@class="text"]//text()').extract()) > 0:
			annonceItem['title_annonce'] = ''.join(response.xpath('//h1[@class="h1 cap"]//span[@class="text"]//text()').extract())
		else:
			annonceItem['title_annonce'] = None

		annonceItem['type_annonce'] = annonce['type']

		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'Nombre de pi' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				annonceItem['room_number_annonce'] = int(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2])
				break
			else:
				annonceItem['room_number_annonce'] = None
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'Nombre de chambre' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				annonceItem['bedroom_number_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2]
				break
			else:
				annonceItem['bedroom_number_annonce'] = None
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'bain' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				annonceItem['bathroom_number_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2]
				break
			else:
				annonceItem['bathroom_number_annonce'] = None
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'Ann' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				annonceItem['construction_year_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2]
				break
			else:
				annonceItem['construction_year_annonce'] = None
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'Surface<' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				annonceItem['area_annonce'] = float(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2].split(' ')[0])
				annonceItem['area_annonce'] = int(annonceItem['area_annonce'])
				break
			else:
				annonceItem['area_annonce'] = None
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'tage<' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				annonceItem['storey_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2].split(' ')[0]
				break
			else:
				annonceItem['storey_annonce'] = None
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'tage(s)<' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i] or 'immeuble<' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				annonceItem['total_storey_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2].split(' ')[0]
				break
			else:
				annonceItem['total_storey_annonce'] = None

		if 'GES' in str(response.xpath('//div[@class="estate-diagnostic-content"]').extract()):
			if len(response.xpath('//div[@class="estate-diagnostic-content"]//text()').extract())>6:
				annonceItem['ges_annonce'] = response.xpath('//div[@class="estate-diagnostic-content"]//text()').extract()[6]
			else:
				annonceItem['ges_annonce'] = None
		else:
			annonceItem['ges_annonce'] = None
		if 'DPE' in str(response.xpath('//div[@class="estate-diagnostic-content"]').extract()):
			if len(response.xpath('//div[@class="estate-diagnostic-content"]//text()').extract())>2:
				annonceItem['energy_annonce'] = response.xpath('//div[@class="estate-diagnostic-content"]//text()').extract()[2]
			else:
				annonceItem['energy_annonce'] = None
		else:
			annonceItem['energy_annonce'] = None

		if len(response.xpath('//span[@class="c-vignette__address"]//text()').extract()) > 0:
			annonceItem['location_annonce'] = response.xpath('//span[@class="c-vignette__address"]//text()').extract_first()
		else:
			annonceItem['location_annonce'] = None

		if len(response.xpath('//div[@class="estateNeighborhood__ref"]//text()').extract()) > 0:
			annonceItem['local_id_annonce'] = response.xpath('//div[@class="estateNeighborhood__ref"]//text()').extract_first().split(" : ")[1].split("\n")[0]
		else:
			annonceItem['local_id_annonce'] = None

		if len(response.xpath('//div[@class="paragraphs-textcell"]//p//text()').extract()) > 0:
			annonceItem['description_annonce'] = response.xpath('//div[@class="paragraphs-textcell"]//p//text()').extract_first()
		else:
			annonceItem['description_annonce'] = None

		annonceItem['images_annonce'] = annonce['images']

		yield annonceItem
