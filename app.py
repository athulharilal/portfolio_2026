from flask import Flask, render_template, abort
import requests
import json
import os

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def load_data():
    try:
        data_path = os.path.join(app.root_path, 'data', 'profile.json')
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.context_processor
def inject_data():
    # Inject profile data into all templates
    return dict(profile=load_data())

@app.route('/')
def home():
    return render_template('home.html', page='home')

@app.route('/experience')
def experience():
    return render_template('experience.html', page='experience')

@app.route('/projects')
def projects():
    return render_template('projects.html', page='projects')

@app.route('/blog')
def blog():
    # Fetch articles from Dev.to API
    try:
        response = requests.get('https://dev.to/api/articles?username=athulharilal')
        articles = response.json()
    except:
        articles = []
    return render_template('blog.html', page='blog', articles=articles)

@app.route('/contact')
def contact():
    # In a real app, this would handle form submission
    return render_template('contact.html', page='contact')

if __name__ == '__main__':
    app.run(debug=True)
