import time
import requests
import pandas as pd
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


data = {

}

info = {}

url = 'https://academico.uepb.edu.br/ca/index.php/usuario/autenticar'

print("> starting browser...")
driver = webdriver.Firefox()
print("> browser started")

print("> getting url...")
driver.get(url)

print("> login...")
driver.find_element_by_name("nome_usuario").send_keys(data['nome_usuario'])
driver.find_element_by_name("senha_usuario").send_keys(data['senha_usuario'])
driver.find_element_by_css_selector("body > div > div > div > form > div.login-wrap > div > button").click()
print("> logged ")

print("> getting CRE ...")
cre = driver.find_element_by_xpath("//*[@id='main-content']//section//div[2]//div[1]//div//div//span").get_attribute('outerHTML')
cre_value = BeautifulSoup(cre,'html.parser').find('span').contents[0]

info['cre'] = cre_value


# print("> loading RDM ...")
# driver.find_element_by_css_selector("#nav-accordion > li:nth-child(3) > a").click()

driver.quit()

print("> Saving file with info...")
print("> Done!")