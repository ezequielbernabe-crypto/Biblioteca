from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)


# funcion para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect("biblioteca.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return redirect(url_for('lectores'))


@app.route("/lectores")
def lectores():
    conn = get_db_connection()
    lectores = conn.execute(
        "SELECT * FROM lectores"
    ).fetchall()
    conn.close()

    return render_template("lectores.html", lectores=lectores)


if __name__ == "__main__":
    app.run(debug=True)