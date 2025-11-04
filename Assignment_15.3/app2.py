from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for students
students = {}
next_id = 1

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(list(students.values()))

@app.route('/students', methods=['POST'])
def add_student():
    global next_id
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
        
    new_student = {
        "id": next_id,
        "name": data["name"],
        "age": data.get("age"),
        "grade": data.get("grade")
    }
    
    students[next_id] = new_student
    next_id += 1
    return jsonify(new_student), 201

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404
        
    data = request.get_json()
    student = students[id]
    
    student["name"] = data.get("name", student["name"])
    student["age"] = data.get("age", student["age"])
    student["grade"] = data.get("grade", student["grade"])
    
    return jsonify(student)

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404
        
    deleted_student = students.pop(id)
    return jsonify(deleted_student)

if __name__ == '__main__':
    app.run(debug=True)