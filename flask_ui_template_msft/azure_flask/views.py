"""
Routes and views for the flask application.
"""
import pyodbc
import requests as r
from datetime import datetime
from flask import render_template, send_file
from azure_flask import app
import json
import os
from pymongo import MongoClient
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


@app.route('/data')
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