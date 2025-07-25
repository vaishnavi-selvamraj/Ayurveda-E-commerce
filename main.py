from flask import Flask, render_template, Response, redirect, request, session, abort, url_for, flash
import os
from flask_marshmallow import Marshmallow
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
from werkzeug.utils import secure_filename
from datetime import datetime
import time

import mysql.connector
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    charset = "utf8",
    database = "ayurveda"
    )

app = Flask(__name__)
app.secret_key = 'abcdef'

@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""
    cursor=db.cursor()
    
    return render_template('index.html')

@app.route('/retailer_login',methods=['POST','GET'])
def login_retailer():
    msg=""
    act=''
    cnt=''
    msg1=''
    cursor = db.cursor()
    if request.method=='POST':
        page = request.form['page']
        print("page_name:",page)
        if page == 'login':
            retailername=request.form['username']
            retailerpass=request.form['password']
            cursor=db.cursor()
            cursor.execute("SELECT count(*) FROM retailer_reg WHERE username=%s && password=%s && status=1",(retailername,retailerpass))
            result=cursor.fetchone()[0]
            print(result)

            if result>0:
                session['username']=retailername
                return redirect (url_for('retailer_home'))
            else:
                msg="Invalid Username or Password!!!"
        else:
            username = request.form['username']
            email = request.form['email']
            mobile = request.form['contactnumber']
            address = request.form['address']
            district = request.form['district']
            password = request.form['password']
            cpassword = request.form['confirmpassword']
            

            cursor.execute("SELECT count(*) FROM retailer_reg WHERE username=%s || email=%s",(username,email))
            cnt = cursor.fetchone()[0]
            if cnt == 0:
                cursor.execute("SELECT max(id)+1 FROM retailer_reg")
                maxid = cursor.fetchone()[0]
                if maxid is None:
                    maxid=1
                sql = "INSERT INTO retailer_reg(id,username,email,mobile,address,district,password,confirmpassword) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (maxid,username,email,mobile,address,district,password,cpassword)
                cursor.execute(sql,val)
                db.commit()
                msg1="Register Successfully"
            else:
                msg="FAIL"
            

    return render_template('retailer_login.html',msg=msg,act=act,msg1=msg1)

@app.route('/retailer_home',methods=['POST','GET'])
def retailer_home():
    msg=''
    data=''
    username=''
    if 'username' in session:
        username = session['username']
    print(username,"****uname*****")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM retailer_reg WHERE username=%s",(username, ))
    data = cursor.fetchone()

    return render_template("retailer_home.html",data=data)

@app.route('/add_product',methods=['POST','GET'])
def add_product():
    data=''
    username=''
    msg=''
    date=''
    if 'username' in session:
        username = session['username']

    print(username,"###username###")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM retailer_reg where username=%s",(username, ))
    data = cursor.fetchone()

    if request.method == 'POST':
        productname = request.form['name']
        description = request.form['Description']
        amount = request.form['Amount']
        producttype = request.form['Type']
        file = request.files['image']

        cursor.execute("SELECT max(id)+1 FROM addproduct")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1

        #now = date.today()
        #rdate = now.strftime("%d-%m-%y")

        if file:
            filename1 = file.filename
            filename2 = secure_filename(filename1)
            photo = "p"+str(maxid)+filename2
            file.save(os.path.join("static/upload/",photo))
            

        sql = "INSERT INTO addproduct(id,username,name,Description,Amount,Type,image) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,username,productname,description,amount,producttype,photo)
        cursor.execute(sql,val)
        db.commit()
        #cursor.close()
        msg = "Product Added"
        #return redirect (url_for('retailer_product'))

    return render_template("add_product.html",msg=msg,data=data)

@app.route('/viewproduct',methods=['POST','GET'])
def viewproduct():
    msg=''
    data=''
    name=''
    data2=[]
    if 'username' in session:
        name = session['username']
    print(name,"****username*****")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM retailer_reg WHERE username=%s",(name, ))
    data = cursor.fetchone()
    print(data,"data")

    cursor.execute("SELECT * FROM addproduct WHERE username=%s",(name, ))
    d1 = cursor.fetchall()
    for p in d1:
        dt=[]
        dt.append(p[0])
        dt.append(p[1])
        dt.append(p[2])
        dt.append(p[3])
        dt.append(p[4])
        dt.append(p[5])
        dt.append(p[6])
        #dt.append(p[7])
        #dt.append(p[8])
        #dt.append(p[9])
        s1="2"
        ss=""
        cursor.execute("SELECT count(*) FROM orders where retailer=%s && pid=%s",(name, p[0]))
        cnt3 = cursor.fetchone()[0]
        if cnt3>0:
            s1="1"
            ss=str(cnt3)

        print("ss="+ss)

        dt.append(ss)
        dt.append(s1)
        data2.append(dt)
        #data2.append(dt)
        print("data2:",data2)
    
    return render_template("viewproduct.html",data2=data2,msg=msg,data=data,d1=d1)

@app.route('/shop', methods=['POST', 'GET'])
def shop():
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM addproduct")
    data = cursor.fetchall()  # fetch all rows safely

    # Retrieve user_id and username from the session
    user_id = session.get('user_id')  # get user_id from session
    username = session.get('username')  # get username from session

    # Check if session variables exist, if not, set to None
    if user_id and username:
        print(f"User ID: {user_id}, Username: {username}")
    else:
        print("No user logged in")

    # Pass product data and session info to the template
    return render_template("shop.html", data=data, user_id=user_id, username=username)



@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    # Fetch the product from the database using product_id
    cursor = db.cursor()
    cursor.execute("SELECT * FROM addproduct WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    
    if product:
        # Initialize cart if it doesn't exist in the session
        if 'cart' not in session:
            session['cart'] = []
        
        # Add the product to the cart (ensure price is a float)
        session['cart'].append({
            'product_id': product[0],  # Product ID
            'name': product[2],        # Product name
            'price': float(product[4]), # Ensure price is a float
            'quantity': 1              # Default quantity
        })
        session.modified = True
        flash('Product added to cart!', 'success')

    return redirect(url_for('shop'))


@app.route('/cart')
def cart():
    # Retrieve cart from session
    cart_items = session.get('cart', [])
    
    # Calculate total price, ensuring prices are floats
    total_price = sum(float(item['price']) * item['quantity'] for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/checkout')
def checkout():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    
    # You can also add user authentication and address details here if needed
    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    
    # Simulate payment processing
    flash('Payment Successful!', 'info')
    
    # Clear the cart after payment
    session.pop('cart', None)
    
    return redirect(url_for('order_success'))



@app.route('/customer_login',methods=['POST','GET'])
def customer_login():
    msg=""
    act=''
    cnt=''
    msg1=''
    cursor = db.cursor()
    if request.method=='POST':
        page = request.form['page']
        print("page_name:",page)
        if page == 'login':
            customername=request.form['username']
            customerpass=request.form['password']
            cursor=db.cursor()
            cursor.execute("SELECT count(*) FROM customer WHERE username=%s && password=%s",(customername,customerpass))
            result=cursor.fetchone()[0]
            print(result)

            if result>0:
                session['username']=customername
                return redirect (url_for('customer_home'))
            else:
                msg="Invalid Username or Password!!!"
        else:
            username = request.form['username']
            email = request.form['email']
            mobile = request.form['contactnumber']
            address = request.form['address']
            district = request.form['district']
            password = request.form['password']
            cpassword = request.form['confirmpassword']
            

            cursor.execute("SELECT count(*) FROM customer WHERE username=%s || email=%s",(username,email))
            cnt = cursor.fetchone()[0]
            if cnt == 0:
                cursor.execute("SELECT max(id)+1 FROM customer")
                maxid = cursor.fetchone()[0]
                if maxid is None:
                    maxid=1
                sql = "INSERT INTO customer(id,username,email,mobile,address,district,password,confirmpassword) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (maxid,username,email,mobile,address,district,password,cpassword)
                cursor.execute(sql,val)
                db.commit()
                msg1="Register Successfully"
            else:
                msg="FAIL"

    return render_template('customer_login.html',msg=msg,act=act,msg1=msg1)

@app.route('/customer_home', methods=['POST', 'GET'])
def customer_home():
    data = ''
    if 'username' in session:
        username = session['username']
        print("cname:", username)
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM customer WHERE username=%s", (username,))
        data = cursor.fetchone()

        # Store user_id in session along with username
        user_id = data[0]  # Assuming the user_id is the first column in the 'customer' table
        session['user_id'] = user_id  # Store user_id in session
        
    else:
        print("No username found in session.")
        # Handle the case where username is not found, e.g., redirect to login page
        return redirect(url_for('customer_login'))  # You can adjust this to your desired redirect

    return render_template('customer_home.html', data=data)



@app.route('/rice',methods=['POST','GET'])
def rice():
    msg=''
    data1=''
    name=''
    data2=[]
    data=''
    d1=''
    pid=''
    productname=''
    cursor = db.cursor()
    cursor.execute("SELECT * FROM addproduct Where Type = 'rice'")
    data1 = cursor.fetchall()
    print("RiceData:",data1)

    
    '''
    if request.method=='POST':
        quantity = request.form.get('quantity')
        cursor.execute("SELECT * FROM addproduct WHERE id=%s OR name=%s",(pid,productname,))
        data=cursor.fetchone()
        q=int(quantity)
        amount = int(data[4])
        t=q*amount
        print("TotalAmount:",t)
    
    if 'username' in session:
        name=session['username']
    print("name:",name)
    cursor=db.cursor()
    cursor.execute("SELECT * FROM customer WHERE username=%s && mobile=%s",(name,contactnumber,))
    udata=cursor.fetchone()

    cursor.execute("SELECT * FROM retailer_reg WHERE username=%s",(retailer,))
    rdata=cursor.fetchone()
        
    cursor.execute("SELECT * FROM addproduct WHERE id=%s && name=%s",(pid,productname,))
    data=cursor.fetchone()
    #pro=data[1]
    #amount=int(data[4])
    print("amount,",amount)
    
    
    if request.method=='POST':
        quantity = request.form.get('quantity')

        cursor.execute("SELECT max(id)+1 FROM orders")
        maxid=cursor.fetchone()[0]
        if maxid is None:
            maxid=1
        q=int(quantity)
        t=q*amount
        print("TotalAmount:",t)

        sql="INSERT INTO orders(id,username,retailer,pid,contactnumber,productname,Amount,quantity,totalamount) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(maxid,name,retailer,pid,contactnumber,productname,amount,q,t)
        cursor.execute(sql,val)
        db.commit()
        msg="success"
  
    if request.method=='POST':
        page = request.form['page']
        pname=request.args.get("name")
        print("**Page**",page)
        print("pname:",pname)
        cursor=db.cursor()
        cursor.execute("SELECT * FROM addproduct where name=%s",(pname,))
        dd = cursor.fetchone()
        
        if page == 'order':
            
            query = "SELECT name FROM addproduct WHERE name ='Basmathi' OR name='Ponni' OR name='Seeragasamba'"
            cursor.execute(query)
            result = cursor.fetchall()
            
            
            query = "SELECT name FROM addproduct WHERE name = 'Ponni'"
            cursor.execute(query)
            result = cursor.fetchone()

            query = "SELECT name FROM addproduct WHERE name = 'Bamboo'"
            cursor.execute(query)
            result = cursor.fetchone()

            query = "SELECT name FROM addproduct WHERE name = 'Idlyrice'"
            cursor.execute(query)
            result = cursor.fetchone()

            query = "SELECT name FROM addproduct WHERE name = 'Karunguruvai'"
            cursor.execute(query)
            result = cursor.fetchone()

            query = "SELECT name FROM addproduct WHERE name = 'Mapillaisamba'"
            cursor.execute(query)
            result = cursor.fetchone()

            query = "SELECT name FROM addproduct WHERE name = 'Poongar'"
            cursor.execute(query)
            result = cursor.fetchone()
            
            query = "SELECT name FROM addproduct WHERE name = 'Seeragasamba'"
            cursor.execute(query)
            result = cursor.fetchone()
            

            print('result:',result)
            if result is not None:
                field_value = result[0]
                print(field_value,':field_value')
                if field_value=='Basmathi':
                    quantity = request.form.get('quantity')
                    print("quantity",quantity)
                    cursor.execute("SELECT * FROM addproduct WHERE name = 'Basmathi'")
                    data = cursor.fetchone()
                    print("fulldata",data)
                    print("amount",data[4])
                    amount = int(data[4])
                    q=int(quantity)
                    t=q*amount
                    print("Basmathi totalvalue:",t)
                    
                elif field_value=='Ponni':
                    quantity = request.form.get('quantity')
                    print("quantity",quantity)
                    cursor.execute("SELECT * FROM addproduct WHERE name = 'Ponni'")
                    data = cursor.fetchone()
                    print("fulldata",data)
                    print("amount",data[4])
                    amount = int(data[4])
                    q=int(quantity)
                    t=q*amount
                    print("Ponni totalvalue:",t)
                elif field_value=='Bamboo':
                    quantity = request.form.get('quantity')
                    print("quantity",quantity)
                    cursor.execute("SELECT * FROM addproduct WHERE name = 'Bamboo'")
                    data = cursor.fetchone()
                    print("fulldata",data)
                    print("amount",data[4])
                    amount = int(data[4])
                    q=int(quantity)
                    t=q*amount
                    print("Bamboo totalvalue:",t)
                elif field_value=='Idlyrice':
                    quantity = request.form.get('quantity')
                    print("quantity",quantity)
                    cursor.execute("SELECT * FROM addproduct WHERE name = 'Idlyrice'")
                    data = cursor.fetchone()
                    print("fulldata",data)
                    print("amount",data[4])
                    amount = int(data[4])
                    q=int(quantity)
                    t=q*amount
                    print("Idlyrice totalvalue:",t)
                elif field_value=='Karunguruvai':
                    quantity = request.form.get('quantity')
                    print("quantity",quantity)
                    cursor.execute("SELECT * FROM addproduct WHERE name = 'Karunguruvai'")
                    data = cursor.fetchone()
                    print("fulldata",data)
                    print("amount",data[4])
                    amount = int(data[4])
                    q=int(quantity)
                    t=q*amount
                    print("Karunguruvai totalvalue:",t)
                elif field_value=='Mapillaisamba':
                    quantity = request.form.get('quantity')
                    print("quantity",quantity)
                    cursor.execute("SELECT * FROM addproduct WHERE name = 'Mapillaisamba'")
                    data = cursor.fetchone()
                    print("fulldata",data)
                    print("amount",data[4])
                    amount = int(data[4])
                    q=int(quantity)
                    t=q*amount
                    print("Mapillaisamba totalvalue:",t)
                elif field_value=='Poongar':
                    quantity = request.form.get('quantity')
                    print("quantity",quantity)
                    cursor.execute("SELECT * FROM addproduct WHERE name = 'Poongar'")
                    data = cursor.fetchone()
                    print("fulldata",data)
                    print("amount",data[4])
                    amount = int(data[4])
                    q=int(quantity)
                    t=q*amount
                    print("Poongar totalvalue:",t)
                elif field_value=='Seeragasamba':
                    quantity = request.form.get('quantity')
                    print("quantity",quantity)
                    cursor.execute("SELECT * FROM addproduct WHERE name = 'Seeragasamba'")
                    data = cursor.fetchone()
                    print("fulldata",data)
                    print("amount",data[4])
                    amount = int(data[4])
                    q=int(quantity)
                    t=q*amount
                    print("Seeragasamba totalvalue:",t)
                else:
                    print("No Data Found")
            else:
                print("Not found")
                    '''
    
    return render_template('rice.html',data1=data1,msg=msg,data=data,d1=d1)

@app.route('/millets',methods=['POST','GET'])
def millets():
    msg=''
    data1=''
    name=''
    data2=[]
    data=''
    d1=''
    cursor = db.cursor()
    cursor.execute("SELECT * FROM addproduct Where Type = 'millets'")
    data1 = cursor.fetchall()
    print("millets:",data1)
    
    return render_template('millets.html',data1=data1,msg=msg,data=data,d1=d1)

@app.route('/dals',methods=['POST','GET'])
def dals():
    msg=''
    data1=''
    name=''
    data2=[]
    data=''
    d1=''
    cursor = db.cursor()
    cursor.execute("SELECT * FROM addproduct Where Type = 'dals'")
    data1 = cursor.fetchall()
    print("dals:",data1)
    
    return render_template('dals.html',data1=data1,msg=msg,data=data,d1=d1)

@app.route('/masalas',methods=['POST','GET'])
def masalas():
    msg=''
    data1=''
    name=''
    data2=[]
    data=''
    d1=''
    cursor = db.cursor()
    cursor.execute("SELECT * FROM addproduct Where Type = 'masalas'")
    data1 = cursor.fetchall()
    print("masalas:",data1)
    
    return render_template('masalas.html',data1=data1,msg=msg,data=data,d1=d1)

@app.route('/sugar',methods=['POST','GET'])
def sugar():
    msg=''
    data1=''
    name=''
    data2=[]
    data=''
    d1=''
    cursor = db.cursor()
    cursor.execute("SELECT * FROM addproduct Where Type = 'sugar'")
    data1 = cursor.fetchall()
    print("sugar:",data1)
    
    return render_template('masalas.html',data1=data1,msg=msg,data=data,d1=d1)
@app.route('/oil',methods=['POST','GET'])
def oil():
    msg=''
    data1=''
    name=''
    data2=[]
    data=''
    d1=''
    cursor = db.cursor()
    cursor.execute("SELECT * FROM addproduct Where Type = 'oil'")
    data1 = cursor.fetchall()
    print("oil:",data1)
    
    return render_template('masalas.html',data1=data1,msg=msg,data=data,d1=d1)

@app.route('/spices',methods=['POST','GET'])
def spices():
    msg=''
    data1=''
    name=''
    data2=[]
    data=''
    d1=''
    cursor = db.cursor()
    cursor.execute("SELECT * FROM addproduct Where Type = 'spices'")
    data1 = cursor.fetchall()
    print("spices:",data1)
    
    return render_template('masalas.html',data1=data1,msg=msg,data=data,d1=d1)

@app.route('/login_admin',methods=['POST','GET'])
def login_admin():
    msg=""
    act=""
    cnt=0
    if request.method == 'POST':
        ####page = request.form['adminpage']
        username1 = request.form['username']
        password1 = request.form['password']
        cursor = db.cursor()
        cursor.execute("SELECT count(*) FROM admin where username=%s && password=%s",(username1,password1))
        result = cursor.fetchone()[0]
        print(result)
        print(username1)
        print(password1)
        if result>0:
            session['username'] = username1
            return redirect(url_for('admin'))
        else:
            msg="You are logged in fail!!!"


        #return render_template('login_admin1.html',msg=msg,act=act)
    return render_template('login_admin.html',msg=msg,act=act)

@app.route('/order', methods=['POST', 'GET'])
def order():
    msg = ''
    data1 = ''
    name = ''
    data2 = []
    udata = ''
    data = ''
    d1 = ''
    t = ''
    q = ''
    rs2 = ''
    field = ''
    contactnumber = ''
    retailer = ''
    productname = ''
    amount = ''
    rid = ''  # Initialize rid
    pdata = ''
    address = ''
    district = ''

    pid = request.args.get("pid")
    contactnumber = ''
    
    if 'username' in session:
        name = session['username']
    print("name:", name)

    cursor = db.cursor()
    cursor.execute("SELECT * FROM customer WHERE username=%s", (name,))
    udata = cursor.fetchone()
    print(data, "......")
    contactnumber = udata[3]
    address = udata[4]
    district = udata[5]
    print("contactnumber", contactnumber)

    cursor.execute("SELECT * FROM addproduct WHERE id=%s", (pid,))
    data = cursor.fetchone()
    # Assuming the retailer is stored in the second column of the addproduct table
    retailer = data[1]
    productname = data[2]
    amount = int(data[4])
    print(retailer)
    print("amount,", amount)
    
    # Assign rid from retailer (assuming retailer is the id of the retailer)
    rid = retailer  # You can change this if the retailer value is different

    cursor.execute("SELECT * FROM retailer_reg WHERE id=%s", (rid,))
    rdata = cursor.fetchone()
    #print(rdata[1])

    if request.method == 'POST':
        quantity = request.form.get('quantity')

        cursor.execute("SELECT max(id)+1 FROM orders")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid = 1
        q = int(quantity)
        t = q * amount
        print("TotalAmount:", t)

        sql = "INSERT INTO orders(id, username, retailer, pid, contactnumber, productname, Amount, quantity, totalamount, address, district) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, name, retailer, pid, contactnumber, productname, amount, q, t, address, district)
        cursor.execute(sql, val)
        db.commit()
        msg = "success"
    
    return render_template('order.html', data1=data1, msg=msg, data=data, d1=d1, udata=udata, rdata=rdata, pdata=pdata)

@app.route('/vieworder',methods=['POST','GET'])
def view_order():
    rdata=''
    retailer=''
    data=''
    act=request.args.get("act")
    pid=request.args.get("pid")
    msg=''
    if 'username' in session:
        retailer = session['username']
    cursor=db.cursor()
    cursor.execute("SELECT * FROM orders WHERE retailer=%s",(retailer,))
    rdata=cursor.fetchall()
    print(rdata,"radata")

    if act == "ok":
        pid=request.args.get("pid")
        cursor.execute("update orders set status=1 where id=%s",(pid,))
        db.commit()
        msg="success"
    if act == "yes":
        pid=request.args.get("id")
        cursor.execute("DELETE FROM orders WHERE status='1' ")
        db.commit()
        msg="delete"
    
    return render_template('vieworder.html',rdata=rdata,data=data,msg=msg,act=act)

@app.route('/payment',methods=['POST','GET'])
def payment():
    data=''
    pid=''
    msg=''
    cursor=db.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 1")
    data=cursor.fetchone()
    print(data,"...")
    if request.method=='POST':
        msg="success"
    
    return render_template('payment.html',data=data,msg=msg)

@app.route('/admin',methods=['POST','GET'])
def admin():
    data=''
    msg=''
    act=request.args.get("act")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM retailer_reg")
    data = cursor.fetchall()

    if act == "ok":
        pid=request.args.get("pid")
        cursor.execute("update retailer_reg set status=1 where id=%s",(pid,))
        db.commit()
        msg="success"
    if act == 'delete':
        pid=request.args.get("pid")
        cursor.execute("DELETE FROM retailer_reg WHERE id=%s", (pid,))
        db.commit()
        msg="delete"
        
        
    return render_template('admin.html',data=data,act=act,msg=msg)
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        # Retrieve the form data
        username = request.form['username']
        rating = request.form['rating']
        review_text = request.form['reviewText']
        
        # Store the review in the MySQL database
        cursor = db.cursor()
        
        # Insert the review into the database
        query = "INSERT INTO reviews (username, rating, review_text) VALUES (%s, %s, %s)"
        values = (username, rating, review_text)
        
        cursor.execute(query, values)
        db.commit()
        
        cursor.close()
        
        # Redirect to a thank you page or show the reviews page
        flash("Thank you for your feedback! Your review has been submitted.", "success")
        return redirect(url_for('reviews'))

    return render_template('reviews.html')  # Render the review form page

@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
