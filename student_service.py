from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    con = sqlite3.connect("university.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (student_id,))
    row = cur.fetchone()
    con.close()
    if row:
        return jsonify({"id": row[0], "name": row[1], "age": row[2], "eligible_courses": row[3]})
    return jsonify({"error": "Student not found"}), 404

@app.route('/students/<int:student_id>/eligibility/<string:course_id>', methods=['GET'])
def check_eligibility(student_id, course_id):
    con = sqlite3.connect("university.db")
    cur = con.cursor()
    cur.execute("SELECT eligible_courses FROM students WHERE id=?", (student_id,))
    row = cur.fetchone()
    con.close()
    if row and course_id in row[0].split(","):
        return jsonify({"eligible": True})
    return jsonify({"eligible": False})

if __name__ == '__main__':
    app.run(port=5001)
