
from flask import Flask, render_template
import study

app = Flask(__name__)

study.load_data()


@app.route("/")
def home():
    courses = study.courses

    total_courses = len(courses)
    total_topics = 0 
    completed_topics = 0

    for topics in courses.values():
        total_topics += len(topics)

        for completed in topics.values():
            if completed:
                completed_topics += 1


    if total_topics > 0:
        progress = round(completed_topics / total_topics * 100)
    else:
        progress = 0


    return render_template(
        "index.html",
        courses=courses,
        total_courses=total_courses,
        total_topics=total_topics,
        completed_topics=completed_topics,
        progress=progress
    )