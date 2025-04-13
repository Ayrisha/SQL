# Данный python-скрипт имитирует запрос к БД


# Импорт библиотек
import pandas as pd
import duckdb

# Задание таблиц БД
users = pd.read_csv('users.csv')
course_users = pd.read_csv('course_users.csv')
courses = pd.read_csv('courses.csv')
course_types = pd.read_csv('course_types.csv')
lessons = pd.read_csv('lessons.csv')
subjects = pd.read_csv('subjects.csv')
cities = pd.read_csv('cities.csv')
homework_done = pd.read_csv('homework_done.csv')
homework = pd.read_csv('homework.csv')
homework_lessons = pd.read_csv('homework_lessons.csv')
user_roles = pd.read_csv('user_roles.csv') 

# Задание SQL-запроса
query = """
SELECT 
  c.id AS course_id,
    c.name AS course_name,
    s.name AS subject_name,
    s.project AS subject_type,
    ct.name AS course_type,
    c.starts_at AS course_starts_at,
    u.id AS user_id,
    u.last_name AS user_last_name,
    c2.name AS city_name,
    cu.active AS active,
    cu.created_at AS course_created_at,
    FLOOR(cu.available_lessons/c.lessons_in_month) AS available_months,
    COUNT(hd.homework_id) FILTER (WHERE c.id = l.course_id) AS completed_homeworks_count
FROM 
  courses c
  INNER JOIN subjects s ON c.subject_id = s.id
    INNER JOIN course_types ct ON c.course_type_id = ct.id
    INNER JOIN course_users cu ON c.id = cu.course_id
    INNER JOIN users u ON cu.user_id = u.id
    INNER JOIN user_roles ur ON u.user_role_id = ur.id AND ur.name ='student'
    INNER JOIN cities c2 ON u.city_id = c2.id
    LEFT JOIN homework_done hd ON u.id = hd.user_id 
    LEFT JOIN homework_lessons hl ON hd.homework_id = hl.homework_id
    LEFT JOIN lessons l ON hl.lesson_id = l.id  
GROUP BY 
  c.id,
    c.name,
    s.name,
    s.project,
    ct.name,
    c.starts_at,
    u.id,
    u.last_name,
    c2.name,
    cu.active,
    cu.created_at,
    cu.available_lessons,
    c.lessons_in_month;
"""

# Выполнение SQL-запроса
df_result = duckdb.query(query).to_df()

df_result.to_csv('result.csv')

# Вывод результата
print(df_result)