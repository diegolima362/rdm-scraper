import time
import requests
import pandas as pd
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


course_data = "<section class='panel'><div class='user-heading bg-primary'><h2>REDES DE COMPUTADORES</h2><p>CPT01036</p></div><ul class='nav nav-pills nav-stacked'><li><i class='fa fa-info-circle'></i>Carga horária de 60</li><li><i class='fa fa-user icone-margem-rdm'></i>DJALMA DE MELO CARVALHO FILHO</li><li><i class='fa fa-clock-o icone-margem-rdm'></i>Quarta 11:00 (2) - Sala: B103<br>Sexta 09:00 (2) - Sala: B104 - Lab.Inf do CCT<br><i class='disciplina-turno ico-sun diurno tooltips' title='' data-original-title='Diurno'></i></li><li class='col-md-12 tabela-rdm'><div class='text-center col-md-6 col-xs-6'><h5>---</h5>Unid. I</div><div class='text-center col-md-6 col-xs-6'><h5>---</h5>Unid. II</div></li><li class='col-md-12 rdm-falta-final'><div class='col-md-6 col-xs-6 rdm-falta'><div class='gauge-canvas text-center'><canvas width='85' height='60' id='gauge0'></canvas></div><div class='text-center'><span id='gauge-textfield0' class='gauge-value'>0</span><strong>/15</strong> Faltas</div></div><div class='text-center col-md-6 col-xs-6 rdm-final'><h5 class='text-blue-dark'>---</h5>Prova final</div></li></ul></section>"
courses = []
courses.append(build_course(course_data))
save_file(courses, 'courses.json')
