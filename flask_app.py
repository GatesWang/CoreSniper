from flask import Flask, request, redirect, url_for
from find_core_class import *

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        type = request.form.get('type')
        if str(type) == "find by requirement":
            return redirect(url_for('find'))
        elif str(type) == "find by number of requirements":
            return redirect(url_for('number'))

    return '''
                            <img src="static/rutgers.png" alt="Italian Trulli">
                            <form method="post">
                            <input type="radio" name="type" value="find by requirement">find by requirement<br>
                            <input type="radio" name="type" value="find by number of requirements">find by number of requirements<br>
                            <input type="submit" value="GO!" value="got">
                        </form>
            '''

@app.route('/number',methods=['GET', 'POST'])
def number():
      if request.method == 'POST':  #this block is only entered when the form is submitted
        number = request.form.get('number')
        if int(str(number)) > 7:
            return 'that is too many classes'
        else:
            return get_good_courses(int(number))
      return '''		<form method="post">
                            <select name="number">
                              <option value="1">1</option>
                              <option value="2">2</option>
                              <option value="3">3</option>
                              <option value="4">4</option>
                              <option value="5">5</option>
                              <option value="6">6</option>
                              <option value="7">7</option>
                            </select>
                            <input type="submit" value="Find Courses" value="got">
                        </form>
            '''

@app.route('/find',methods=['GET', 'POST'])
def find():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        requirement1 = request.form.get('requirement1')
        requirement2 = request.form.get('requirement2')
        requirement3 = request.form.get('requirement3')
        requirement4 = request.form.get('requirement4')
        requirement5 = request.form.get('requirement5')
        requirement6 = request.form.get('requirement6')
        requirement7 = request.form.get('requirement7')

        req_nums = []
        if requirement1 == 'on':
            req_nums.append(1)
        if requirement2 == 'on':
            req_nums.append(2)
        if requirement3 == 'on':
            req_nums.append(3)
        if requirement4 == 'on':
            req_nums.append(4)
        if requirement5 == 'on':
            req_nums.append(5)
        if requirement6 == 'on':
            req_nums.append(6)
        if requirement7 == 'on':
            req_nums.append(7)

        return get_courses(req_nums)

    return '''		<form method="post">
                            <input type="checkbox" name="requirement1"> requirement1<br>
                            V1 : Contemporary Challenges [CC] <br><br>
                            <input type="checkbox" name="requirement2"> requirement2<br>
                            V2 : Areas of Inquiry: Natural Sciences [NS] <br><br>
                            <input type="checkbox" name="requirement3"> requirement3<br>
                            V3 : Areas of Inquiry: Social [SCL] and Historical [HST] Analysis<br><br>
                            <input type="checkbox" name="requirement4"> requirement4<br>
                            V4 : Areas of Inquiry: Arts and Humanities [AHo], [AHp], [AHq], [AHr]<br><br>
                            <input type="checkbox" name="requirement5"> requirement5<br>
                            V5 : Cognitive Skills and Processes: Writing and Communication [WC], [WCr], [WCd]<br><br>
                            <input type="checkbox" name="requirement6"> requirement6<br>
                            V6 : Cognitive Skills and Processes: Quantitative and Formal Reasoning [QQ], [QR]<br><br>
                            <input type="checkbox" name="requirement7"> requirement7<br>
                            V7 : Cognitive Skills and Processes: Information Technology and Research [ITR]<br><br>
                            <input type="submit" value="Find Courses">
                        </form>
            '''
