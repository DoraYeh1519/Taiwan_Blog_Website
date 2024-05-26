# Introduction  

## Setup
#### 1. Setup the program and virtual environment:
   1. Open the terminal by ``` Ctrl+` ```
   2. Execute ``` $pip install -r requirement.txt ``` to install packages
   3. Open it in visual studio and try running it. The editor will ask you to setup virtual environment. Just do it.
#### 2. Setup Database:
   1. Import **'dbms_project.sql'** file from folder **'DataBase Setting'** into your MySQL server.
   2. Setup **username**, **password**, and **database** in the **#connect to DB** section in **main.py**
```python
   # CONNECT TO DB
    username = "" #Your username
    password = "" #Your password
    host = "localhost"
    port = 3306
    database = "dbms_project" #Your database name
    connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
```
