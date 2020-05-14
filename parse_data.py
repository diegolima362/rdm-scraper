import time
import requests
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def extract_schedule(info):
    (time, local) = info.split('-')[0:2]
    (day, start) = time.split(' ')[0:2]

    schedule = {}
    schedule['dia'] = day.strip()
    schedule['inicio'] = start.strip()
    schedule['sala'] = local.split(':')[-1].strip()

    return schedule


def build_course(html_data):
    course = {}

    data = BeautifulSoup(html_data, 'html.parser')

    course['curso'] = data.select_one('h2').get_text()

    con = ([p.get_text(strip=True, separator="%") for p in data.select('li')])

    course['ch'] = con[0][-2:]
    course['professor'] = con[1]
    course['faltas'] = con[4].split('%')[0]

    info = con[2].split('%')
    class_info = []

    for i in info:
        class_info.append(extract_schedule(i))

    course['schedule'] = class_info

    return course


def save_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as jp:
        js = json.dumps(data, indent=4)
        jp.write(js)

course_data = ' '
courses = []
courses.append(build_course(course_data))
save_file(courses, 'courses.json')
