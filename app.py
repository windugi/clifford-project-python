from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

def get_events():
    events = []
    try:
        with open('mexam_events.txt') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                name, date_str = line.split(',')
                event_date = datetime.strptime(date_str.strip(), '%d/%m/%y').date()
                today = datetime.now().date()
                days_until = (event_date - today).days
                events.append({
                    'name': name,
                    'date': event_date.strftime('%d %B %Y'),
                    'days_until': days_until,
                    'color': 'red' if days_until <= 7 else 'lightblue'
                })
    except FileNotFoundError:
        pass
    return sorted(events, key=lambda x: x['days_until'])

@app.route('/')
def index():
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    current_date = now.strftime('%d/%m/%Y')
    events = get_events()
    return render_template('index.html', time=current_time, date=current_date, events=events)

if __name__ == '__main__':
    app.run(debug=True)
