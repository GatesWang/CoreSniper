import sqlite3
import itertools

requirements = []
requirements.append(['CC'])
requirements.append(['NS'])
requirements.append(['SCL','HST'])
requirements.append(['AHo', 'AHp', 'AHq', 'AHr'])
requirements.append(['WC','WCd','WCr'])
requirements.append(['QQ','QR'])
requirements.append(['ITR'])

###create the tables
##for num in range(0,len(requirements)):
##    c.execute('''CREATE TABLE requirement''' + str(num+1) + ''' (number text, name text, core text)''')
##    requirement = requirements[num]
##    for core in requirement:
##        print(core)

###insert the data
##requirement_nums = [1,2,3,4,5,6,7]
##for num in requirement_nums:
##    requirement = requirements[num-1]
##    for core in requirement:
##        print(core)
##        core_classes = cores[core].readlines()
##        for course in core_classes:
##            course_parts = course.split("|")
##            print(course_parts[0])
##            print(course_parts[1])
##            print(core)
##            c.execute('''INSERT INTO {} VALUES (?, ?, ?)'''.format('requirement' + str(num)),(course_parts[0], course_parts[1], core))

#given the requirements get core codes
def get_core_codes(requirement_nums):
    core_req = []
    for num in requirement_nums:
        requirement = requirements[num-1]
        for core in requirement:
            core_req.append(core)
    return str(core_req)

#get the courses that satisfy certain requirements
def get_courses(requirement_nums):
    conn = sqlite3.connect('classes.db')
    c = conn.cursor()
    sql = ''
    for i in range(0,len(requirement_nums)):
        num = requirement_nums[i]
        sql += 'SELECT  name from {} '.format('requirement'+str(num))
        if i != len(requirement_nums)-1:
            sql += 'INTERSECT '

    courses = c.execute(sql)
    result = ''
    for course in courses:
        result += course[0] + '<br>'
    conn.commit()
    conn.close()
    return result

#print courses that satisfy a certain number of requirements
def get_good_courses(number):
    result = ''
    requirement_nums = [1,2,3,4,5,6,7]
    combinations = list(itertools.combinations(requirement_nums,number))
    for combination in combinations:
        courses = get_courses(combination)
        rows = courses.split('<br>')
        print(len(rows))
        if len(rows)!=1:
            result += str(combination) + '<br>'
            for row in rows:
                result += str(row) + '<br>'
        else:
            print('hello')
    return result













