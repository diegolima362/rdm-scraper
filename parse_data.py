import datetime
import re


def sanitize_absences(dom):
    absences = []

    reg_exp = re.compile(r"\(\d\.\d\)")
    reg_exp2 = re.compile(r".\.")

    script = str(dom.find("script", text=reg_exp))
    values = reg_exp.findall(script)

    for val in values:
        absences.append(int(reg_exp2.findall(val)[0].split('.')[0]))

    return absences


def sanitize_absences_limit(dom):
    reg_exp = re.compile(r"maxValue = (\d*);")
    # reg_exp2 = re.compile(r"\d{1,2}")

    script = str(dom.find("script", text=reg_exp))
    values = reg_exp.findall(script)
    limits = []
    for val in values:
        limits.append(int(val))

    return limits


def sanitize_schedule(info):
    (time, local) = info.split('-')[0:2]
    (day, start) = time.split(' ')[0:2]
    return {
        'day': day.strip().upper(),
        'time': start.strip(),
        'location': local.split(':')[-1].strip()
    }


def build_course(dom):
    con = ([p.get_text(strip=True, separator="%") for p in dom.select('li')])

    if len(con) < 5:
        con.insert(1, 'SEM PROFESSOR')

    title = dom.select_one('h2').text
    course_id = dom.select_one('p').text

    course_data = dom.select('li')
    grades_data = dom.select('h5')

    grades = []

    for g in grades_data:
        grades.append(g.text)

    if len(course_data) < 5:
        course_data.insert(1, '<p>SEM PROFESSOR</p>')

    ch = int(course_data[0].text.split(' ')[3])

    professor = course_data[1].text

    info = con[2].split('%')

    schedule = [sanitize_schedule(i) for i in info]

    course = {
        'id': course_id,
        'title': title,
        'professor': professor,
        'ch': ch,
        'schedule': schedule,
        'und1Grade': grades[0],
        'und2Grade': grades[1],
        'finalTest': grades[2],
    }

    return course


def sanitize_courses(dom):
    data = dom.find_all(class_='profile-nav')

    courses = []

    absences = sanitize_absences(dom)
    absences_limit = sanitize_absences_limit(dom)

    for d in data:
        courses.append(build_course(d))

    for i in range(len(courses)):
        courses[i]['absences'] = absences[i]
        courses[i]['absences_limit'] = absences_limit[i]

    return courses


def sanitize_home_info(dom):
    return {
        'cra': dom.find(class_="text-purple").text,
        'cumulativeCH': dom.find(class_="ch").text,
        'building': dom.find(class_="nome-predio").text
    }


def sanitize_personal_data(dom):
    data = dom.body.find_all(class_='form-control-static'),

    if data is None:
        return None

    name = data[0][1].text
    date = data[0][12].text.split('/')
    birth_date = datetime.datetime(int(date[2]), int(date[1]), int(date[0])).date()
    birth_date = birth_date.strftime("%m/%d/%Y")

    return {
        'register': data[0][0].text,
        'name': name,
        'viewName': name.split(' ')[0],
        'program': data[0][3].text.split(' (')[0].split('- ')[1],
        'campus': data[0][3].text.split('(')[1].split(')')[0],
        'birthDate': birth_date,
        'gender': data[0][13].text[0]
    }


def build_profile(personal_data, home_info):
    return {
        'name': personal_data['name'],
        'register': personal_data['register'],
        'cra': home_info['cra'],
        'cumulativeCH': home_info['cumulativeCH'],
        'building': home_info['building'],
        'viewName': personal_data['viewName'],
        'birthDate': personal_data['birthDate'],
        'campus': personal_data['campus'],
        'gender': personal_data['gender'],
        'program': personal_data['program'],
    }


def sanitize_profile(dom):
    home_info = sanitize_home_info(dom['home'])
    personal_data = sanitize_personal_data(dom['personal_data'])

    return build_profile(personal_data, home_info)
