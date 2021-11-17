from flask import Flask, render_template, request, redirect, session
import psycopg2
app = Flask(__name__) 
app.secret_key = 'keep it secret, keep it safe'

conn = psycopg2.connect(
    database="dcth13s0gio0s4",
    user="garovzdkeoturn",
    password="f2266ce9ca11d4a6120fad3c87892197a6761ea228cf6dcb9046cc94ef8a6ec3",
    host="ec2-18-215-44-132.compute-1.amazonaws.com",
    port="5432")

cur = conn.cursor()

#Usted solo modifique de aqui para abajo

@app.route('/')
def index():
    cur.execute("SELECT * from city order by id desc limit  20")
    rows = cur.fetchall()
    my_list = []
    for row in rows:
        my_list.append(row)

    cur.execute("SELECT countrycode from city  group by 1 order by 1 asc")
    rows = cur.fetchall()
    codes = []
    for row in rows:
        codes.append(row)

    return render_template('index.html',  results=my_list , codes = codes)

@app.route('/show/<id>')
def show(id):
    sql = "SELECT * from city where id = "+id+" limit 1"
    cur.execute(sql)
    rows = cur.fetchall()
    city = []
    for row in rows:
        city.append(row)

    return render_template('show.html',  city=city[0])

@app.route('/update/<id>',methods = ['POST'])
def update(id):
    population = request.form.get("population")
    
    sql = "Update city set population ="+ str(population) +" where id = "+str(id)
    cur.execute(sql)

    return redirect('/show/'+id)

@app.route('/insert',methods = ['POST'])
def insert():    
    cur.execute("SELECT * from city order by id desc limit 1")
    rows = cur.fetchall()
    id = []
    for row in rows:
        id.append(row)

    new_id = int(id[0][0])+1
    

    name = str(request.form.get("name"))
    district = str(request.form.get("district"))
    countrycode = str(request.form.get("countrycode"))
    population = str(request.form.get("population"))
    

    sql = "Insert Into City values ("+str(new_id)+",'"+name+"','"+countrycode+"','"+district+"','"+population+"')"
    cur.execute(sql)

    return redirect('/')

@app.route('/search',methods = ['POST'])
def search():
    search = request.form.get("search")
    cur.execute("SELECT * from city where name like '%"+search+"%'")
    rows = cur.fetchall()
    my_list = []
    for row in rows:
        my_list.append(row)

    return render_template('index.html',  results=my_list)

@app.route('/delete/<id>')
def delete(id):
    sql = "Delete from city where id = "+id
    cur.execute(sql)

    return redirect('/')

#Usted solo modifique de aqui para arriba

if __name__=="__main__":
    app.run(debug=True)

