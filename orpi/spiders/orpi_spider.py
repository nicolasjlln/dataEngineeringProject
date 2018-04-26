# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from orpi.items import AgenceItem, AnnonceItem

import json


class OrpiSpider(scrapy.Spider):
	name= "orpi"
	start_urls = ["https://www.orpi.com/agences-immobilieres/recherche"]

	def parse(self, response):
		agencies = response.xpath('//script').re(r'agencies:\s*(.*)')
		agencies = json.loads(''.join(agencies).encode('utf-8')[:-1])
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
			r1 = scrapy.Request("https://www.orpi.com/"+str(agence["slug"])+"/", callback=self.parse_agence)
			r1.meta['agenceItem'] = agenceItem
			yield r1
			
	def parse_agence(self, response):
		agenceItem = response.meta['agenceItem']
		agenceItem['rating_agence'] = response.xpath('//span[contains(@itemprop, "ratingValue")]//text()').extract_first()
		agenceItem['description_agence'] = response.xpath('//div[@class="agencyHeader-text"]//p//text()').extract_first()
		agenceItem['agent_number'] = response.xpath('//div[@class="stat-item"]//span[@class="dblock"]//text()').extract()[6]
		agenceItem['sells_number_agence'] = response.xpath('//div[@class="stat-item"]//span[@class="dblock"]//text()').extract()[2]
		agenceItem['location_number_agence'] = response.xpath('//div[@class="stat-item"]//span[@class="dblock"]//text()').extract_first()
		agenceItem['name_agent'] = response.xpath('//div[@class="teamItem-content"]//span[@class="teamItem-name"]//text()').extract_first()
		agenceItem['title_agent'] = response.xpath('//div[@class="teamItem-content"]//span[@class="teamItem-job"]//text()').extract_first()
		agenceItem['email_agent'] = response.xpath('//div[@class="teamItem-contact"]//a[@class="textColorLink textColorLink--candy prefixed-icon"]//@href').extract_first().split(":")[1]
		if agenceItem['name_agent'].encode('ascii','ignore') in response.xpath('//div[@class="teamItem-contact"]//a[@class="phone textColorLink textColorLink--candy prefixed-icon"]').extract()[1].decode('unicode_escape').encode('ascii','ignore'):
			agenceItem['phone_agent'] = response.xpath('//div[@class="teamItem-contact"]//a[@class="phone textColorLink textColorLink--candy prefixed-icon"]//text()').extract()[1]
		else:
			agenceItem['phone_agent'] = response.xpath('//div[@class="teamItem-contact"]//a[@class="phone textColorLink textColorLink--candy prefixed-icon"]//text()').extract()[0]
		r2 = scrapy.Request("https://www.orpi.com/recherche/buy?agency="+str(agenceItem["name_agence"])+"/", callback=self.parse_general_annonce)
		r2.meta['agenceItem'] = agenceItem
		yield agenceItem
		yield r2

	def parse_general_annonce(self, response):
		agenceItem = response.meta['agenceItem']
		annonces = response.xpath('//script').re(r'items: (.*),')[0]
		annonces = json.loads(''.join(annonces).encode('utf-8'))
		for annonce in annonces:
			annonceItem = AnnonceItem()
			r3 = scrapy.Request("https://www.orpi.com/annonce-vente-"+str(annonce["slug"])+"/?agency=" + agenceItem["name_agence"] +"/", callback=self.parse_annonce)
			r3.meta['agenceItem'] = agenceItem
			r3.meta['annonce'] = annonce
			r3.meta['annonceItem'] = annonceItem
			yield r3

	def parse_annonce(self, response):
		agenceItem = response.meta['agenceItem']
		annonce = response.meta['annonce']
		annonceItem = response.meta['annonceItem']
		annonceItem['url_annonce'] = response.url
		annonceItem['title_annonce'] = ''.join(response.xpath('//h1[@class="h1 cap"]//span[@class="text"]//text()').extract())
		annonceItem['type_annonce'] = annonce['type']
		for i in range(0,len(response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract())):
			if 'Nombre de pi' in response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li').extract()[i]:
				annonceItem['room_number_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2]
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
				annonceItem['area_annonce'] = response.xpath('//ul[@class="dotted-list dotted-list--ocom"]//li//text()').extract()[3*i+2].split(' ')[0]
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
		annonceItem['description_annonce'] = response.xpath('//div[@class="paragraphs-textcell"]//p//text()').extract_first()
		if 'GES' in str(response.xpath('//div[@class="estate-diagnostic-content"]').extract()):
			annonceItem['ges_annonce'] = response.xpath('//div[@class="estate-diagnostic-content"]//text()').extract()[6]
		else:
			annonceItem['ges_annonce'] = None
		if 'DPE' in str(response.xpath('//div[@class="estate-diagnostic-content"]').extract()):
			annonceItem['energy_annonce'] = response.xpath('//div[@class="estate-diagnostic-content"]//text()').extract()[2]
		else:
			annonceItem['energy_annonce'] = None
		annonceItem['location_annonce'] = response.xpath('//span[@class="c-vignette__address"]//text()').extract_first()
		annonceItem['local_id_annonce'] = response.xpath('//div[@class="estateNeighborhood__ref"]//text()').extract_first().split(" : ")[1].split("\n")[0]
		annonceItem['images_annonce'] = annonce['images']
		yield annonceItem