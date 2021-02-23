from flask import Flask, render_template, request
import sqlite3
import secrets


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS meeting (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, email TEXT, password TEXT, url TEXT)')
    conn.close()

init_sqlite_db()


app = Flask(__name__)

@app.route('/')
@app.route('/sign-up/')
def enter_new_student():
    return render_template('sign-up.html')


@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        msg = None
        try:
            name = request.form['name']
            surname = request.form['surname']
            email = request.form['email']
            password = request.form['password']
            url = 'https://mydomain.com/reset=' + secrets.token_urlsafe()

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO meeting (name, surname, email, password, url) VALUES (?, ?, ?, ?, ?)", (name, surname, email, password, url))
                con.commit()
                msg = name + " was successfully added to the database."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            con.close()
            return render_template('chat.html', msg=msg)

@app.route('/show-results/', methods=["GET"])
def show_results(request):
    current_user = str(request.id)
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT name, email, url OF CURRENT USER FROM meeting WWHERE id = %s",[current_user])
            results = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
        return render_template('records.html', records=results)
















# @app.route('/delete-student/<int:student_id>/', methods=["GET"])
# def delete_student(student_id):

#     msg = None
#     try:
#         with sqlite3.connect('database.db') as con:
#             cur = con.cursor()
#             cur.execute("DELETE FROM student WHERE id=" + str(student_id))
#             con.commit()
#             msg = "A record was deleted successfully from the database."
#     except Exception as e:
#         con.rollback()
#         msg = "Error occurred when deleting a student in the database: " + str(e)
#     finally:
#         con.close()
#         return render_template('delete-success.html', msg=msg)
