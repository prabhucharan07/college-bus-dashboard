from flask import Flask, render_template_string, jsonify
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="sql7.freesqldatabase.com",
        user="sql7825905",
        password="48i1bgllVt",
        database="sql7825905",
        port=3306
    )

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>College Bus Dashboard</title>
    <style>
        body { font-family: Arial; background: #f0f0f0; padding: 20px; }
        h1 { color: #333; text-align: center; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th { background: #4CAF50; color: white; padding: 12px; }
        td { padding: 10px; border-bottom: 1px solid #ddd; text-align: center; }
        tr:hover { background: #f5f5f5; }
        .count { font-size: 24px; color: #4CAF50; text-align: center; margin: 20px; }
    </style>
    <meta http-equiv="refresh" content="30">
</head>
<body>
    <h1>🚌 College Bus Entry Dashboard</h1>
    <div class="count">Today Total Buses: {{ total }}</div>
    <table>
        <tr>
            <th>S.No</th>
            <th>Route Number</th>
            <th>Entry Time</th>
            <th>Date</th>
        </tr>
        {% for i, entry in entries %}
        <tr>
            <td>{{ i }}</td>
            <td>{{ entry[1] }}</td>
            <td>{{ entry[2] }}</td>
            <td>{{ entry[3] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/')
def dashboard():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM bus_entry 
                      WHERE date = CURDATE() 
                      ORDER BY entry_time DESC""")
    entries = cursor.fetchall()
    cursor.close()
    db.close()
    numbered = list(enumerate(entries, start=1))
    return render_template_string(HTML, entries=numbered, total=len(entries))

@app.route('/api/buses')
def api_buses():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM bus_entry 
                      WHERE date = CURDATE()""")
    entries = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify([{
        'id': e[0],
        'route': e[1],
        'time': str(e[2]),
        'date': str(e[3])
    } for e in entries])

if __name__ == "__main__":
    app.run(debug=False)
