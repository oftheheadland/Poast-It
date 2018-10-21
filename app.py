from flask import Flask, render_template, request, jsonify, make_response
from json import dumps
from string import Template
from collections import Counter
from datetime import datetime
import psycopg2
import os 
import random
import string

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']

HTML_TEMPLATE = Template("""
<h1>${note_ID}</h1>

			<textarea id="textbox" rows="4" cols="50">
			${content}
			</textarea>
""")


@app.route('/notes/<url_note_ID>')
def note_page(url_note_ID):
    foundContent = fetchFromTable(url_note_ID)

    return(HTML_TEMPLATE.substitute(note_ID=url_note_ID, content= foundContent))


    """
    note_ID = "rhuahdagwhhja"
    PULL FROM DB WHERE ID = note_ID
    RETURN CONTENT
    """


@app.route('/post/', methods=['POST'])
def poast():
    print(request.form.get('text', 0))    
    messageText = request.form.get('text', 0)
    generatedID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))


    print(addToTable(messageText, generatedID))
    return(generatedID)


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
        
        insertcommand = "INSERT INTO poasts (ID, CONTENT, TITLE, DELETED, DATE_UPLOADED, VIEWS) VALUES ('" + postID + "', " + "'" + messageText + "'" + ", 'test title', null, '2018-10-18 22:20:46', '1');"
        print(insertcommand)
        cur.execute(insertcommand)

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
