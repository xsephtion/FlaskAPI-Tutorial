from flask import Flask, request, jsonify
from flask import render_template
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient('mongodb://127.0.0.1:27017')
db = client.UserTest
user_col = db.user

@app.route('/', methods=['GET'])
def home_page():
    return render_template("index.html")

@app.route('/post', methods=['POST'])
def post_item():
    fname = request.form['fname']
    lname = request.form['lname']
    mname = request.form['mname']
    ids = request.form['id']

    x = user_col.insert({
        "id": ids,
        "fname": fname,
        "lname": lname,
        "mname": mname,
    })
    return "Success"

@app.route('/values', methods=['GET', 'POST'])
def get_item():
    if request.method == 'GET':
        return render_template('view.html')
    else:
        doc = user_col.find_one({'id': request.form['id']})
        if doc == None:
            return "Not found"
        else:
            return jsonify({'fname' : doc['fname'], 'lname':doc['lname'], 'id': doc['id']})

@app.route('/update', methods=['GET', 'POST'])
def update_item():
    if request.method == 'GET':
        return render_template('update.html')
    else:
        fname = request.form['fname']
        lname = request.form['lname']
        mname = request.form['mname']
        ids = request.form['id']
        x = user_col.update_one({'id': ids},{
            "$set":{
                "id": ids,
                "fname": fname,
                "lname": lname,
                "mname": mname,
            }
        })
        return "Success"
        # if x:
            
        # else:
        #     return "Unsuccessful"

@app.route('/delete', methods=['GET', 'POST'])
def delete_item():
    if request.method == 'GET':
        return render_template('delete.html')
    else:
        ids = request.form['id']
        delete = user_col.delete_one({'id': ids})
        if delete:
            return "Success"




app.run(debug=True)