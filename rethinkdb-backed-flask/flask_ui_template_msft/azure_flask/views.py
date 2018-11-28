"""
Routes and views for the flask application.
"""
import pyodbc
import requests as r
from datetime import datetime
from flask import render_template, send_file, request, abort
from azure_flask import app
import json
import os
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
import matplotlib.pyplot as plt
import numpy as np

import io


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/data',  methods=['GET'])
def data():
    """Renders the data page."""
    raw_data = get_fused_news_data()
    return render_template(
        'data.html',
        title='Data',
        message='Give me your data.',
        image_name='some_image',
        news_data=loads(raw_data.content)
    )

@app.route('/add_data_form', methods=['GET'])
def add_data_form():
    """Presents form to add data."""
    return render_template(
        'add_data_form.html',
        title='Add Some Data',
        message='Give me your data.'
    )

@app.route('/image/<some_image>')
def image_render(some_image):

    plt.plot([1, 2, 3, 4], [1, 4, 200,5000])
    img = io.BytesIO()
    plt.savefig(img)
    img.seek(0)
    image = send_file(img, mimetype='image/png')
    return image




def get_fused_news_data():
    return r.get("http://localhost:5001/api/v1/fusednews")


@app.route('/add_fused_news_data',methods=["POST"])
def add_fused_news_data():
    fused_news_item = {'headline':request.form['headline'],'url':request.form['url']}

    try:
        result = r.post('http://localhost:5001/api/v1/fusednews', json=fused_news_item, )
        return 'success', 200
    except Exception as e:
        return abort(500)


