from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time

#set up web parsing stuff
##options = Options()
##options.add_argument('--headless')
##options.add_argument('--disable-gpu')
##driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome()

site = 'http://sis.rutgers.edu/soc/#home'
delay = 10
driver.get(site)
try:
    #pick semester
    semesters = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'currentSemesters')))
    for option in semesters.find_elements_by_tag_name('span'):
        if option.text == 'Fall 2018':
            option.click() # select() in earlier versions of webdriver
            break
    #pick campus
    campus = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'locationsOnCampusList')))
    for option in campus.find_elements_by_tag_name('span'):
        if option.text == 'New Brunswick':
            option.click() # select() in earlier versions of webdriver
            break
    #pick level
    level = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'levelsList')))
    for option in level.find_elements_by_tag_name('span'):
        if option.text == 'Undergraduate':
            option.click() # select() in earlier versions of webdriver
            break
    #submit to SOC
    submit = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'continueButton')))
    submit.click()

    #change to core urls
    codes = ['AHo','AHp','AHq','AHr','CC','HST','ITR','NS','QQ','QR','SCL','WC','WCd','WCr']
    core_url_parts = ['http://sis.rutgers.edu/soc/#coreCode?code=', '&semester=92018&campus=NB&level=U']
    course_lists = {}
    for i in range(0,len(codes)):
        driver.get('http://sis.rutgers.edu/soc/#coreCode?code=' + codes[i] + '&semester=92018&campus=NB&level=U')
        time.sleep(1)
        driver.refresh()
        time.sleep(1)
        #get courses
        #need to get more information on courses
        #course name, link, etc
        courses = driver.execute_script("""
                                            var ele = document.getElementById('s2out');
                                            var children = ele.children;
                                            var body = children[1]; courses = [];
                                            var i;
                                            for (i = 0; i < body.children.length; i++) { 
                                                courses.push(body.children[i].id);
                                            }  
                                            return courses                    
                                    """)
        temp = []
        #modify all elements in courses and store in temp
        for eachCourse in courses:
            eachCourseParts = eachCourse.split('.')
            courseCode = eachCourseParts[2] + '.' + eachCourseParts[3]
            #now get course name
            courseID = courseCode +  '.courseTitleAndCredits.courseTitle'
            courseName = driver.execute_script("""
                                            var ele = document.getElementById('""" + courseID + """');
                                            var children = ele.children;
                                            courseName = children[0].innerText; 
                                            return courseName;                    
                                    """)
            temp.append(courseCode + '|' + courseName)
            
        #make a dictionary corresponding to each core type
        course_lists[codes[i]] = temp
except TimeoutException:
    print('Loading took too much time!')
    driver.close()

#tests for correctness
##for eachCourse in course_lists['AHo']:
##    print(eachCourse)
##for key,items in course_lists.items():
##    print(key + " " + str(len(items)))

#output classes to textfiles
for key,value in course_lists.items():
    text_file = open(key + '.txt', 'w+')
    for course in value:
        text_file.write(course + '\n')
    text_file.close()


