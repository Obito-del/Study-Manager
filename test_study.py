import study
import json

# capsys when the program uses print(), it let's pytest collect the prints so the test can check them
def test_calculate_progress(capsys):
    study.courses = {
        "Python": {
            "Variables": True,
            "Loops": False
        }
    }


    study.calculate_progress()

    captured = capsys.readouterr()

    assert "Completed: 1 / 2 topics" in captured.out
    assert "Overall Progress: 50.0%" in captured.out


# monkeypatch let's me change things tmeporary, in this case "Python" is the temporary thing we can use it for testing
def test_search_courses(monkeypatch, capsys):
    study.courses = {
            "Python": {
                "Variables": True,
                "Loops": False
            }
    }

# lambda creates a small, unnamed function "_" is a parameter just like what function have
    monkeypatch.setattr("builtins.input", lambda _: "python")

    study.search_course()
    captured = capsys.readouterr()

    assert "Course found: Python" in captured.out
    assert "Variable" in captured.out
    assert "Loops" in captured.out


def test_add_course(monkeypatch, capsys):
    study.courses = {}
# iter creats an iterator which gives us values on at a time
    inputs = iter(["Python", "variables"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(study, "save_data", lambda: None)

    study.add_course()

    captured = capsys.readouterr()


    assert "Python" in study.courses
    assert study.courses["Python"]["Variables"] is False
    assert "added!" in captured.out



def test_duplicate_topic(monkeypatch, capsys):
    study.courses = {
        "Python": {
            "Variables": False
        }
    }

    inputs = iter(["Python", "Variables"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(study, "save_data", lambda: None)

    study.add_course()

    captured = capsys.readouterr()

    assert "already exists" in captured.out
    assert len(study.courses["Python"]) == 1


def test_search_no_match(monkeypatch, capsys):
    study.courses = {
            "Python": {
                "Variables": False
            }
        }

    monkeypatch.setattr("builtins.input", lambda _: "biology")

    study.search_course()
    captured = capsys.readouterr()
    assert "No matching course or topics found." in captured.out

# creating a temporary folder for testing
def test_load_data(tmp_path, monkeypatch):
    test_data = {
        "Python": {
            "Variables": True,
            "Loops": False
        }
    }
# json.dump converts pYthon into json formated text
# json.load reads the json text fro the file and converts it back into python
    file_path = tmp_path / "data.json"
    file_path.write_text(json.dumps(test_data))
# chdir means chang directory, tells what is the current folder
    monkeypatch.chdir(tmp_path)

    study.load_data()

    assert study.courses == test_data

def test_save_data(tmp_path, monkeypatch):
    study.courses = {
        "Python": {
            "Variables": True,
            "Loops": False
        }
    }

    monkeypatch.chdir(tmp_path)

    study.save_data()

    file_path = tmp_path / "data.json"
# write_text writes text into a file
# read_text ready from that file
    saved_data = json.loads(file_path.read_text())

    assert saved_data == study.courses

def test_complete_topic(monkeypatch, capsys):
    study.courses = {
        "Python": {"Variables": False}
    }

    inputs = iter(["Python", "Variables"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(study, "save_data", lambda: None)

    study.complete_topic()

    captured = capsys.readouterr()

    assert study.courses["Python"]["Variables"] is True
    assert "marked as completed!" in captured.out


def test_complete_topic_missing_course(monkeypatch, capsys):
    study.courses = {
        "Python": {
            "Variables": False
        }
    }

    monkeypatch.setattr("builtins.input", lambda _: "Biology")
    study.complete_topic()

    captured = capsys.readouterr()
    assert "not found" in captured.out.lower()


def test_load_data_missing_file(tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        study.courses = {"Old course": {"Old topic": True}}

        study.load_data()
        assert study.courses == {}


