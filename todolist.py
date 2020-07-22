from sqlalchemy import create_engine  # creates a database file
from sqlalchemy.ext.declarative import declarative_base  # creates a table in the database
from sqlalchemy import Column, Integer, String, Date  # creates a table in the database
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker  # allows to access the database

engine = create_engine('sqlite:///todo.db?check_same_thread=False')  # creates the database

Base = declarative_base()  # creates the table

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field

Base.metadata.create_all(engine)

# these two lines access the database
Session = sessionmaker(bind=engine)
session = Session()

def week_view(delta, query):
    print(f"{(datetime.today().date() + timedelta(days=delta)).strftime('%A %d %b')}:")
    if not query:
        print("Nothing to do!")
        print("")
    else:
        i = 0
        while i < len(query):
            row = query[i]
            print(f"{i + 1}. {row.task}")
            i += 1
        print("")

def menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")

def today():
    today_rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    print("")
    print(f"Today {datetime.today().strftime('%d %b')}:")
    if not today_rows:
        print("Nothing to do!")
        print("")
    else:
        i = 0
        while i < len(today_rows):
            row = today_rows[i]
            print(f"{i + 1}. {row.task}")
            i += 1
        print("")

def add():
    print("")
    print("Enter task")
    task = input()
    print("Enter deadline")
    deadline_entry = input().split('-')
    deadline = datetime(int(deadline_entry[0]), int(deadline_entry[1]), int(deadline_entry[2]))

    #  Adding a task
    new_row = Table(task=task,
                    deadline=datetime.strptime(deadline.strftime("%Y-%m-%d"), '%Y-%m-%d').date())
    session.add(new_row)
    session.commit()

    print("The task has been added!")
    print("")

def this_week():
    today_rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    tomorrow_rows = session.query(Table).filter(Table.deadline == datetime.today().date() + timedelta(days=1)).all()
    third_day_rows = session.query(Table).filter(Table.deadline == datetime.today().date() + timedelta(days=2)).all()
    fourth_day_rows = session.query(Table).filter(Table.deadline == datetime.today().date() + timedelta(days=3)).all()
    fifth_day_rows = session.query(Table).filter(Table.deadline == datetime.today().date() + timedelta(days=4)).all()
    sixth_day_rows = session.query(Table).filter(Table.deadline == datetime.today().date() + timedelta(days=5)).all()
    seventh_day_rows = session.query(Table).filter(Table.deadline == datetime.today().date() + timedelta(days=6)).all()

    print('')
    week_view(0, today_rows)
    week_view(1, tomorrow_rows)
    week_view(2, third_day_rows)
    week_view(3, fourth_day_rows)
    week_view(4, fifth_day_rows)
    week_view(5, sixth_day_rows)
    week_view(6, seventh_day_rows)

def all():
    rows = session.query(Table).order_by(Table.deadline).all()  # gets all rows from the table
    print("")
    print("All tasks:")
    if not rows:
        print("Nothing to do!")
        print("")
    else:
        i = 0
        while i < len(rows):
            row = rows[i]
            print(f"{i + 1}. {row.task}. {row.deadline.strftime('%d %b')}")
            i += 1
        print("")

def missed():
    missed_rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    print("")
    print("Missed tasks:")
    if not missed_rows:
        print("Nothing is missed!")
        print("")
    else:
        i = 0
        while i < len(missed_rows):
            row = missed_rows[i]
            print(f"{i + 1}. {row.task}. {row.deadline.strftime('%d %b')}")
            i += 1
        print("")

def delete():
    rows = session.query(Table).order_by(Table.deadline).all()
    if not rows:
        print("")
        print("No tasks to delete!")
        print("")
    else:
        print("")
        print("Choose the number of the task you want to delete:")
        i = 0
        while i < len(rows):
            row = rows[i]
            print(f"{i + 1}. {row.task}. {row.deadline.strftime('%d %b')}")
            i += 1
        to_delete = int(input())
        row_to_delete = rows[to_delete - 1]
        session.delete(row_to_delete)
        session.commit()
        print("The task has been deleted!")
        print("")

while True:
    menu()
    choice = int(input())
    if choice == 1:
        today()
    elif choice == 2:
        this_week()
    elif choice == 3:
        all()
    elif choice == 4:
        missed()
    elif choice == 5:
        add()
    elif choice == 6:
        delete()
    elif choice == 0:
        print("Bye!")
        exit()