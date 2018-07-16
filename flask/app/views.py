from app import app
from flask import render_template, redirect, session, request, jsonify, url_for
from pca import get_2d_ingredients

@app.route('/')
def index():
    return render_template('index.html', ingredients_arr=get_2d_ingredients())
