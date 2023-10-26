from sqlalchemy.orm import sessionmaker
from models import Group, Student, Teacher, Subject, Mark
from sqlalchemy import create_engine, func

from config import URL

DATABASE_URL = URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    session = SessionLocal()
    result = session.query(Mark.student_id, func.avg(Mark.mark).label('average_mark'))\
        .group_by(Mark.student_id)\
        .order_by(func.avg(Mark.mark).desc())\
        .limit(5).all()
    session.close()
    return result


# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_id):
    session = SessionLocal()
    result = session.query(Mark.student_id)\
        .filter(Mark.subject_id == subject_id)\
        .group_by(Mark.student_id)\
        .order_by(func.avg(Mark.mark).desc())\
        .first()
    session.close()
    return result


# 3. Знайти середній бал у групах з певного предмета.
def select_3(subject_id):
    session = SessionLocal()
    result = session.query(Student.group_id, func.avg(Mark.mark))\
        .join(Mark, Mark.student_id == Student.id)\
        .filter(Mark.subject_id == subject_id)\
        .group_by(Student.group_id).all()
    session.close()
    return result


# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    session = SessionLocal()
    result = session.query(func.avg(Mark.mark)).scalar()
    session.close()
    return result


# 5. Знайти які курси читає певний викладач.
def select_5(teacher_id):
    session = SessionLocal()
    result = session.query(Subject.name).filter_by(teacher_id=teacher_id).all()
    session.close()
    return result


# 6. Знайти список студентів у певній групі.
def select_6(group_id):
    session = SessionLocal()
    result = session.query(Student.name).filter_by(group_id=group_id).all()
    session.close()
    return result


# 7. Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_id, subject_id):
    session = SessionLocal()
    result = session.query(Student.name, Mark.mark).join(Mark).filter(
        Student.group_id == group_id,
        Mark.subject_id == subject_id
    ).all()
    session.close()
    return result


# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_id):
    session = SessionLocal()
    result = session.query(func.avg(Mark.mark)).join(Subject).filter(
        Subject.teacher_id == teacher_id
    ).scalar()
    session.close()
    return result


# 9. Знайти список курсів, які відвідує певний студент.
def select_9(student_id):
    session = SessionLocal()
    result = session.query(Subject.name).join(Mark).filter(
        Mark.student_id == student_id
    ).distinct().all()
    session.close()
    return result


# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(student_id, teacher_id):
    session = SessionLocal()
    result = session.query(Subject.name).join(Mark).filter(
        Mark.student_id == student_id,
        Subject.teacher_id == teacher_id
    ).distinct().all()
    session.close()
    return result


if __name__ == "__main__":
    print(select_1())
    print(select_2(3))
    print(select_3(3))
    print(select_4())
    print(select_5(1))
    print(select_6(2))
    print(select_7(2, 3))
    print(select_8(1))
    print(select_9(4))
    print(select_10(4, 1))