import sqlite3
import pandas as pd

# Подключение к базе данных (если файла нет, он будет создан)
conn = sqlite3.connect('vgsales.db')
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vgsales (
        Rank INTEGER,
        Name TEXT,
        Platform TEXT,
        Year INTEGER,
        Genre TEXT,
        Publisher TEXT,
        NA_Sales REAL,
        EU_Sales REAL,
        JP_Sales REAL,
        Other_Sales REAL,
        Global_Sales REAL
    )
''')

# Загрузка данных из CSV с помощью pandas
df = pd.read_csv('vgsales.csv')

# Запись данных в таблицу SQLite
df.to_sql('vgsales', conn, if_exists='replace', index=False)

print("Данные успешно загружены в базу данных 'vgsales.db'.\n")

# Функция для красивого вывода данных
def print_table(dataframe, title="Результат запроса"):
    print(f"\n{title}")
    print("=" * 80)
    print(dataframe.head(10).to_string(index=False))  # Вывод первых 10 строк
    print("=" * 80)

# Примеры запросов к базе данных

# 1. Вывести топ-10 игр по глобальным продажам
query1 = "SELECT Name, Platform, Year, Global_Sales FROM vgsales ORDER BY Global_Sales DESC LIMIT 10"
result1 = pd.read_sql_query(query1, conn)
print_table(result1, "Топ-10 игр по глобальным продажам")

# 2. Вывести суммарные продажи по платформам
query2 = "SELECT Platform, SUM(Global_Sales) AS Total_Sales FROM vgsales GROUP BY Platform ORDER BY Total_Sales DESC LIMIT 10"
result2 = pd.read_sql_query(query2, conn)
print_table(result2, "Топ-10 платформ по суммарным продажам")

# 3. Вывести игры жанра Action с наибольшими продажами в Европе
query3 = "SELECT Name, Platform, Year, EU_Sales FROM vgsales WHERE Genre = 'Action' ORDER BY EU_Sales DESC LIMIT 10"
result3 = pd.read_sql_query(query3, conn)
print_table(result3, "Топ-10 игр жанра Action по продажам в Европе")

# 4. Вывести количество игр по годам
query4 = "SELECT Year, COUNT(*) AS Game_Count FROM vgsales WHERE Year IS NOT 'N/A' GROUP BY Year ORDER BY Year DESC LIMIT 10"
result4 = pd.read_sql_query(query4, conn)
print_table(result4, "Количество игр по годам (последние 10 лет)")

# Закрытие соединения с базой данных
conn.close()
