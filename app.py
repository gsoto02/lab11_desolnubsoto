from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "lab11-jfarfan-2026"

DB = "contactos.db"

def get_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with get_db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS contactos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                direccion TEXT
            )
        """)

@app.route("/")
def index():
    q = request.args.get("q", "")
    with get_db() as con:
        if q:
            contactos = con.execute(
                "SELECT * FROM contactos WHERE nombre LIKE ? OR email LIKE ? OR telefono LIKE ?",
                (f"%{q}%", f"%{q}%", f"%{q}%")
            ).fetchall()
        else:
            contactos = con.execute("SELECT * FROM contactos ORDER BY nombre").fetchall()
    return render_template("index.html", contactos=contactos, q=q)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        if not nombre:
            flash("El nombre es obligatorio.", "error")
            return redirect(url_for("agregar"))
        with get_db() as con:
            con.execute(
                "INSERT INTO contactos (nombre, telefono, email, direccion) VALUES (?,?,?,?)",
                (nombre, request.form["telefono"], request.form["email"], request.form["direccion"])
            )
        flash(f"Contacto '{nombre}' agregado correctamente.", "success")
        return redirect(url_for("index"))
    return render_template("form.html", contacto=None, accion="Agregar")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    with get_db() as con:
        contacto = con.execute("SELECT * FROM contactos WHERE id=?", (id,)).fetchone()
    if not contacto:
        flash("Contacto no encontrado.", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        with get_db() as con:
            con.execute(
                "UPDATE contactos SET nombre=?, telefono=?, email=?, direccion=? WHERE id=?",
                (nombre, request.form["telefono"], request.form["email"], request.form["direccion"], id)
            )
        flash(f"Contacto actualizado.", "success")
        return redirect(url_for("index"))
    return render_template("form.html", contacto=contacto, accion="Editar")

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    with get_db() as con:
        con.execute("DELETE FROM contactos WHERE id=?", (id,))
    flash("Contacto eliminado.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    # 0.0.0.0 para que sea accesible desde fuera (necesario en AWS)
    app.run(host="0.0.0.0", port=5000, debug=True)
