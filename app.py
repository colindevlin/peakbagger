from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from models import Peak, db_session
import datetime

app = Flask(__name__)
app.secret_key = 'dev'

@app.route('/')
def home_page():
    all_peaks = db_session.query(Peak).all()

    return render_template('home.html', all_peaks=all_peaks)


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

