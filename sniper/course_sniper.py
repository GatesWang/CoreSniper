from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

#set up web parsing stuff
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
#driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome()

subject = input('enter subject: ')
course = input('enter the course number: ')
sections = input('enter sections (1,2,3): ')
usr= input('enter username: ')
pswd = input('enter password: ')

site = 'http://sis.rutgers.edu/soc/#home'
delay = 1000
logged = False

try:
    while True:
        driver.get(site)
        driver.refresh();
        time.sleep(2)
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

        #go to the subject you want to take
        driver.get('http://sis.rutgers.edu/soc/#courses?subject='+ subject + '&semester=92018&campus=NB&level=U')
        driver.refresh()
        time.sleep(2)

        
        #parse all of the sections
        #wait for element to load g selenium
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'courseDataParent')))
        script = """ 
        var ele = document.getElementById('courseDataParent');
        courses = ele.children;
        var i; course_ids = [];
        for (i = 0; i < courses.length; i++) { 
            course_ids.push(courses[i].id);
        }
        return course_ids;
        """
        course_ids = driver.execute_script(script)
        
        #find class that you want and assign values for js ids
        expand_id = ''
        for course_id in course_ids:
            course_id_parts = course_id.split('.')
            course_numbers = course_id_parts[2]
            if course in course_numbers:
                exapand_id = course_id_parts[2] + '.' + course_id_parts[3]
                listing_id = course_id_parts[2] + '.' + course_id_parts[3] + '.sectionListings'
        #find class and see if it is open
        #wait for element to load selenium
        ele1 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, exapand_id)))
        ele2 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, listing_id)))
        
        script = """ 
        CourseService.expandOrCollapseCourse('""" + exapand_id + """');
        var listing = document.getElementById('""" + listing_id + """');
        sections = listing.children;
        var i;
        register_links = [];
        for (i = 1; i < sections.length; i++) { 
            section = sections[i];
            section_body = section.children[section.children.length-1];
            //availibility = section_body.children[0].children[0].classList
            //if(availibility[0] == 'sectionopen'){
            register = section_body.children[section_body.children.length-1];
            register_link = register.getElementsByTagName('a')[0].href;
                register_links.push(register_link);
            //}
        }
        return register_links;
        """
        all_register_links = driver.execute_script(script)
        #log in to webreg
        if sections == None:
            register_links = all_register_links
            print('not working')
        else:
            print('working')
            register_links = []
            sections_list = sections.split(',')
            for section in sections_list:
                register_links.append(all_register_links[int(section)-1])
        for i in range(0,len(register_links)):
            driver.get(register_links[i])
            #check to see if logged in
            if not logged:        
                username = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'username')))
                username.send_keys(usr) 

                password = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'password')))
                password.send_keys(pswd) 
                password.send_keys(Keys.ENTER)
                logged = True

            #register for the class
            register_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'submit')))
            register_button.click()

            #check for errors
            error = driver.find_elements_by_class_name('error')
            if len(error)>0:
                print(error[0].get_attribute('innerHTML'))
            else:
                print('successfully registered')
        time.sleep(2)
except TimeoutException:
    print('Loading took too much time!')
    driver.close()
