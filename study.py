import json


courses = {}

def add_course():
        course_name = input("Course name: ").strip().title()
        topic_name = input("Topic name: ").strip().title()

        if not course_name or not topic_name:
            print("=========>Course name and topic cannot be empty")
            return

        if course_name not in courses:
            courses[course_name] = {}

        if topic_name in courses[course_name]:
            print(f"=========> Topic '{topic_name}' already exists in '{course_name}'.")
            return

        courses[course_name][topic_name] = False
        save_data()

        print(f"==========> Course '{course_name}' with topic '{topic_name}' added!")




def view_courses():
        if not courses:
            print("===========> \nYou haven't added any courses yet.")
            return


        print("\nYour COurses")
        print("============================ Courses  =======================")

        for course_name in courses:
            print(course_name)

            for topic_name, completed in courses[course_name].items():
                if completed:
                    print(f" ===========> [Completed👍] {topic_name}")
                else:
                    print(f" ===========> [Not Completed] {topic_name}")


def complete_topic():
        if not courses:
            print("=============> You haven't added any courses yet.")
            return

        course_name = input("Course name: ").strip().title()

        if course_name not in courses:
            print("=============> Course not found.")
            return

        topic_name = input("=============> Topic name to complete: ").strip().title()


        if topic_name not in courses[course_name]:
            print("==================>Topic not found in that course.")
            return


        courses[course_name][topic_name] = True
        save_data()
        print(f"==============> '{topic_name}' marked as completed!")


def calculate_progress():
    if not courses:
        print("============> You haven't added any courses yet.")
        return

    total_topics = 0
    completed_topics = 0

    for course_name in courses:
        for topic_name, completed in courses[course_name].items():
            total_topics += 1

            if completed:
                completed_topics += 1

    percentage = (completed_topics / total_topics) * 100

    print(f"==========> Completed: {completed_topics} / {total_topics} topics")
    print(f"===========> Overall Progress: {percentage:.1f}%")


def save_data():
    with open("data.json", "w") as file:
        json.dump(courses, file, indent=4)


def load_data():
    global courses

    try:
        with open("data.json", "r") as file:
            courses = json.load(file)
    except FileNotFoundError:
        courses = {}



def search_course():
    if not courses:
        print("============> You haven't added any courses yet.")
        return

    search_term = input("Search for a course or topic: ").strip().lower()

    if not search_term:
        print("========> Search cannot be empty.")
        return

    found = False

    for course_name in courses:
        if search_term in course_name.lower():
            print(f"========>Course found: {course_name}")

            for topic_name, completed in courses[course_name].items():
                if completed:
                    print(f" ===========> [Completed👍] {topic_name}")
                else:
                    print(f" ===========> [Not completed] {topic_name}")

            found = True

        for topic_name, completed in courses[course_name].items():
            if search_term in topic_name.lower():
                status = "Completed" if completed else "Not completed"
                print(f"Topic found: {topic_name} ({course_name}) - {status}")
                found = True


    if not found:
        print("===========> No matching course or topics found.")




def main():
    load_data()

    while True:
        print("\n➡️➡️➡️   Study Manager   ⬅️⬅️⬅️")
        print("1. Add a course and topic")
        print("2. View Courses")
        print("3. Mark a topic complete")
        print("4. See Progress")
        print("5. Search Topics and Courses")
        print("6. Exit")

        choice = input("Choose an Option: ")

        if choice == "1":
            add_course()
        elif choice == "2":
            view_courses()
        elif choice == "3":
            complete_topic()
        elif choice == "4":
            calculate_progress()
        elif choice == "5":
            search_course()
        elif choice == "6":
            print("Goodbye, bro! keep studying!")
            break
        else:
            print("Invalid choice. Please choose 1, 2, 3, 4, 5 or 6.")


if __name__ == "__main__":
    main()
