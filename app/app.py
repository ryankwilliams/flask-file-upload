import os
from random import randint

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# volume settings
VOLUME_PATH = '/mnt/app'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'mysql://root:password@db/kingbob'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class FileEntry(db.Model):
    """Simple file entry class."""
    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(db.Integer, unique=True, nullable=False)
    file = db.Column(db.String(100), unique=True, nullable=False)
    file_path = db.Column(db.String(100), unique=True, nullable=False)


@app.route('/upload_yml', methods=['POST'])
def upload_yml():
    """Upload a yaml file."""

    # get uploaded file bytes
    fh = request.files['file']

    # generate upload id
    _id = randint(1, 100000)

    # generate file name
    file_name = '%s.yml' % _id

    # generate absolute file path
    file_path = os.path.join(VOLUME_PATH, file_name)

    # write file to storage
    fh.save(file_path)

    # add entry into database
    file_entry = FileEntry(
        upload_id=_id,
        file=file_name,
        file_path=file_path
    )

    db.session.add(file_entry)
    db.session.commit()

    return 'FILE UPLOADED SUCCESSFULLY'


if __name__ == '__main__':
    # create database entries
    db.create_all()

    # run flask application
    app.run(host='0.0.0.0')
