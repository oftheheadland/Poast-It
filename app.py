from flask import Flask, render_template, request, jsonify, make_response
from json import dumps
from string import Template
from collections import Counter
from datetime import datetime
import psycopg2
import os 
import random
import string
import base64
import subprocess
try:
    from Crypto import Random
    from Crypto.Cipher import AES
except:
    subprocess.call(['pip', 'install', 'pycryptodome'])
import hashlib
import json
import time    





BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[-1]]
class AESCipher:

    def __init__( self, key ):
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw.encode('utf8') ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))





app = Flask(__name__)
#DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = 'postgres://gxdvbdjpsgzase:3b9c304dab325ba9788e1f3f882d17f5c3e57767fcba1222b2a1f318b16dba24@ec2-184-73-197-211.compute-1.amazonaws.com:5432/d9mg0f8n3nrkb3'

HTML_TEMPLATE = Template("""
<h1>${note_ID}</h1>

			<textarea readonly id="textbox" rows="4" cols="50">
			${content}
			</textarea>
            <form method="post" id="form">
            <input id="key">Key</input><br>
			<button>Search</button>
		</form>
        <script>
<script src="{{ url_for('static', filename='js/decrypt.js') }}"></script>
            """)



@app.route('/notes/<url_note_ID>')
def note_page(url_note_ID):
    foundContent = fetchFromTable(url_note_ID)
    encrypted = str(foundContent[0])
    print(encrypted)

    #AES_key = "oopsiewoopsie" 
    #cipher = AESCipher(AES_key)


    #decrypted = cipher.decrypt(encrypted)
    #print(decrypted.decode("utf-8"))


    return render_template('note.html', content= encrypted)
    #return(HTML_TEMPLATE.substitute(note_ID=url_note_ID, content= foundContent))


@app.route('/encrypt/', methods=['POST'])
def poast():
    #print(request.form.get('text', 0))    
    messageText = request.form.get('text', 0)

    #AES_key = "oopsiewoopsie" 
    AES_key = request.form.get('key', 0)

    generatedID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))

    
    cipher = AESCipher(AES_key)
    encrypted = cipher.encrypt(messageText)
    print(encrypted.decode("utf-8") )
    decrypted = cipher.decrypt(encrypted)
    #print(encrypted)
    #print(decrypted)

    data = {
    "key": str(AES_key),
    "encrypted": str(encrypted),
    "decrypted": str(decrypted),
    "generatedID": generatedID
    }
    addToTable(encrypted.decode("utf-8") , generatedID)
    #addToTable(messageText, generatedID)

    return jsonify(data)
    #return json.dumps(str(decrypted) + " " + str(encrypted) + " " + str(AES_key))
    #return(generatedID)
    




@app.route('/decrypt/', methods=['POST'])
def decrypt():
    messageText = request.form.get('text', 0)
    AES_key = request.form.get('key', 0)


    #AES_key = "oopsiewoopsie" 
    cipher = AESCipher(AES_key)
    #encrypted = cipher.encrypt(messageText)
    #print(encrypted.decode("utf-8") )
    try:
        decrypted = cipher.decrypt(messageText)
        data = {
        "key": str(AES_key),
        "decrypted": str(decrypted.decode("utf-8"))
        }

 
        return jsonify(data)


    except:
        return jsonify("failed")

    #print(encrypted)
    #print(decrypted)



@app.route('/')
def index():
    return render_template('index.html')

def fetchFromTable(postID):

    conn = None

    try:

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        #cur.execute('SELECT FROM poasts WHERE ID=' + postID)
        cur.execute('SELECT CONTENT FROM poasts WHERE ID = ' + "'" + postID + "'")
        row = cur.fetchone()
        
        print(row)

        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()

        print(row)
        return row

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error

    finally:
        if conn is not None:
            conn.close()



def addToTable(messageText, postID):
    #print("----IN HIGHLIGHT FUNCTION----")
    #print(tableName)
    #print(messageText)

    conn = None
    try:

        """ Connect to the PostgreSQL database server """
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        # execute a statement
        # cur.execute(command)

        # working insert
        #insertcommand = "INSERT INTO poasts " + "(LINK) VALUES ('" + messageText + "');"
        
        insertcommand = "INSERT INTO poasts (ID, CONTENT, TITLE, DELETED, DATE_UPLOADED, VIEWS) VALUES ('" + postID + "', " + "'" + messageText + "'" + ", 'test title', null," + "'" + time.strftime('%Y-%m-%d %H:%M:%S') + "'" + ", '1');"
        print(insertcommand)
        try:
            cur.execute(insertcommand)
        except:
            pass

        cur.close()
        conn.commit()
        print("Success. Added " + messageText + " to highlights")
        return "Added!"

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        # return error

    finally:
        if conn is not None:
            conn.close()















if __name__ == '__main__':
    app.run(debug=True)
