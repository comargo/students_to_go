from flask import render_template
from flask.typing import ResponseReturnValue
from flask.views import View

from students_to_go.model import Program, Group


class ListPrograms(View):
    def dispatch_request(self) -> ResponseReturnValue:
        programs = Program.query.all()
        return render_template('list_programs.html', programs=programs)


class ListGroups(View):
    def dispatch_request(self, program_id) -> ResponseReturnValue:
        program = Program.query.get(program_id)
        return render_template('list_groups.html', program=program)


class ShowGroup(View):
    def dispatch_request(self, program_id, group_id) -> ResponseReturnValue:
        group = Group.query.get(group_id)
        return render_template('show_group.html', group=group)
