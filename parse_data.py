from bs4 import BeautifulSoup


def extract_schedule(info):
    schedule = {}

    (time, local) = info.split('-')[0:2]
    (day, start) = time.split(' ')[0:2]

    schedule['day'] = day.strip().upper()
    schedule['time'] = start.strip()
    schedule['location'] = local.split(':')[-1].strip()

    return schedule


def build_course(data):
    course = {'title': data.select_one('h2').get_text().strip()}

    con = ([p.get_text(strip=True, separator="%") for p in data.select('li')])

    if len(con) < 5:
        con.insert(1, 'SEM PROFESSOR')

    course['ch'] = con[0][-2:]
    course['instructor'] = con[1]
    course['absences'] = con[4].split('%')[0]

    info = con[2].split('%')

    course['schedule'] = [extract_schedule(i) for i in info]

    return course


def extract_courses(html_data):
    data = BeautifulSoup(html_data, 'html.parser')
    info = data.select('.panel')

    courses = [build_course(i) for i in info]

    return courses


def extract_profile(html_data):
    profile = {}

    data = BeautifulSoup(html_data, 'html.parser')

    profile['name'] = data.select_one('h2').get_text().strip()

    info = ([p.get_text(strip=True) for p in data.select('span')])

    profile['registration'] = info[0]
    profile['program'] = info[1].split('-')[1].strip()
    profile['cra'] = info[-3]
    profile['cumulative_ch'] = info[-1]

    return profile
