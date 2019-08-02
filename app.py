#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, flash, request, redirect, render_template
import sys, os, train_model, predict_model
import urllib.request
from werkzeug.utils import secure_filename

app = Flask(__name__)

ENVIRONMENT_WINDOWS = False

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/predict', methods=['GET','POST'])
def predict_ui():
    if request.method == 'POST':
        # check if the post request has the file part
        print (request.form)
        username = request.form['username']
        experiment_name = request.form['experiment_name']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save('../data/{}/{}/predicting/{}'.format(username, experiment_name, filename))
            print('File successfully uploaded')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)
            
    return render_template('upload.html')


@app.route('/experiments/<user>', methods=['GET'])
def get_experiments(user):
    user = user.lower()

    file_dir_data = os.listdir('../data/')
    if user not in file_dir_data:
        return make_response(jsonify({'error':'User Not Found'}), 404)
    
    else:
        file_dir_user = os.listdir('../data/{}'.format(user))
        return jsonify({"user":user, "experiments":file_dir_user})
    return render_template('upload.html')

@app.route('/api/v1.0/predict/<user>/<experiment_name>/<query_file>', methods=['GET'])
def predict_experiment(user, experiment_name, task_id):
    user = user.lower()
    experiment_name = experiment_name.lower()
    
    file_dir_data = os.listdir('../data/')
    if user not in file_dir_data:
        return make_response(jsonify({'error':'User Not Found'}), 404)
    
    file_dir_user = os.listdir('../data/{}'.format(user))
    if experiment_name not in file_dir_user:
        return make_response(jsonify({'error':'Experiment Not Found'}), 404)

    model_def = '../data/{}/{}/model_definition.yaml'.format(user, experiment_name)
    
    return jsonify({"user":user, "response":task_id*5})

@app.route('/api/v1.0/train/<user>/<experiment_name>', methods=['GET'])
def train_experiment(user, experiment_name):
    user = user.lower()
    experiment_name = experiment_name.lower()
    
    file_dir_data = os.listdir('../data/')
    if user not in file_dir_data:
        return make_response(jsonify({'error':'User Not Found'}), 404)
    
    file_dir_user = os.listdir('../data/{}'.format(user))

    if experiment_name not in file_dir_user:
        return make_response(jsonify({'error':'Experiment Not Found'}), 404)

    model_def = '../data/{}/{}/model_definition.yaml'.format(user, experiment_name)
    data_csv = '../data/{}/{}/train_data.csv'.format(user, experiment_name)
    log_file = '../data/{}/{}/training.log'.format(user, experiment_name)
    if ENVIRONMENT_WINDOWS:
        output_dir = '..\data\{}\{}'.format(user, experiment_name)
    else:
        output_dir = '../data/{}/{}'.format(user, experiment_name)

    res = train_model.train_model(model_def, output_dir, data_csv, experiment_name, log_file)

    if res != True:
        return jsonify({"user":user, "response":res, "model_definition":model_def, "data_csv": data_csv, "log_file":log_file, "output_dir":output_dir})
        
    return jsonify({"user":user, "response":"Training in Progress"})

@app.route('/api/v1.0/register/<user>', methods=['GET'])
def register_user(user):
    user = user.lower()
    dir_list_users = os.listdir('../data/')
    if user in dir_list_users:
        return make_response(jsonify({'error':'User Already Exists'}), 420)
    else:
        os.mkdir("../data/{}".format(user))
        return jsonify({"user":user, "response":"User Successfully Created"})

@app.route('/api/v1.0/register/<user>/<experiment_name>', methods=['GET'])
def register_experiment(user, experiment_name):
    user = user.lower()
    experiment_name = experiment_name.lower()

    dir_list_users = os.listdir('../data/')
    if user in dir_list_users:
        dir_list_experimemnts = os.listdir('../data/{}/'.format(user))
        if experiment_name in dir_list_experiments:
            return make_response(jsonify({'error':'Experiment Already Exists'}), 420)
        else:
            os.mkdir('../data/{}/{}'.format(user, experiment_name))
            return jsonify({"user":user, "response":"Experiment Successfully Created"})
    else:
        return make_response(jsonify({'error':'User Does Not Exist'}), 420)

@app.route('/api/v1.0/remove/<user>', methods=['GET'])
def remove_user(user):
    user = user.lower()
    dir_list_users = os.listdir('../data/')
    if user not in dir_list_users:
        return make_response(jsonify({'error':'User Does Not Exist'}), 420)
    else:
        dir_list_experiments = os.listdir('../data/{}'.format(user))
        if len(dir_list_experiments) == 0:
            os.rmdir("../data/{}".format(user))
            return jsonify({"user":user, "response":"User Successfully Removed"})
        else:
            return jsonify({"user":user, "response":"User Experiments still exist", "experiments": dir_list_experiments})

@app.route('/api/v1.0/remove/<user>/<experiment_name>', methods=['GET'])
def remove_experiment(user,experiment_name):
    user = user.lower()
    experiment_name = experiment_name.lower()

    dir_list_users = os.listdir('../data/')
    if user in dir_list_users:
        dir_list_experiments = os.listdir('../data/{}/'.format(user))
        if experiment_name in dir_list_experiments:
            os.rmdir('../data/{}/{}'.format(user, experiment_name))
            return jsonify({"user":user, "response":"Experiment Successfully Removed"})
        else:
            return make_response(jsonify({'error':'Experiment Does Not Exist'}), 420)
    else:
        return make_response(jsonify({'error':'User Does Not Exist'}), 420)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Request Not Found'}), 404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='5001')