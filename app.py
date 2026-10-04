from flask import Flask, render_template, redirect, url_for, request
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


@app.route("/libros")
def libros():
    conn = get_db_connection()
    libros = conn.execute(
        "SELECT * FROM libros"
    ).fetchall()
    conn.close()

    return render_template("libros.html", libros=libros)


@app.route("/libro/nuevo", methods=['GET', 'POST'])
def nuevo_libro():

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']

        conn = get_db_connection()

        conn.execute(
            "INSERT INTO libros(titulo, autor) VALUES (?,?)",
            (titulo, autor)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('libros'))

    return render_template('form_libro.html')

@app.route("/libro/editar/<int:id>", methods=['GET', 'POST'])
def editar_libro(id):

    conn = get_db_connection()

    libro = conn.execute(
        "SELECT * FROM libros WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == 'POST':

        titulo = request.form['titulo']
        autor = request.form['autor']

        conn.execute(
            "UPDATE libros SET titulo=?, autor=? WHERE id=?",
            (titulo, autor, id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('libros'))

    conn.close()

    return render_template('form_libro.html', libro=libro)

@app.route("/libro/eliminar/<int:id>")
def eliminar_libro(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM libros WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('libros'))

@app.route("/prestamos")
def prestamos():

    conn = get_db_connection()

    prestamos = conn.execute(
        """
        SELECT p.id,
        p.fecha,
        l.titulo AS libro,
        le.nombre || ' ' || le.apellidos AS lector
        FROM prestamos p
        JOIN libros l ON p.libro_id = l.id
        JOIN lectores le ON p.lector_id = le.id
        """
    ).fetchall()

    conn.close()

    return render_template(
        'prestamos.html',
        prestamos=prestamos
    )

@app.route("/prestamo/nuevo", methods=['GET', 'POST'])
def nuevo_prestamo():

    conn = get_db_connection()

    if request.method == 'POST':

        fecha = request.form['fecha']
        lector_id = request.form['lector_id']
        libro_id = request.form['libro_id']

        conn.execute(
            """
            INSERT INTO prestamos
            (fecha, lector_id, libro_id)
            VALUES (?,?,?)
            """,
            (fecha, lector_id, libro_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('prestamos'))

    lectores = conn.execute(
        """
        SELECT id,
        nombre || ' ' || apellidos AS nombre
        FROM lectores
        """
    ).fetchall()

    libros = conn.execute(
        """
        SELECT id, titulo
        FROM libros
        """
    ).fetchall()

    conn.close()

    return render_template(
        'form_prestamo.html',
        lectores=lectores,
        libros=libros
    )


if __name__ == "__main__":
    app.run(debug=True)