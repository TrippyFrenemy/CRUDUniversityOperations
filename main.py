import argparse
import datetime

from sqlalchemy.orm import sessionmaker
from models import Teacher, Group, Student, Subject, Mark
from sqlalchemy import create_engine

from config import URL


DATABASE_URL = URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# Teacher
def create_teacher(session, name):
    teacher = Teacher(name=name)
    session.add(teacher)
    session.commit()
    session.close()

def list_teachers(session):
    teachers = session.query(Teacher).all()
    for teacher in teachers:
        print(f"{teacher.id} - {teacher.name}")
    session.close()

def update_teacher(session, teacher_id, name):
    teacher = session.query(Teacher).get(teacher_id)
    if teacher:
        teacher.name = name
        session.commit()
    session.close()

def remove_teacher(session, teacher_id):
    teacher = session.query(Teacher).get(teacher_id)
    if teacher:
        session.delete(teacher)
        session.commit()
    session.close()

# Group
def create_group(session, name):
    group = Group(name=name)
    session.add(group)
    session.commit()

def list_groups(session):
    groups = session.query(Group).all()
    for group in groups:
        print(f"ID: {group.id}, Name: {group.name}")

def update_group(session, group_id, name):
    group = session.query(Group).get(group_id)
    if group:
        group.name = name
        session.commit()

def delete_group(session, group_id):
    session.query(Group).filter(Group.id == group_id).delete()
    session.commit()


# Student
def create_student(session, name, group_id):
    student = Student(name=name, group_id=group_id)
    session.add(student)
    session.commit()

def list_students(session):
    students = session.query(Student).all()
    for student in students:
        print(f"ID: {student.id}, Name: {student.name}, Group ID: {student.group_id}")

def update_student(session, student_id, name, group_id):
    student = session.query(Student).get(student_id)
    if student:
        student.name = name
        student.group_id = group_id
        session.commit()

def delete_student(session, student_id):
    session.query(Student).filter(Student.id == student_id).delete()
    session.commit()

# Mark
def create_mark(session, student_id, subject_id, mark, date):
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    mark = Mark(student_id=student_id, subject_id=subject_id, mark=mark, date=date_obj)
    session.add(mark)
    session.commit()

def list_marks(session):
    marks = session.query(Mark).all()
    for mark in marks:
        print(f"ID: {mark.id}, Student ID: {mark.student_id}, Subject ID: {mark.subject_id}, Mark: {mark.mark}, Date: {mark.date}")

def update_mark(session, mark_id, student_id, subject_id, mark, date):
    mark_obj = session.query(Mark).get(mark_id)
    if mark_obj:
        mark_obj.student_id = student_id
        mark_obj.subject_id = subject_id
        mark_obj.mark = mark
        mark_obj.date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        session.commit()

def delete_mark(session, mark_id):
    session.query(Mark).filter(Mark.id == mark_id).delete()
    session.commit()

# Subjects
def create_subject(session, name, teacher_id):
    teacher = session.query(Teacher).get(teacher_id)
    if teacher:
        new_subject = Subject(name=name, teacher_id=teacher_id)
        session.add(new_subject)
        session.commit()
        print(f"Subject '{name}' added with Teacher ID: {teacher_id}")
    else:
        print("Teacher not found.")

def list_subjects(session):
    subjects = session.query(Subject).all()
    for subject in subjects:
        print(f"ID: {subject.id}, Name: {subject.name}, Teacher ID: {subject.teacher_id}")

def update_subject(session, subject_id, name=None, teacher_id=None):
    subject = session.query(Subject).get(subject_id)
    if subject:
        if name:
            subject.name = name
        if teacher_id:
            subject.teacher_id = teacher_id
        session.commit()
        print(f"Subject with ID {subject_id} updated.")
    else:
        print("Subject not found.")

def remove_subject(session, subject_id):
    subject = session.query(Subject).get(subject_id)
    if subject:
        session.delete(subject)
        session.commit()
        print(f"Subject with ID {subject_id} removed.")
    else:
        print("Subject not found.")

def main():
    parser = argparse.ArgumentParser(description="University Database Management")
    # Common arguments
    parser.add_argument("-a", "--action", required=True, choices=['create', 'list', 'update', 'remove'],
                        help="CRUD actions: create, list, update, remove")
    parser.add_argument("-m", "--model", required=True, choices=['Teacher', 'Group', 'Student', 'Subject', 'Mark'],
                        help="Models: Teacher, Group, Student, Subject, Mark")

    # Arguments for name-based models (Teacher, Group, Student, Subject)
    parser.add_argument("-n", "--name", help="Name of the object")

    # Argument for identification of specific records
    parser.add_argument("--id", type=int, help="ID of the object to update/remove")

    # Arguments specific to the Mark model
    parser.add_argument("--student_id", type=int, help="Student ID for the mark")
    parser.add_argument("--subject_id", type=int, help="Subject ID for the mark")
    parser.add_argument("--mark", type=int, help="Mark to be added/updated")
    parser.add_argument("--date", help="Date when the mark was given, format: YYYY-MM-DD")

    # Arguments for models involving foreign keys
    parser.add_argument("--group_id", type=int, help="Group ID for Student/Subject")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID for Subject")

    args = parser.parse_args()
    session = Session()

    if args.model == "Teacher":
        if args.action == "create":
            create_teacher(session, args.name)
        elif args.action == "list":
            list_teachers(session)
        elif args.action == "update":
            update_teacher(session, args.id, args.name)
        elif args.action == "remove":
            remove_teacher(session, args.id)
        else:
            print("Invalid action")
    elif args.model == "Group":
        if args.action == "create":
            create_group(session, args.name)
        elif args.action == "list":
            list_groups(session)
        elif args.action == "update":
            update_group(session, args.id, args.name)
        elif args.action == "delete":
            delete_group(session, args.id)
        else:
            print("Invalid action")
    elif args.model == "Student":
        if args.action == "create":
            create_student(session, args.name, args.group_id)
        elif args.action == "list":
            list_students(session)
        elif args.action == "update":
            update_student(session, args.id, args.name, args.group_id)
        elif args.action == "delete":
            delete_student(session, args.id)
        else:
            print("Invalid action")
    elif args.model == "Mark":
        if args.action == "create":
            create_mark(session, args.student_id, args.subject_id, args.mark, args.date)
        elif args.action == "list":
            list_marks(session)
        elif args.action == "update":
            update_mark(session, args.id, args.student_id, args.subject_id, args.mark, args.date)
        elif args.action == "delete":
            delete_mark(session, args.id)
        else:
            print("Invalid action")
    elif args.model == "Subject":
        if args.action == "create":
            create_subject(session, args.name, args.teacher_id)
        elif args.action == "list":
            list_subjects(session)
        elif args.action == "update":
            update_subject(session, args.id, args.name, args.teacher_id)
        elif args.action == "remove":
            remove_subject(session, args.id)
        else:
            print("Invalid action")


if __name__ == "__main__":
    main()
