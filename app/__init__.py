import os
from flask import Flask, render_template, request
from datetime import datetime as DateTime
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict


load_dotenv()
app = Flask(__name__)

if os.getenv('TESTING') == "true":
    print('Running in test mode')
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        port=3306
    )

print(mydb)


class TimelinePosts(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField()

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePosts])

# Links declared for dynamic rendering in template
nav_menu = [
    {'name': 'Home', 'url': '/'},
    {'name': 'Hobbies', 'url': '/hobbies'},
    {'name': 'Experience', 'url': '/experience'},
    {'name': 'Education', 'url': '/education'},
    {'name': 'Timeline', 'url': '/timeline'}
]


# Function that sets one link to active based on the rendered page
def active_menu(menu, url):
    for item in menu:
        if item['url'] == url:
            item['active'] = True
        else:
            item['active'] = False
    return menu


@app.route('/')
def index():
    google_api_key = os.getenv('google_api_key')
    print(active_menu(nav_menu, '/'))
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), menu=active_menu(nav_menu, '/'), google_api_key=google_api_key)


@app.route('/hobbies')
def hobbies():
    hobbies = {
        "Creative Pursuits": [
            {"name": "Graphic Design", "description": "UI and UX Design", "image": "./static/img/graphic-design.jpg"},
            {"name": "Crosswords", "description": "Staying sharp by solving (and creating) puzzles.", "image": "./static/img/crossword.jpeg"}
        ],
        "Active and Culinary": [
            {"name": "Bouldering/Climbing", "description": "Challenging myself with a good bouldering route.", "image": "./static/img/bouldering.jpeg"},
            {"name": "Cooking/Baking", "description": "Trying out new recipes and baking delicious treats.", "image": "./static/img/cooking.jpg"}
        ],
    }
    return render_template('hobbies.html', hobbies=hobbies, menu=active_menu(nav_menu, '/hobbies'))


experience_data = [
    {
        'title': 'MLH Fellow - Production Engineering',
        'company': 'MLH Fellowship',
        'location': 'Remote',
        'dates': 'June 2024 - Present',
        'description': 'MLH Fellow working as a PE DevOps Intern with Meta.',
    },
    {
        'title': 'Research Assistant - Hybrid Design and Digital Fabrication',
        'company': 'The Hybrid Atelier',
        'location': 'University of Texas at Arlington',
        'dates': 'May 2023 - January 2024',
        'description': 'Worked as a research assistant in the Hybrid Atelier lab, focusing on digital fabrication and hybrid design.',
    },
]

@app.route('/experience')
def experience():
    return render_template('experience.html', title="Experience", url=os.getenv("URL"), menu=active_menu(nav_menu, '/experience'), experience=experience_data)


@app.route('/education')
def education():
    education = [
        {
            "degree": "Bachelor of Science, Software Engineering",
            "institution": "University of Texas at Arlington",
            "location": "Arlington, Texas",
            "dates": "August 2024",
            "description": "Relevant Coursework: Data Structures & Algorithms, Software Design Patterns, Calculus 3, Software Engineering, Computer Architecture, Operating Systems, Database Systems, and more."
        },
        {
            "degree": "Associates of Science, Engineering",
            "institution": "Tarrant County College",
            "location": "Fort Worth, Texas",
            "dates": "September 2022",
            "description": ""
        }
    ]
    return render_template('education.html', education=education, menu=active_menu(nav_menu, '/education'))


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
    except KeyError:
        return "Invalid name", 400

    try:
        email = request.form['email']
    except KeyError:
        return "Invalid email", 400

    try:
        content = request.form['content']
    except KeyError:
        return "Invalid content", 400

    name = request.form['name']

    email = request.form['email']
    # Validate email
    if not email or '@' not in email:
        return "Invalid email", 400

    content = request.form['content']
    # Check content
    if not content:
        return "Invalid content", 400

    timeline_post = TimelinePosts.create(name=name, email=email, content=content, created_at=DateTime.now())

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_post():
    return {
        'timeline_posts': [
            model_to_dict(timeline_post) for timeline_post in TimelinePosts.select()
            .order_by(TimelinePosts.created_at.desc())
        ]
    }


@app.route('/api//timeline_post', methods=['DELETE'])
def delete_timeline_post():

    id = request.form['id']
    timeline_post = TimelinePosts.get(TimelinePosts.id == id)
    timeline_post.delete_instance()

    return model_to_dict(timeline_post)


@app.route('/timeline')
def timeline():
    return render_template('timeline.html', Title="Timeline", entries=TimelinePosts.select().order_by(TimelinePosts.created_at.desc()), menu=active_menu(nav_menu, '/timeline'))
