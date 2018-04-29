# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class AgenceItem(scrapy.Item):
    name_agence = Field()
    phone_agence = Field()
    email_agence = Field()
    address_agence = Field()
    city_agence = Field()
    lat_agence = Field()
    lon_agence = Field()
    rating_agence = Field()
    description_agence = Field()
    sells_number_agence = Field()
    location_number_agence = Field()
    ad_number = Field()
    agent_number = Field()
    name_agent = Field()
    title_agent = Field()
    email_agent = Field()
    phone_agent = Field()

class AnnonceItem(scrapy.Item):
    url_annonce = Field()
    price_annonce = Field()
    agence_annonce = Field()
    domaine_annonce = Field()
    title_annonce = Field()
    type_annonce = Field()
    room_number_annonce = Field()
    bedroom_number_annonce = Field()
    bathroom_number_annonce = Field()
    construction_year_annonce = Field()
    area_annonce = Field()
    storey_annonce = Field()
    total_storey_annonce = Field()
    description_annonce = Field()
    ges_annonce = Field()
    energy_annonce = Field()
    location_annonce = Field()
    local_id_annonce = Field()
    images_annonce = Field()