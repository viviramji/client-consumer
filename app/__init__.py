"""  
* UTB
* @author               Victor Victor Ramos J. href=<viviramji@gmail.com>
* Project:			    Client consumer
* Description:		    
*
* Changes (Version)
* _________________________________________
*
*               No.        Date            Author                    Description
*               ____    __________      __________________      _____________________________________
* @version      1.0     25/09/2020    	Victor Ramos         	  Initial implementation.
"""
import os
from flask import (
    Flask, jsonify, g, redirect, render_template, request, session, url_for
)

studentsDB = [
    {
        'id': 'T00055671',
        'name': 'Juan Perez',
        'course': 'Machine Learning'
    },
    {
        'id': 'T00045678',
        'name': 'Maria Martinez',
        'course': 'Software Engineer'
    }
]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/students', methods=['GET'])
    def get_all_students():
        """
        Obtiene todos los estudiantes
        """
        print(jsonify(studentsDB))
        return render_template('students/students.html', students=studentsDB)
        # return jsonify({'students': studentsDB})

    @app.route('/students/<stdId>', methods=['GET'])
    def get_student(stdId):
        """
        Obtiene un estudiante
        """
        user = [std for std in studentsDB if (std['id'] == stdId)]
        print(user)
        return render_template('students/student.html', student=user[0])
        # return jsonify({'est': usr})

    @app.route('/students/<stdId>', methods=['POST'])
    def update_students(stdId):
        row = [est for est in studentsDB if (est['id'] == stdId)]
        # print(type(row))

        row[0]['name'] = request.form['name']
        row[0]['course'] = request.form['course']

        return render_template('students/students.html', students=studentsDB)

    @app.route('/students', methods=['POST'])
    def create_student():
        """ 
        Crea un estudiante
        """
        print('called create user')
        dat = {
            'id': request.form['id'],
            'name': request.form['name'],
            'course': request.form['course']
        }
        studentsDB.append(dat)
        return render_template('students/students.html', students=studentsDB)

    @app.route('/students/<stdId>/delete', methods=['POST'])
    def deleteStudent(stdId):
        """ 
        Elimina un usuario
        """
        print(stdId)
        row = [est for est in studentsDB if (est['id'] == stdId)]
        if len(row) == 0:
            os.abort(404)
        studentsDB.remove(row[0])
        return redirect(url_for('get_all_students'))

    return app
