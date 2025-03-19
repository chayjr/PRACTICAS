from flask import Flask, render_template,request,redirect, url_for 
import mysql.connector

app = Flask(__name__)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="inventario"
    )

#Metodo para selecionar y mostrar los datos de la tabla 
@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    miresultado = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column [0] for column in cursor.description]
    for record in miresultado:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    conn.close()
    return render_template("index.html", dato=insertObject)

#Meodo de Agregar
@app.route("/add", methods=["POST"])
def add():
    Producto = request.form["producto"]
    Cantidad = int(request.form["cantidad"])  # Convertimos cantidad a entero
    Precio = int(request.form["precio"])  # Convertimos precio a entero
    P_obsoleto = (request.form["p_obsoleto"])
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (producto, cantidad, precio, p_obsoleto) VALUES (%s, %s, %s, %s)", (Producto, Cantidad, Precio, P_obsoleto))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("home"))

#Metodo para actualizar
@app.route("/update/<string:id>", methods=["POST"])
def update(id):
    Producto = request.form["producto"]
    Cantidad = int(request.form["cantidad"])  # Convertimos cantidad a entero
    Precio = int(request.form["precio"])  # Convertimos precio a entero
    P_obsoleto = (request.form["p_obsoleto"])
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET producto = %s, cantidad = %s, precio = %s, p_obsoleto = %s WHERE id = %s", (Producto, Cantidad, Precio, P_obsoleto, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("home"))

#Metodo para eliminar
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("home"))
