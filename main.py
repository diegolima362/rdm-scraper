from webscraping import get_all_data, save_file

if __name__ == '__main__':
    user = 'matricula'
    password = 'senha'

    try:
        data = get_all_data(user, password)
        file_name = str(data['profile']['register']).lower() + '.json'
        print(data)
        save_file(data, file_name)
    except PermissionError as e:
        print(e)
