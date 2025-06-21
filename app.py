from flask import Flask, render_template, redirect, url_for, request
from models import Peak, PeakList, db_session, User
import datetime

app = Flask(__name__)
app.secret_key = 'dev'


@app.route('/')
def index():
    all_peaks_lists = db_session.query(PeakList).all()
    return render_template('index.html', all_peaks_lists=all_peaks_lists)

@app.route('/list/<int:list_id>', methods=['GET', 'POST'])
def list_view(list_id):
    all_peaks_lists = db_session.query(PeakList).all()
    peak_list = db_session.query(PeakList).get(list_id)

    if request.method == 'GET':
        return render_template('list_view.html', peak_list=peak_list, all_peaks_lists=all_peaks_lists)

    elif request.method == 'POST':
        return render_template('list_view.html')

@app.route('/update_user_data', methods=['POST'])
def update_user_data():
    list_id = int(request.form.get('list_id'))
    selected_peak_ids = set(map(int, request.form.getlist('peaks')))
    peak_list = db_session.query(PeakList).get(list_id)
    all_peaks = peak_list.peaks

    for peak in all_peaks:
        if peak.id in selected_peak_ids:
            peak.complete = True
        else:
            peak.complete = False

    db_session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()


