import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import parse_data as parser


def save_file(info, filename):
    with open(filename, 'w') as jp:
        json.dump(info, jp, ensure_ascii=False, indent=4)


def load_user():
    user_info = {'nome_usuario': input("Matricula: "), 'senha_usuario': input("Senha: ")}

    return user_info


def login():
    user = load_user()

    user_xpath = "/html/body/div/div/div/form/div[2]/div/div/input[1]"
    pass_xpath = "/html/body/div/div/div/form/div[2]/div/div/input[2]"
    submit_xpath = "/html/body/div/div/div/form/div[2]/div/button"

    driver.find_element_by_xpath(user_xpath).send_keys(user['nome_usuario'])
    driver.find_element_by_xpath(pass_xpath).send_keys(user['senha_usuario'])
    driver.find_element_by_xpath(submit_xpath).click()

    driver.get(url_history)

    if driver.current_url != url_history:
        print("> Login fails\n> Exiting...")
        driver.quit()
        exit()


#################################################################################


home_url = "https://academico.uepb.edu.br/ca/index.php/usuario/autenticar"
url_history = "https://academico.uepb.edu.br/ca/index.php/alunos/historico"
url_rdm = "https://academico.uepb.edu.br/ca/index.php/alunos/rdm"

option = Options()
option.headless = True

print("> starting browser...")
driver = webdriver.Firefox(options=option)
print("> browser started")

print("> getting url...")
driver.get(home_url)

print("> login...")
login()
print("> logged ")

profile_css_selector = "#main-content > section > section"
courses_data_selector = "#main-content > section > div:nth-child(3)"

print("> Getting profile data...")
profile_data = driver.find_element_by_css_selector(profile_css_selector).get_attribute("outerHTML")

print("> Getting courses data...")
driver.get(url_rdm)
courses_data = driver.find_element_by_css_selector(courses_data_selector).get_attribute("outerHTML")

print("> Parsing data")
data = {'profile': parser.extract_profile(profile_data), 'courses': parser.extract_courses(courses_data)}

print("> Closing browser...")
driver.quit()
print("> Browser closed")

print("> Saving file...")
save_file(data, 'data.json')
print("> Files save 'data.json'")

print("> All done")
