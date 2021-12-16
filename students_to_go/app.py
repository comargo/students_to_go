from flask import Flask

from . import views
from .model import db

app = Flask(__name__)
app.config.from_object('students_to_go.config')
db.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


app.add_url_rule('/programs/', view_func=views.ListPrograms.as_view('list_programs'))
app.add_url_rule('/programs/<int:program_id>', view_func=views.ListGroups.as_view('show_program'))
app.add_url_rule('/programs/<int:program_id>/groups', view_func=views.ListGroups.as_view('list_groups'))
app.add_url_rule('/programs/<int:program_id>/groups/<int:group_id>', view_func=views.ShowGroup.as_view('show_group'))
