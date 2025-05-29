# TaskFlow - Task Management Application

A modern, full-stack task management application built with FastAPI, GraphQL, WebSockets, and React. TaskFlow provides a seamless experience for managing your daily tasks with real-time updates and a beautiful, responsive interface.

## ✨ Features

- **User Authentication**: Secure JWT-based authentication with registration and login
- **Task Management**: Create, read, update, and delete tasks with rich metadata
- **Real-time Updates**: WebSocket integration for live task updates
- **GraphQL API**: Flexible data querying with GraphQL alongside REST endpoints
- **Advanced Filtering**: Filter tasks by status, priority, category, and search functionality
- **Responsive Design**: Beautiful glassmorphism UI that works on all devices
- **Task Statistics**: Visual dashboard showing task completion metrics
- **Categories & Priorities**: Organize tasks with custom categories and priority levels

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **GraphQL**: Query language with Strawberry GraphQL
- **WebSockets**: Real-time bidirectional communication
- **SQLAlchemy**: Python SQL toolkit and ORM
- **SQLite**: Lightweight database for development
- **JWT Authentication**: Secure token-based authentication
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **React**: JavaScript library for building user interfaces
- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Icon library
- **Glassmorphism UI**: Modern design with backdrop blur effects

## 📁 Project Structure

```
taskflow/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── rest_schemas.py
│   │   │   └── graphql_schemas.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── tasks.py
│   │   │   └── websocket.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── task_service.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   └── index.html
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for development tools, optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/uzairrrrrr/taskflow.git
   cd taskflow
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the application**
   - Frontend: Go to frondend folder open index.html on browser
   - API Documentation: http://localhost:8000/docs
   - GraphQL Playground: http://localhost:8000/graphql

## 📋 API Endpoints

### REST API

#### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

#### Tasks
- `GET /api/tasks/` - Get all tasks (with filtering)
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task

### GraphQL API

Access GraphQL at `/graphql`

#### Queries
```graphql
# Get all tasks with optional filtering
query GetTasks($filters: TaskFilterGQL, $skip: Int, $limit: Int) {
  tasks(filters: $filters, skip: $skip, limit: $limit) {
    id
    title
    description
    status
    priority
    category
    createdAt
    dueDate
  }
}

# Get a specific task
query GetTask($id: Int!) {
  task(id: $id) {
    id
    title
    description
    status
    priority
    category
  }
}
```

#### Mutations
```graphql
# Create a new task
mutation CreateTask($taskInput: TaskInputGQL!) {
  createTask(taskInput: $taskInput) {
    id
    title
    status
  }
}

# Update a task
mutation UpdateTask($id: Int!, $taskInput: TaskUpdateInputGQL!) {
  updateTask(id: $id, taskInput: $taskInput) {
    id
    title
    status
  }
}

# Delete a task
mutation DeleteTask($id: Int!) {
  deleteTask(id: $id)
}
```

### WebSocket

Connect to WebSocket at `/ws/{user_id}` for real-time task updates.

## 🎨 Frontend Features

### Components
- **Login/Register**: Authentication forms with validation
- **Dashboard**: Main task management interface
- **TaskCard**: Individual task display with inline editing
- **TaskForm**: Modal form for creating new tasks
- **Filters**: Advanced filtering and search functionality

### Key Features
- Real-time task updates via WebSocket
- Inline task editing
- Task status toggling
- Priority and category management
- Responsive glassmorphism design
- Task statistics dashboard

## 🔐 Authentication

The application uses JWT (JSON Web Tokens) for authentication:

1. Users register with username, email, and password
2. Login returns an access token
3. Token is stored in localStorage
4. All API requests include the token in the Authorization header
5. Tokens expire after 30 minutes (configurable)

## 🗃️ Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- full_name
- hashed_password
- created_at
- is_active

### Tasks Table
- id (Primary Key)
- title
- description
- status (todo, in_progress, completed)
- priority (low, medium, high, urgent)
- category
- due_date
- created_at
- updated_at
- completed_at
- owner_id (Foreign Key to Users)

## 🚀 Deployment

### Development
```run.py
cd backend
python run.py
```



## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Strawberry GraphQL for GraphQL integration
- Tailwind CSS for the utility-first CSS framework
- React team for the amazing frontend library

---

**TaskFlow** - Making task management simple and beautiful! 🚀