Aura Calendar Pro 2026
A modern, high-performance desktop calendar application built with Python and Tkinter, featuring a sleek "Aura" design system and SQL Server integration for persistent task management.

Key Features
Premium UI: Apple-inspired design with rounded cards, hover effects, and smooth animations.

Smart Indicators: Visual status dots (Green/Red) on calendar days to track task completion at a glance.

Intuitive Navigation: Navigate through months using the mouse wheel or modern UI buttons.

Persistence: Theme preferences and tasks are stored in a Microsoft SQL Server database.

Adaptive Theme: Toggle between Dark and Light modes with one click.

Tech Stack
Language: Python 3.x

GUI Framework: Tkinter

Database: Microsoft SQL Server

Driver: pyodbc

Installation & Setup
1. Database Configuration
Run the following script in your SQL Server Management Studio (SSMS) to initialize the database:

SQL
CREATE DATABASE BookShelf;
GO
USE BookShelf;

CREATE TABLE Settings (
    id INT PRIMARY KEY DEFAULT 1,
    is_dark_mode BIT DEFAULT 1,
    CONSTRAINT one_row CHECK (id = 1)
);
INSERT INTO Settings (id, is_dark_mode) VALUES (1, 1);

CREATE TABLE Tasks (
    id INT IDENTITY PRIMARY KEY,
    date_str VARCHAR(10),
    task_text NVARCHAR(MAX),
    is_done BIT DEFAULT 0
);
2. Python Environment
Install the required dependencies:

Bash
pip install pyodbc
3. Connection Settings
Update the connection string in main.py with your local credentials:

Python
'SERVER=localhost,1433;'
'UID=your_username;'
'PWD=your_password;'
Usage
Left Click: Open the task manager for a specific day.

Mouse Wheel: Scroll up/down to change months.

Theme Toggle: Click the ☀️/🌙 icon to switch modes.

Task Toggle: Inside the task window, select a task and click "Toggle Status" to mark it as done.
