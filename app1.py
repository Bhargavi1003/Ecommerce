from flask import Flask,render_template,request
import pymysql
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import random
import razorpay
RAZORPAY_KEY_ID = 'rzp_test_7aThPyJimSbFfi'
RAZORPAY_KEY_SECRET = 'ZynBiRWjqyj9SzYwe95cCk6l'
client = razorpay.Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET))
verifyotp = "0"
db_config = {
    'host' : 'localhost',
    'database' : 'flowercart',
    'user' : 'root',
    'password' : 'root'
}
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")

@app.route("/collectcontactus",methods=["POST","GET"])
def collectcontactus():
    if request.method == "POST":
        fullname = request.form["name"]
        mobile = request.form["mobile"]
        mail = request.form["email"]
        print(fullname, mobile, mail)
    else:
        return "Data sent by unauthorized person"
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        q = "SELECT * FROM ENQUIRY"
        cursor.execute(q)
        rows = cursor.fetchall()
        print(rows)
        existed_emails = []
        for i in rows:
            existed_emails.append(i[2])
        if mail in existed_emails:
            x = f"Dear {fullname}, you  are already in our database. Our team will get back to you"
            return render_template("contactresult.html",message=x)
        else:
            conn = pymysql.connect(**db_config)
            print("succesfull")
            cursor = conn.cursor()
            print("cursor")
            q1 = "INSERT INTO ENQUIRY VALUES (%s,%s,%s)"
            print(fullname, mobile, mail)
            cursor.execute(q1,(fullname,mobile,mail))
            print("execute")
            conn.commit()
            print("commit")
    except:
        return render_template("contactresult.html",message="Data not properly sent to the server")
    else:
        x = f"Dear {fullname}, our team will get back to you"
        return render_template("contactresult.html",message = x)
@app.route("/contactresult")
def contactresult():
    return render_template("contactresult.html")
@app.route("/enquirydata")
def enquirydata():
    return render_template("enquirydata.html")
@app.route("/gatherenquirydata")
def gatherenquirydata():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        q = "SELECT * FROM ENQUIRY"
        cursor.execute(q)
        rows = cursor.fetchall()
        print(rows)
        return render_template("enquirydata.html",data=rows)
    except:
        x = "Some random error occured while fetching enquiry data from database"
        return render_template("contactresult.html",message=x)
@app.route("/signup")
def signup():
    return render_template("signup.html")
@app.route("/sendotp", methods=["POST", "GET"])
def sendotp():
    otp = random.randint(1111,9999)
    global verifyotp
    verifyotp = str(otp)
    print(verifyotp)
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        mobile = request.form['mobile']
        mailid = request.form['email']
        print(fname,lname,mobile,mailid)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        mailusername = "bhargavichigurupati04@gmail.com"
        mailpassword = "bgfm sutc pful qizq"
        from_email = "bhargavichigurupati04@gmail.com"
        to_email = mailid
        subject = "OTP FOR VERIFICATION"
        body = f"The OTP for Verification is {verifyotp}"
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP(smtp_server,smtp_port)
        server.starttls()
        server.login(mailusername,mailpassword)
        server.send_message(msg)
        server.quit()
        return render_template("signup1.html",fname=fname,lname=lname,mobile=mobile,email=mailid)
    else:
        return "Data entered by un autarized user"
@app.route('/verifyotp',methods = ["POST",'GET'])
def verifyotp():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        mobile = request.form['mobile']
        mailid = request.form['email']
        gototp = request.form['otp']
        if gototp == verifyotp:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            q = "INSERT INTO USERS VALUES (%s,%s,%s,%s)"
            cursor.execute(q,(fname,lname,mobile,mailid))
            conn.commit()
            x = "Data Sucessfully Stored into our data base, Now you can Login"
            return render_template("contactresult.html",message=x)
        else:
            return "Wrong OTP entered"
@app.route("/signup1")
def signup1():
    return render_template("signup1.html")

@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/verifylogin", methods=["POST","GET"])
def verifylogin():
    if request.method == "POST":
        mail = request.form['email']
        mobile = request.form['mobile']
        print(mail,mobile)
        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            q = "SELECT * FROM USERS"
            cursor.execute(q)
            rows = cursor.fetchall()
            print(rows)
            mobile_numbers = []
            emails = []
            fnames = []
            lnames = []
            for x in rows:
                fnames.append(x[0])
                lnames.append(x[1])
                mobile_numbers.append(x[2])
                emails.append(x[3])
            if mail in emails:
                ind = emails.index(mail)
                if mobile in mobile_numbers[ind]:
                    fn = fnames[ind]
                    ln = lnames[ind]
                    fnamee = fn + " " + ln
                    return render_template("shopping.html",name=fnamee,mail=mail)
                else:
                    return render_template("contactresult.html",message="Invalid Mobile number, Check and Try again")
            else:
                return render_template("contactresult.html",message="Invalid Email, Check and try again")
        except:
            return render_template("contactresult.html",message="Unable to access data")
    else:
        return render_template("contactresult.html",message="Data can not be sent to server")
    

@app.route("/shopping")
def shopping():
    return render_template("shopping.html")


@app.route("/storecart",methods=["POST","GET"])
def storecart():
    if request.method == "POST":
        details = request.form['cart']
        id,pname,price,uname,email = details.split(",")
        print(details)
        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            q = "SELECT * FROM CART"
            cursor.execute(q)
            rows = cursor.fetchall()
            ids = []
            names = []
            prices = []
            emails = []
            qts = []
            for x in rows:
                ids.append(x[0])
                names.append(x[1])
                emails.append(x[2])
                prices.append(x[3])
                qts.append(x[4])
            if id in ids:
                ind = ids.index(id)
                x = qts[ind]
                x = int(x)
                x = x + 1
                x = str(x)
                conn = pymysql.connect(**db_config)
                cursor = conn.cursor()
                q = "UPDATE CART SET QTY = %s WHERE PID = %s"
                cursor.execute(q,(x,id))
                conn.commit()
                return render_template("shopping.html",name=uname,mail=email)
            else:
                conn = pymysql.connect(**db_config)
                cursor = conn.cursor()
                q = "INSERT INTO CART VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(q,(id,pname,email,price,"1"))
                conn.commit()
                return render_template("shopping.html",name=uname,mail=email)
        except:
            return render_template("contactresult.html",message="Error occured in Data base")
    else:
        return render_template("contactresult.html",message="Data not sent to backend, try once again")

@app.route("/cart", methods = ["POST","GET"])
def cart():
    if request.method == "POST":
        email = request.form['mail']
        conn = pymysql.connect(**db_config)
        print("connect")
        cursor = conn.cursor()
        print("cursor")
        q = "SELECT * FROM CART WHERE EMAIL = %s"
        print("query")
        cursor.execute(q,(email))
        print("execute")
        rows = cursor.fetchall()
        print("fetch")
        print(rows)
        prices = []
        quantities= []
        for i in rows:
            prices.append(i[3])
            quantities.append(i[4])
        print(prices)
        print(quantities)
        total_price = 0
        for i in range(len(prices)):
            price = int(prices[i])
            quantity = int(quantities[i])
            total_price = total_price + (price*quantity)
        total_price = total_price
        order = client.order.create({
            'amount' : total_price,
            'currency' : 'INR',
            'payment_capture' : '1'
        })
        return render_template("shoppingcart.html",data=rows,total=total_price,order = order,email=email)
    
@app.route("/storecart1",methods=["POST","GET"])
def storecart1():
    if request.method == "POST":
        # email = request.method['mail']
        data = request.form['cart']
        rowss = []
        rows = data.split(",")
        rowss.append(rows)
        print(rowss)
        total_price = int(rowss[0][3])+100
        order = client.order.create({
            'amount' : total_price,
            'currency' : 'INR',
            'payment_capture' : '1'
        })
        return render_template("shoppingcart.html",data=rowss,total=total_price,order = order,email=rowss[0][2])
        # return render_template("shoppingcart.html",data=rowss,total=rows[3])

@app.route("/sucess",methods = ["POST","GET"])
def sucess():
    payment_id = request.form.get('razorpay_payment_id')
    order_id = request.form.get('razorpay_order_id')
    signature = request.form.get('razorpay_signature')
    total_price = request.form.get('total_price')
    dict1 = {
        'razorpay_order_id' : order_id,
        'razorpay_payment_id' : payment_id,
        'razorpay_signature' : signature
    }
    try:
        client.utility.verify_payment_signature(dict1)
        return render_template("contactresult.html",message = "Payment Sucessfull")
    except razorpay.errors.SignatureVerificationError:
        return render_template("contactresult.html",message="Payment Un sucessfull")
    
# @app.route("/shoppingcart")
# def shoppingcart():
#     return render_template("shoppingcart.html")


if __name__ == "__main__":
    app.run(port=5001)