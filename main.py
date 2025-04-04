from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret_key"

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="*******",  
        database="MedicalDatabase"
    )

@app.route('/')
def index():
    return redirect(url_for('medicines'))

@app.route('/medicines')
def medicines():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Medicines")
    medicines = cursor.fetchall()
    connection.close()
    return render_template('medicines.html', medicines=medicines)

@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']

    if not name or not price:
        flash("Name and price are required!", "error")
        return redirect(url_for('medicines'))

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Medicines (name, description, price) VALUES (%s, %s, %s)", (name, description, price))
    connection.commit()
    connection.close()

    flash("Medicine added successfully!", "success")
    return redirect(url_for('medicines'))

@app.route('/delete_medicine/<int:medicine_id>', methods = ['POST'])
def delete_medicine(medicine_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Medicines WHERE id = %s", (medicine_id,))
    connection.commit()
    connection.close()

    flash("Medicine deleted successfully!", "success")
    return redirect(url_for('medicines'))

@app.route('/update_medicine', methods=['POST'])
def update_medicine():
    medicine_id = request.form['id']
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']

    if not name or not price:
        flash("Name and price are required!", "error")
        return redirect(url_for('medicines'))

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE Medicines SET name=%s, description=%s, price=%s WHERE id=%s", (name, description, price, medicine_id))
    connection.commit()
    connection.close()

    flash("Medicine updated successfully!", "success")
    return redirect(url_for('medicines'))

@app.route('/pacients')
def pacients():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Pacients")
    pacients = cursor.fetchall()
    connection.close()
    return render_template('pacients.html', pacients=pacients)

@app.route('/add_pacient', methods=['POST'])
def add_pacient():
    name = request.form['name']
    age = request.form['age']
    address = request.form['address']

    if not name or not age or not address:
        flash("All fields are required!", "error")
        return redirect(url_for('pacients'))

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Pacients (name, age, address) VALUES (%s, %s, %s)", (name, age, address))
    connection.commit()
    connection.close()

    flash("Pacient added successfully!", "success")
    return redirect(url_for('pacients'))

@app.route('/delete_pacient/<int:pacient_id>', methods=['POST'])
def delete_pacient(pacient_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Pacients WHERE id = %s", (pacient_id,))
    connection.commit()
    connection.close()

    flash("Pacient deleted successfully!", "success")
    return redirect(url_for('pacients'))

@app.route('/update_pacient', methods=['POST'])
def update_pacient():
    pacient_id = request.form['id']
    name = request.form['name']
    age = request.form['age']
    address = request.form['address']

    if not name or not age or not address:
        flash("All fields are required!", "error")
        return redirect(url_for('pacients'))

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE Pacients SET name=%s, age=%s, address=%s WHERE id=%s", (name, age, address, pacient_id))
    connection.commit()
    connection.close()

    flash("Pacient updated successfully!", "success")
    return redirect(url_for('pacients'))

@app.route('/assignments')
def assignments():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT mp.id, m.name, p.name, mp.dosage FROM Medicine_Pacient mp \n JOIN Medicines m ON mp.medicine_id = m.id \n JOIN Pacients p ON mp.pacient_id = p.id")
    assignments = cursor.fetchall()
    connection.close()
    return render_template('assignments.html', assignments=assignments)

@app.route('/add_assignment', methods=['POST'])
def add_assignment():
    medicine_name = request.form['medicine_name'].lower()
    pacient_name = request.form['pacient_name'].lower()
    dosage = request.form['dosage']

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM Medicines WHERE LOWER(name) = %s", (medicine_name,))
    medicine = cursor.fetchone()

    cursor.execute("SELECT id FROM Pacients WHERE LOWER(name) = %s", (pacient_name,))
    pacient = cursor.fetchone()

    if not medicine or not pacient:
        flash("Invalid medicine or pacient name!", "error")
        connection.close()
        return redirect(url_for('assignments'))

    cursor.execute("INSERT INTO Medicine_Pacient (medicine_id, pacient_id, dosage) VALUES (%s, %s, %s)", (medicine[0], pacient[0], dosage))
    connection.commit()
    connection.close()

    flash("Assignment added successfully!", "success")
    return redirect(url_for('assignments'))

@app.route('/delete_assignment/<int:assignment_id>', methods = ['POST'])
def delete_assignment(assignment_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Medicine_Pacient WHERE id = %s", (assignment_id,))
    connection.commit()
    connection.close()

    flash("Assignment deleted successfully!", "success")
    return redirect(url_for('assignments'))

@app.route('/update_assignment', methods=['POST'])
def update_assignment():
    assignment_id = request.form['id']
    medicine_name = request.form['medicine_name'].lower()
    pacient_name = request.form['pacient_name'].lower()
    dosage = request.form['dosage']

    connection = get_connection()
    cursor = connection.cursor()

    
    cursor.execute("SELECT id FROM Medicines WHERE LOWER(name) = %s", (medicine_name,))
    medicine = cursor.fetchone()

    
    cursor.execute("SELECT id FROM Pacients WHERE LOWER(name) = %s", (pacient_name,))
    pacient = cursor.fetchone()

    
    if not medicine or not pacient:
        flash("Invalid medicine or pacient name!", "error")
        connection.close()
        return redirect(url_for('assignments'))

    
    cursor.execute("""
        UPDATE Medicine_Pacient 
        SET medicine_id=%s, pacient_id=%s, dosage=%s 
        WHERE id=%s
    """, (medicine[0], pacient[0], dosage, assignment_id))

    connection.commit()
    connection.close()

    flash("Assignment updated successfully!", "success")
    return redirect(url_for('assignments'))

if __name__ == '__main__':
    app.run(debug=True)
