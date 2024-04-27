from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import pandas as pd
import plotly.express as px
import plotly.io as pio
import csv
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

from utils import DICHRONA

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b\xc0;\xde\xedG&#\xf5A[qHL\xf3W\x90\x97\xec\x85\x9c\xfd\x9a\x1c\xf8'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database setup
DATABASE = 'users.db'

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    db = get_db()
    user_row = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user_row is None:
        return None

    user = User()
    user.id = user_row['username']
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user_row = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user_row and check_password_hash(user_row['password'], password):
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('add_macrons'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/stats')
@login_required
def display_pie_chart():
    # Load the TSV file with headers
    data = pd.read_csv('macrons_wiki_and_hypo_collated.tsv', delimiter='\t')

    # Create a new column for pie chart segmentation
    data['segment'] = data['macron'].apply(lambda x: 'empty' if pd.isna(x) or x == '' else 'non-empty')
    # Use source column directly for those entries that are non-empty
    data.loc[data['segment'] == 'non-empty', 'segment'] = data['source'].fillna('no source')
    # Generate a summary of the segments
    summary = data['segment'].value_counts()

    # Generate the first pie chart
    fig1 = px.pie(
        names=summary.index,
        values=summary.values,
        title="Macronized lines by source"
    )
    pie_html1 = pio.to_html(fig1, full_html=False)

    # Statistics for second pie chart
    # Count instances of DICHRONA characters in the token column
    data['dichrona_count'] = data['token'].apply(lambda x: sum(1 for char in x if char in DICHRONA))
    total_dichrona = data['dichrona_count'].sum()

    # Count the total number of digits in the macron column
    data['macron_digit_count'] = data['macron'].fillna('').apply(lambda x: sum(char.isdigit() for char in x))
    total_macron_digits = data['macron_digit_count'].sum()

    # Data for the second pie chart
    stats = pd.Series([total_dichrona, total_macron_digits], index=['Dichrona', 'Macrons'])

    # Generate the second pie chart
    fig2 = px.pie(
        names=stats.index,
        values=stats.values,
        title="Macronized dichrona"
    )
    pie_html2 = pio.to_html(fig2, full_html=False)

    # Render the template and include the pie charts
    return render_template('stats.html', pie_chart1=pie_html1, pie_chart2=pie_html2)

@app.route('/add_macrons', methods=['GET', 'POST'])
def add_macrons():
    if request.method == 'POST':
        token = request.form['token']
        new_macron = request.form['macron']
        update_tsv('macrons_wiki_and_hypo_collated.tsv', token, new_macron)
        return redirect(url_for('add_macrons'))
    
    return render_template('add_macrons.html')

def update_tsv(file_path, token, new_macron):
    data = []
    updated = False
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row[2] == token and not updated:  # Assuming the token is in the third column
                row[3] = new_macron  # Update macron
                row[4] = 'manual'   # Update source
                updated = True
            data.append(row)
    
    if updated:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(data)

if __name__ == '__main__':
    app.run(debug=True)
