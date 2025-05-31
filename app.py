from flask import Flask, render_template, session, redirect, url_for, flash, get_flashed_messages
from models import Peak, PeakList, db_session, User
import datetime

app = Flask(__name__)
app.secret_key = 'dev'

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return db_session.query(User).get(user_id)
    return None

@app.route('/')
def index():
    all_peaks_lists = db_session.query(PeakList).all()
    return render_template('index.html', all_peaks_lists=all_peaks_lists)

@app.route('/list/<int:list_id>')
def list_view(list_id):
    peak_list = db_session.query(PeakList).get(list_id)
    return render_template('list_view.html', peak_list=peak_list)

@app.route('/manage')
def manage_list():
    return render_template('manage.html')

@app.route('/login')
def login():
    session['user_id'] = 1
    flash("Logged in as testuser")
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()


# add a peak to a list:
# some_peak.lists.append(some_peak_list)
# session.commit()
#
# query all lists:
# peak_lists = session.query(PeakList).all()
#
# all peaks in a list:
# peaks = session.query(PeakList).filter_by(name="RMNP").first().peaks

