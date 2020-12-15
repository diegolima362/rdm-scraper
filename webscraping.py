import json

import requests
from bs4 import BeautifulSoup

import parse_data as parser


def request_dom(user, password):
    base_url = "https://academico.uepb.edu.br/ca/index.php/alunos"
    login_url = "https://academico.uepb.edu.br/ca/index.php/usuario/autenticar"

    form_data = {
        'nome_usuario': user,
        'senha_usuario': password
    }

    with requests.Session() as s:
        r = s.get(base_url + '/index')

        print('> login')
        r = s.post(login_url, data=form_data)

        error1 = '<p>Usuário ou senha não conferem.</p>'
        error2 = '<p>Matrícula ou senha não conferem.</p>'

        if error1 in r.text or error2 in r.text:
            raise PermissionError('Matrícula ou senha não conferem')

        print('> login ok')

        print('> get home info')
        inicio = s.get(base_url + '/index')

        print('> get personal info')
        cadastro = s.get(base_url + '/cadastro')

        print('> get courses info')
        rdm = s.get(base_url + '/rdm')

    print('> sanitize')
    return {
        'home': BeautifulSoup(inicio.content, 'html.parser'),
        'personal_data': BeautifulSoup(cadastro.content, 'html.parser'),
        'rdm': BeautifulSoup(rdm.content, 'html.parser'),
    }


def get_all_data(user, password):
    try:
        print('> get dom')
        _dom = request_dom(user, password)

        if _dom is None:
            return None

        print('> data ok')
        return {
            'profile': parser.sanitize_profile(_dom),
            'courses': parser.sanitize_courses(_dom['rdm'])
        }

    except PermissionError:
        raise


#################################################################################


def save_file(info, filename):
    with open(filename, 'w') as jp:
        print('> save data to ' + filename)
        json.dump(info, jp, ensure_ascii=False, indent=4)
