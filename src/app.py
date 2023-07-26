from flask import Flask, render_template, jsonify, url_for, request, redirect, flash
import sqlite3
import bot_db_answer
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta
import pandas as pd 

matplotlib.use('agg')
app = Flask(__name__)
DB_FILE = "database/messages.db"

def get_all_messages(filters=None):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        query = "SELECT * FROM messages"
        if filters:
            status = filters.get("status")
            sort = filters.get("sort")
            label = filters.get("label")
            conditions = []

            if status and status != "all":
                done = '\'Done\''
                wait = '\'Waiting\''
                conditions.append(f"status = {done if status == 'done' else wait}")

            if label:
                label = '\'' + label + '\''
                conditions.append(f"label = {label}")
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            if sort and sort == "old":
                query += " ORDER BY timestamp DESC"
            else:
                query += " ORDER BY timestamp"

        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return rows, columns
    except Exception as e:
        print(f"Error: {e}")
        return [], []

@app.route('/')
def start_page():
    return redirect(url_for('get_all_messages_route'))

@app.route('/get_all_messages', methods=['GET'])
def get_all_messages_route():
    rows, columns = get_all_messages()
    if not rows:
        return jsonify({"message": "No messages found."}), 404
    return render_template('index.html', columns=columns, rows=rows)

@app.route('/view_chat/<int:chat_id>/<string:ticket_text>/<int:id>', methods=['GET', 'POST'])
def view_chat(chat_id, ticket_text, id):
    if request.method == 'POST':
        text = request.form['text']
        print(f"Chat ID: {chat_id}, Text: {text}")
        bot_db_answer.update_status_by_chat_id(DB_FILE, chat_id, text, id)
        return redirect(url_for('get_all_messages_route'))

    return render_template('view_chat.html', id=id, text=ticket_text )

@app.route('/apply_filters', methods=['GET'])
def apply_filters():
    filters = {
        "status": request.args.get("status"),
        "sort": request.args.get("sort"),
        "label": request.args.get("label"),
    }
    rows, columns = get_all_messages(filters)
    if not rows:
        return jsonify({"message": "No messages found with selected filters."}), 404
    return render_template('index.html', columns=columns, rows=rows)


def get_last_month_data():
    data = get_last_month_data()
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    current_date = datetime.now()
    last_month_start = current_date.replace(day=1) - timedelta(days=1)
    last_month_end = last_month_start.replace(day=1)

    last_month_data = df[(df["timestamp"] >= last_month_end) & (df["timestamp"] <= last_month_start)]

    label_counts = last_month_data.groupby("label").size()

    return label_counts

@app.route('/stats')
def index():
    label_counts = get_last_month_data()

    colors = plt.cm.get_cmap('tab20').colors
    num_colors = len(label_counts)
    color_map = colors[:num_colors]

    plt.figure(figsize=(10, 6))
    label_counts.plot(kind='barh', color=color_map)  # Use the custom color map for horizontal bar chart
    plt.title("Distribution by Label for Last Month")
    plt.xlabel("Count")
    plt.ylabel("Label")  # Switch x-axis and y-axis labels for horizontal chart

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()


    plot_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render_template('stats.html', plot_data=plot_data)

def get_last_month_data():
    conn = sqlite3.connect(DB_FILE)

    query = '''
        SELECT timestamp, label
        FROM messages
    '''

    df = pd.read_sql_query(query, conn)

    conn.close()

    label_counts = df.groupby("label").size()

    return label_counts

if __name__ == '__main__':
    app.run(debug=True)
