import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from zikime.models import *  # django.setup() 이후에 임포트해야 오류가 나지 않음

CSV_PATH_PRODUCTS='./city.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None) # 출력시 함께 출력되는 맨첫줄을 제외하고 출력하기 위함
        for row in data_reader:
                if row[0]:
                        city_name_csv = row[0]
                if row[1]:
                        country_name_csv = row[1]
                if row[2]:
                        district_name_csv = row[2]
                city = City_CSV.objects.create(name = city_name_csv)
                country = Country_CSV.objects.create(city=city, name = country_name_csv)
                district = District_CSV.objects.create(name = district_name_csv, country=country)
                