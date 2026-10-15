
from flask import Flask, render_template, request, redirect, url_for
import study

app = Flask(__name__)

study.load_data()


@app.route("/")
def home():
    courses = study.courses
    course_progress = {}

    total_courses = len(courses)
    total_topics = 0 
    completed_topics = 0

    for course, topics in courses.items():
        total_topics += len(topics)

        course_completed = 0 

        for completed in topics.values():
            if completed:
                completed_topics += 1
                course_completed += 1

        if len(topics) > 0:
            course_progress[course] = round(
                course_completed / len(topics) * 100
            )

        else:
            course_progress[course] = 0


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
        progress=progress,
        course_progress=course_progress
)

@app.route("/add_course", methods=["POST"])
def add_course_web():
    course_name = request.form.get("course_name", "").strip().title()
    topic_name = request.form.get("topic_name", "").strip().title()


    if not course_name or not topic_name:
        return redirect(url_for("home"))

    if course_name not in study.courses:
        study.courses[course_name] = {}

    if topic_name in study.courses[course_name]:
        return redirect(url_for("home"))

    study.courses[course_name][topic_name]  = False
    study.save_data()

    return redirect(url_for("home"))

@app.route("/complete_topic", methods=["POST"])
def completed_topic_web():
    course_name = request.form.get("course_name", "")
    topic_name = request.form.get("topic_name", "")

    if course_name not in study.courses:
        return redirect(url_for("home"))
    if topic_name not in study.courses[course_name]:
        return redirect(url_for("home"))

    study.courses[course_name][topic_name] = True
    study.save_data()

    return redirect(url_for("home"))
