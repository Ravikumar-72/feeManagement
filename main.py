from flask import Flask,render_template,request, session
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="Ravikumar@72", database="fee_management")
cur = mydb.cursor()

app = Flask(__name__)

@app.route('/')
@app.route('/home',methods=["POST"])
def home():
    if request.method == "POST":
        full_name = request.form.get('first_name')
        user_type = request.form.get('user_type')
        email = request.form.get('email')
        password = request.form.get('password')
        cur.execute("INSERT INTO registered(full_name,user_type,email,password) VALUES(%s, %s, %s, %s)",
                    (full_name,user_type,email,password))
        mydb.commit()
        return render_template("home.html",title="Home")
    else:
        return render_template("home.html", title="Home")

@app.route('/after_admin_login',methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user_type").lower()
    msg = "Such type of user is not exists. Please confirm whether you registered or not"
    if request.method =="POST":
        cur.execute("SELECT email,password,user_type FROM registered WHERE email = %s AND password = %s AND user_type = %s",
                    (email,password,user_type))
        result = cur.fetchone()
        #print(result)
        if result is not None:
            if user_type == "admin":
                return render_template('after_admin_login.html',title='Hello Admin!')
            if user_type == "accountant":
                return render_template('accountant.html',title='Accountant')
        else:
            return render_template('home.html',title="Home",msg=msg)

@app.route('/accountant',methods=["POST"])
def accountant():
    return render_template('accountant.html',title="Accountant")

@app.route('/register')
def register():
    return render_template('register.html',title="Register")

@app.route('/add_acc',methods=["POST"])
def add_acc():
    # msg = None
    full_name = request.form.get("full_name")
    if full_name is not None:
        # full_name = request.form.get("full_name")
        email = request.form.get("email")
        sex = request.form.get("sex")
        contact = request.form.get("contact")
        msg = "Accountant added successfully..."
        print(str(full_name)+" "+str(email)+" "+str(sex)+" "+str(contact))
        cur.execute("INSERT INTO accountant(full_name,email,sex,contact) VALUES(%s, %s, %s, %s)",
                    (full_name, email, sex, contact))
        mydb.commit()
        if full_name and email and sex and contact is not None:
            return render_template('add_acc.html',title="Add Accountant",msg=msg)
    return render_template('add_acc.html',title='Add Accountant')

@app.route('/view_acc',methods=["POST"])
def view_acc():
    cur.execute("SELECT * FROM accountant")
    result = cur.fetchall()
    print(result)
    return render_template('view_acc.html',title='View Accountant',result=result)

@app.route('/delete_acc',methods=["POST"])
def delete_acc():
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    cur.execute("DELETE FROM accountant WHERE full_name = %s AND email = %s",(full_name,email))
    cur.execute("DELETE FROM registered WHERE full_name = %s AND email = %s",(full_name,email))
    mydb.commit()
    msg = "Accountant deleted successfully..."
    return render_template('delete_acc.html',title='Delete Accountant',msg=msg)

@app.route('/view_student',methods=["POST"])
def view_student():
    cur.execute("SELECT * FROM student")
    result = cur.fetchall()
    print(result)
    return render_template('view_student.html',title="View student",result=result)

@app.route('/add_student',methods=["POST"])
def add_student():
    full_name = request.form.get('full_name')
    if full_name is not None:
        email = request.form.get('email')
        regno = request.form.get('regno')
        dept = request.form.get('dept')
        sex = request.form.get('sex')
        contact = request.form.get('contact')
        msg = "Accountant added successfully..."
        #print(str(full_name)+" "+str(email)+" "+str(regno)+" "+str(dept)+" "+str(sex)+" "+str(contact))
        cur.execute("INSERT INTO student(full_name,email,regno,dept,sex,contact) VALUES(%s, %s, %s, %s, %s, %s)",
                    (full_name, email,regno,dept, sex, contact))
        mydb.commit()
        if full_name and email and regno and dept and sex and contact is not None:
            return render_template('add_student.html',title="Add student",msg=msg)
    return render_template('add_student.html',title="Add student")

@app.route('/delete_student',methods=["POST"])
def delete_student():
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    regno = request.form.get("regno")
    msg = "student deleted successfully..."
    cur.execute("DELETE FROM student WHERE full_name = %s AND email = %s AND regno = %s",(full_name,email,regno))
    return render_template('delete_student.html',title="Delete student",msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
