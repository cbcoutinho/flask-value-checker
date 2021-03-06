from io import BytesIO
from flask import Flask, request
from helper import Invigilator

app = Flask(__name__)
app.config["TESTING"] = True

test_restriction_code = """
    # some simple data for tests here
    firstName : str/lenlim(5, 15) # a random comment
    middleName : str/lenlim(5, inf)/optional
    lastName : str/optional
    email : str
    password : str/lenlim(8, 15)
    phone : str/lenlim(8, 15)
    age : int/lim(18, 99)
    height : float/lim(1, inf)/optional
    someNegativeFloat : float/optional/lim(-inf, 0)
"""

invigilator = Invigilator()


@app.route("/popo", methods=["POST"])
@invigilator.check(
    ["POST"],
    """
    name : str/lenlim(0, 5)
    place : str/lenlim(0, 10)
    animal : str/lenlim(0, 15)
    thing : str/lenlim(0, 20)
    fav_number : int/lim(-10, 10)/optional
    fav_decimal : float/lim(-1, 1)/optional
    """,
)
def popo():
    form = request.form
    return f"hi {form['name']} of {form['place']}, who likes {form['animal']}s and {form['thing']}s"


@app.route("/upload_file", methods=["POST"])
@invigilator.check(
    ["POST"],
    """
    param1 : str/accept(['test1','test2'])
    """,
)
def upload_file():
    file = request.files["file"]
    args = request.args
    return f"param1 {args['param1']} filename {file.filename} file contents {file.read().decode()}"


def test_upload_file():
    with app.test_client() as client:
        rv = client.post(
            "/upload_file?param1=test1",
            content_type="multipart/form-data",
            data={"file": (BytesIO(b"sample"), "sample.txt")},
        )

        assert rv.status_code == 200
        assert rv.data == b"param1 test1 filename sample.txt file contents sample"


def test_simple_flask():
    with app.test_client() as client:
        rv = client.post(
            "/popo",
            data={
                "name": "popo",
                "place": "some place",
                "animal": "panda",
                "thing": "block",
            },
        )

        assert rv.status_code == 200
        assert rv.data == b"hi popo of some place, who likes pandas and blocks"
