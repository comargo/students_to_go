from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.ForeignKey('students.id'))
    group_id = db.Column(db.ForeignKey('groups.id'))
    to_go = db.Column(db.Boolean, default=False)
    student = db.relationship("Student", back_populates="orders")
    group = db.relationship("Group", back_populates="orders")

    def __repr__(self):
        return f'Order(id={self.id}, student="{self.student.name}", group="{self.group.name}", to_go={self.to_go})'


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.String(length=36), primary_key=True)
    name = db.Column(db.String)
    date_of_birth = db.Column(db.Date)
    orders = db.relationship(Order, back_populates="student")
    groups = association_proxy('orders', 'group')

    def __repr__(self):
        return f'Student(name="{self.name}", date_of_birth="{self.date_of_birth}")'


class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True)
    groups = db.relationship("Group", back_populates="program")

    def __repr__(self):
        return f'Program(name="{self.name}")'


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    program_id = db.Column(db.ForeignKey(Program.id))
    program = db.relationship(Program, back_populates="groups")
    orders = db.relationship(Order, back_populates="group")
    students = association_proxy("orders", "student")

    def __repr__(self):
        return f'Group(name="{self.name}")'
