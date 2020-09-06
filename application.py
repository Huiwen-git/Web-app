# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 15:01:21 2020

@author: hwjia

web app
"""

import os
#import magic
import urllib.request
from flask import Flask, flash, request, redirect, render_template, send_file, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd





app = Flask(__name__)
UPLOAD_FOLDER = 'uploads\\'
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
#file_dir = 'E:\\Huiwen_Jia\\web-app\\uploads\\'
if not os.path.exists(file_dir):
    os.makedirs(file_dir)


ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generateresult(filename,file_dir):
    filepath=os.path.join(file_dir, filename)
    a=pd.read_csv(filepath, header=None)  # 读取训练数据
    b=2*a
    filedownloadpath=os.path.join(file_dir, 'download-'+filename.split('.')[0]+'.xlsx')
    return(b)

#@app.route("/")
#def home_form():
#	return render_template('home.html')



@app.route('/')
def upload_form():
	return render_template('upload.html')



@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        #if 'file' not in request.files:
        #    flash('No file part')
		#	return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(file_dir, filename))
			b=generateresult(filename,file_dir)
			flash('File successfully uploaded, the page will direct to the result soon!')
			downloadfilename = 'download'+filename
			b.to_csv(os.path.join(file_dir, downloadfilename))
			return render_template('simple.html',  tables=[b.to_html(classes='data')], titles=b.columns.values) #redirect('/download/<downloadfilename>')
		else:
			flash('Allowed file types csv')
			return redirect(request.url)


'''
@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    directory='static\client\csv'
    try:
        return send_from_directory(directory, filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
'''

        


