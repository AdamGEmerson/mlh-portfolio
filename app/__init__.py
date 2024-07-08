import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict


load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(
    os.getenv('MYSQL_DATABASE'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    host=os.getenv('MYSQL_HOST'),
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
            {"name": "Calligraphy", "description": "Practicing beautiful handwriting and letter design.", "image": "./static/img/57810812c56f8f67b043e6c95a802408.jpg"},
            {"name": "Painting", "description": "Experimenting with colors and techniques on canvas.", "image": "./static/img/painting.jpeg"}
        ],
        "Active and Culinary": [
            {"name": "Basketball", "description": "Playing games and staying active on the court.", "image": "./static/img/MBB-WBB_BallHoop.jpeg"},
            {"name": "Cooking/Baking", "description": "Trying out new recipes and baking delicious treats.", "image": "./static/img/cooking.jpg"}
        ],
    }
    return render_template('hobbies.html', hobbies=hobbies, menu=active_menu(nav_menu, '/hobbies'))


experience_data = [
    {
        'title': 'MLH Fellow - SWE/SRE DevOps Intern',
        'company': 'MLH Fellowship',
        'location': 'Remote',
        'dates': 'June 2024 - Present',
        'description': 'MLH Fellow working as a SWE/SRE DevOps Intern at Meta.',
    },
    {
        'title': 'Software Engineer',
        'company': 'AI Healthcare Startup',
        'location': 'Remote',
        'dates': 'May 2024 - Present',
        'description': 'Partnered with Google and Amazon Developers on healthcare solution startup. Utilized React & Tailwind components to initialize the webpage using 500+ crucial lines of code. Next.js, Tailwind, git, GitHub, Cloud dev, Web development, markdown, Firebase.',
    },
    {
        'title': 'Artificial Intelligence Engineer Intern',
        'company': 'Radical AI',
        'location': 'Remote',
        'dates': 'February 2024 - May 2024',
        'description': 'Proactively engaged in code reviews, debugging, and troubleshooting, resulting in a 10% reduction in system errors. Demonstrated proficiency in both front-end and back-end development, utilizing JS, Tailwind, and PostgreSQL. Developed ReX, an AI Coach utilizing technologies like OpenAI, Vertex AI, and TensorFlow.',
    },
    {
        'title': 'Software Engineer Intern',
        'company': 'Woojoo Universe',
        'location': 'Remote',
        'dates': 'December 2023 - April 2024',
        'description': 'Significantly contributed to cross-platform mobile app development (React.js, React Native, Java) with a notable 30% increase in user engagement. Implemented GraphQL for 25% faster data querying and enhanced SQL database efficiency by 10%. Conducted API testing with Insomnia, ensuring a remarkable 95% error-free interface and streamlining build processes.',
    },
    {
        'title': 'Software Engineer',
        'company': 'Upwork',
        'location': 'Irving, Texas',
        'dates': 'August 2022 - December 2023',
        'description': 'Designed, debugged, and built software applications, maintaining high code quality and performance standards. Collaborated with engineers to architect, implement, and test new features, contributing to the platform\'s evolution. Engaged in agile development practices, ensuring regular software releases and alignment with business objectives.',
    },
]

@app.route('/experience')
def experience():
    return render_template('experience.html', title="Experience", url=os.getenv("URL"), menu=active_menu(nav_menu, '/experience'), experience=experience_data)


@app.route('/education')
def education():
    education = [
        {
            "degree": "Bachelor of Science, Computer Science",
            "institution": "University of Texas at Dallas",
            "location": "Irving, Texas",
            "dates": "Graduation May 2024",
            "description": "Relevant Coursework: Introduction to Computer Science, Programming Fundamentals l, Discrete Math, Calculus l & ll, Linear Algebra, Codepath TIP 102 (Data Structures and Algorithms)"
        },
        {
            "degree": "Bootcamp, Computer Science",
            "institution": "University of California at Irvine",
            "location": "Remote",
            "dates": "Graduated September 2023",
            "description": ""
        },
        {
            "degree": "Intermiadiate Technical Interview Course",
            "institution": "Codeapath",
            "location": "Remote",
            "dates": "Expected September 2024",
            "description": "Deep dive into Data Structures, Algorithms, and System Design. Learning to solve technical interview questions with clarity."
        }
    ]
    return render_template('education.html', education=education, menu=active_menu(nav_menu, '/education'))


@app.route('/api/timeline_post', methods=['POST'])
def post_timeline_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePosts.create(name=name, email=email, content=content)

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
