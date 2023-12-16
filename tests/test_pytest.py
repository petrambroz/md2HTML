from src import runner

r = runner.runner("cs", "title")


def test_2():
    string = "čau jardo, <i>it</i> ale <em>bd</em>, <code>code</code>?"
    assert r.parseline("čau jardo, *it* ale **bd**, `code`?") == string


def test_1():
    string = "ahoj * ahoj"
    assert r.parseline("ahoj * ahoj") == string


def test_3():
    string = "ahoj * ahoj <em>ahoj</em>"
    assert r.parseline("ahoj * ahoj **ahoj**") == string
