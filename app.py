from flask_sqlalchemy import SQLAlchemy
from flask import Response

app = Flask(__name__)
app.config[‘SQLALCHEMY_DATABASE_URI’] = os.environ[‘DATABASE_URL’]
app.config[‘DEBUG’] = True
app.config[‘SQLALCHEMY_TRACK_MODIFICATIONS’] = False

# Create our database model
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String,             unique=True,nullable=False,primary_key=True)
    embedding = db.Column(db.String, unique=False, nullable=False)
def __init__(self, id, embedding):
        self.id = id
        self.embedding = embedding

db = SQLAlchemy(app)
db.init_app(app)

# Create our database model
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    embedding = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, id, embedding):
        self.id = id
        self.embedding = embedding


db.create_all()
db.session.commit()


@app.route('/Welcome')
def Welcome():
    return render_template('Welcome.html')


@app.route('/authenticate', methods=['POST'])
def authenticate():
    if (request.form['UserId'] == ''):
        return jsonify("Please provide Registration User ID")

    if not request.files.get('Signature', None):
        return jsonify("Please provide Signature Image")

    userid = request.form['UserId']
    signimage = request.files['Signature']

    if db.session.query(Users).filter_by(id=userid).scalar() is not None:
        embed = torch.Tensor(json.loads(Users.query.filter_by(id=userid).first().embedding))
        return jsonify(
            "Score: " + str('{:0.3f}'.format(F.pairwise_distance(PhiNet(PreProcess(signimage)), embed).item())))

    else:
        return jsonify("User isn't Registered!")


@app.route('/register', methods=['POST'])
def register():
    if (request.form['UserId'] == ''):
        return jsonify("Please provide Registration User ID")

    if not request.files.get('Signature', None):
        return jsonify("Please provide Signature Image")

    userid = request.form['UserId']
    signimage = request.files['Signature']

    if db.session.query(Users).filter_by(id=request.form['UserId']).scalar() is not None:
        return jsonify("User is already registered!")
    else:
        user = Users(id=str(userid), embedding=json.dumps(PhiNet(PreProcess(signimage)).data.tolist()))
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify("User: " + str(user) + " has been successfully registered")

        except Exception as e:
            print("Failed to add id and embedding")
            print(e)


@app.route('/check', methods=['GET'])
def check():
    print(Users)
    return jsonify({i: user for i, user in enumerate(Users)})