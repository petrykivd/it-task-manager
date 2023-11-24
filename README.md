# it-task-manager

Welcome to the Task | Hub, a simple web application for managing tasks in your development team. This project allows
team members to create tasks, assign them to other members, and mark them as completed.

## Features

- **Task Creation**: Team members can create new tasks, providing details such as name, description, deadline, and
  priority.
- **Task Assignment**: Tasks can be assigned to team members, helping to distribute the workload effectively.
- **Task Completion**: Team members can mark tasks as done, indicating successful completion.
- **Task Editing**: Users with appropriate permissions can edit task details.
- **Worker Management**: View a list of team members and their associated tasks.
- **Authentication**: Secure login/logout functionality.

## Check it out!

[Task Hub project deployed on Render](https://task-manager-j8w3.onrender.com/)

**Demo Credentials:**
- Username: `bob3307` 
- Password: `pass12345`

## Getting Started

1. Clone the repository: ` git clone https://github.com/petrykivd/it-task-manager.git `
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
    - On Windows: `venv\Scripts\activate`
    - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
    - If you don't have **pip** installed  [install it here](https://pip.pypa.io/en/stable/installation/#).
5. Apply database migrations: `python manage.py migrate`
    - `python manage.py loaddata database_dump.json` to load the database dump.
6. Create a superuser: `python manage.py createsuperuser` or use the existing one:
    - Username: `admin`
    - Password: `admin@12345`
      or use regular user:
    - Username: `bob3307`
    - Password: `pass12345`
7. Run the development server: `python manage.py runserver`

Visit `http://127.0.0.1:8000/` in your web browser to access the Task Manager.

## Usage

1. Log in with your credentials or create a new account.
2. Explore the dashboard to view tasks, task counts by priority, and tasks assigned to you.
3. Create new tasks using the "Add task" button.
4. Assign tasks to team members.
5. Mark tasks as completed when finished.

## TODO

- **Task List Page Optimization**: 
   - Implement pagination on pages that display multiple items (e.g., task lists).
   - Implement the ability to search for tasks using various criteria such as name, priority, status, etc.
- **Design Enhancement**:
   - Style Refinement: Improve the styles and layout of elements on the task pages for a more user-friendly experience.
   - Animations and Transitions: Add animations or transitions between pages to enhance visual appeal and usability.
- **Internationalization Support**: 
   - Provide users with the option to choose their preferred language for the user interface (localization).
   - Ensure translation support for essential textual elements used throughout the application.
- **Task Statistics**: 
   - Create a dedicated page displaying task statistics, including the number of tasks by priority, status, etc.
   -  Display these statistics in the form of graphs or diagrams for better data visualization.
- **User Registration**:
   - Enable the registration of new users, allowing them to create accounts for using the application.
- **Test Coverage**:
   - Develop tests for various parts of the application to ensure that all functions work as expected.
   - Verify that the application performs reliably under different scenarios.

## Contributing

Feel free to contribute to these enhancements, and let's make the Task | Hub even better!
