import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

def record_weight(user_id, weight):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO weight_records (user_id, weight, date) VALUES (?, ?, ?)', (user_id, weight, date))
    conn.commit()
    conn.close()

def get_weight_records(user_id):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT weight, date FROM weight_records WHERE user_id = ? ORDER BY date', (user_id,))
    records = cursor.fetchall()
    conn.close
    return records

def plot_weight(records):
    if records:
        dates = [record[1] for record in records]
        weights = [record[0] for record in records]
        plt.figure(figsize=(10, 5))
        plt.plot(dates, weights, marker='o')
        plt.xlabel('Date')
        plt.ylabel('Weight(kg)')
        plt.title('Weight Change Over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print('No weight records found')