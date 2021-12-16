import csv
from datetime import date
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from students_to_go import model
from students_to_go.app import app
from utils import print_progress_bar

import_file = Path.home() / r"Dropbox/Гармония/2021-2022/списки/сверка январь/da549f9e04eea65aee3dba58619d1d56.csv"


def import_row(session: Session, row: dict):
    student = session.get(model.Student, row['ID ребенка'])
    if not student:
        student = model.Student(id=row['ID ребенка'],
                                name=' '.join((row['Фамилия ребенка'], row['Имя ребенка'])),
                                date_of_birth=date.fromisoformat(row['Дата рождения ребенка']))
        session.add(student)
    group = session.get(model.Group, row['ID группы'])
    if not group:
        program = session.execute(
            select(model.Program).filter_by(name=row['Программа'])).scalars().first()
        if not program:
            program = model.Program(name=row['Программа'])
            session.add(program)
        group = model.Group(id=row['ID группы'], name=row['Название группы'], program=program)
        session.add(group)
    order = model.Order(id=row['ID'], student=student, group=group)
    session.add(order)


def do_import(session: Session):
    with open(import_file, encoding='cp1251') as csvfile:
        rows = len(list(csv.DictReader(csvfile, delimiter=';')))
        csvfile.seek(0)
        csv_reader = csv.DictReader(csvfile, delimiter=';')
        for i, row in enumerate(csv_reader):
            print_progress_bar(i, rows)
            with session.begin():
                import_row(session=session, row=row)
        print_progress_bar(rows, rows)


def main():
    with app.app_context() as a:
        model.db.drop_all()
        model.db.create_all()
        do_import(model.db.session)


if __name__ == '__main__':
    exit(0)
    main()
