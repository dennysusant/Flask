from flask import Flask, abort, jsonify, request, render_template, redirect
import mysql.connector

app=Flask(__name__)

dbku = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='denny2310',
    auth_plugin = 'mysql_native_password',
    database='player'
)


@app.route('/',methods=['GET'])
def beranda():
    return render_template('pendaftaran.html')
# ==================Sign Up===========================
@app.route('/login',methods=['POST'])
def login():
    kursor=dbku.cursor()
    kursor.execute('describe user')
    kolom=kursor.fetchall()
    namakolom=[]
    for item in kolom:
        namakolom.append(item[0])
    print(namakolom)
    kursor.execute('select * from user')
    data=kursor.fetchall()
    datadict=[]
    body=request.form
    for item in data:
        x={}
        for item1 in range(len(item)):
            x[namakolom[item1]]=item[item1]
        datadict.append(x)
    x=0
    y=0
    for item in datadict:
        if body['email'] == item['email'] and body['password'] == item['password']:
            x+=1
        elif body['email'] == item['email']:
            y+=1
    if x>=1:
        return 'Berhasil Login'
    elif y>0:
        return 'Password salah'
    elif y==0:
        return 'Silakan Sign Up'
# ============================LOGIN=======================================
@app.route('/User', methods=['GET','POST'])
def students():
    
    kursor=dbku.cursor()
    kursor.execute('describe user')
    kolom=kursor.fetchall()
    namakolom=[]
    for item in kolom:
        namakolom.append(item[0])
    print(namakolom)
    kursor.execute('select * from user')
    data=kursor.fetchall()
    datadict=[]
    for item in data:
        x={}
        for item1 in range(len(item)):
            x[namakolom[item1]]=item[item1]
        datadict.append(x)
    listemail=[]
    for item in datadict:
        listemail.append(item['email'])
    body=request.form
    kursor=dbku.cursor()
    if body['email']in listemail:
        return 'Email sudah digunakan'
    else:
        qry='insert into user (email,password) values(%s,%s)'
        val=(body['email'],body['password'])
        kursor.execute(qry,val)
        dbku.commit()
        return 'Anda sudah terdaftar'
 

if __name__=='__main__':
    app.run(debug=True)