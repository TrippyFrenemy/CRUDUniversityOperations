# University Database Management
This project is a command-line application to manage a university database. It uses SQLAlchemy to interact with a PostgreSQL database, performing various CRUD (Create, Read, Update, Delete) operations on entities such as Students, Teachers, Subjects, Groups, and Marks.Utilizing SQLAlchemy for ORM and PostgreSQL for the database, it simplifies complex CRUD operations. Alembic is used for database migration, ensuring that database schemas are managed and version-controlled efficiently.

## Database Structure
The university database consists of the following entities:

- Group: Represents groups that students belong to. Attributes: `id`, `name`.

- Student: Represents students. Attributes: `id`, `name`, `group_id`. It has a foreign key to the Group.

- Teacher: Represents teachers. Attributes: `id`,`name`.

- Subject: Represents subjects that teachers teach. Attributes: `id`, `name`,`teacher_id`. It has a foreign key to Teacher.

- Mark: Represents students' marks. Attributes: `id`, `student_id`, `subject_id`, `mark`, `date`. It has foreign keys to Student and Subject.

# Setup and Running the Application
1. Configuration: Ensure that the `config.py` file is correctly set up with your PostgreSQL database URL.

2. Dependencies:

    - SQLAlchemy for ORM.
    - Faker for generating fake data.
    - Alembic: Database migration.
    - PostgreSQL as the database.

3. Database Migration with Alembic:
    
   - Before running alembic init the database url in the `alembic.ini` 
   - Run migrations
       ```
       alembic upgrade head
       ```
4. Seeding the Database: Run the `seed.py` script to populate the database with initial data:

    ```
    python seed.py
    ```
    This script will create Groups, Teachers, Subjects, Students, and Marks with randomly generated data using the Faker library.

5. Running the Application: Run the main.py script with appropriate command-line arguments to perform various operations. Here are the types of arguments you can use:

    - -a, --action: CRUD actions: create, list, update, remove.
    - -m, --model: Models: Teacher, Group, Student, Subject, Mark.
    - And others related to the specific attributes of each model you can see use the --help.
    
   For example, to list all teachers:

    ```
    python main.py -a list -m Teacher
    ```