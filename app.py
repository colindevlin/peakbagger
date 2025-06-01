from flask import Flask, render_template, session, redirect, url_for, flash, get_flashed_messages, request
from models import Peak, PeakList, db_session, User
import datetime

app = Flask(__name__)
app.secret_key = 'dev'

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return db_session.query(User).get(user_id)
    return None

@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        user = db_session.query(User).get(session['user_id'])
    return dict(user=user)

@app.route('/')
def index():
    all_peaks_lists = db_session.query(PeakList).all()
    return render_template('index.html', all_peaks_lists=all_peaks_lists)

@app.route('/list/<int:list_id>')
def list_view(list_id):
    all_peaks_lists = db_session.query(PeakList).all()
    peak_list = db_session.query(PeakList).get(list_id)
    print([peak.name for peak in peak_list.peaks])
    return render_template('list_view.html', peak_list=peak_list, all_peaks_lists=all_peaks_lists)

@app.route('/manage', methods=['GET', 'POST'])
def manage_list():
    current_user = get_current_user()
    if request.method == "GET":
        if current_user:
            user_lists = current_user.peak_lists
            all_peaks_lists = db_session.query(PeakList).all()
            return render_template('manage.html', user_lists=user_lists, all_peaks_lists=all_peaks_lists)
        else:
            flash("Please login to manage your lists.")
            return redirect('/')
    elif request.method == "POST":
        if current_user:
            user_lists = current_user.peak_lists
            selected_lists = request.form.getlist('subscribe_list')
            for peak_list in db_session.query(PeakList).filter(PeakList.id.in_(selected_lists)):
                if peak_list not in user_lists:
                    current_user.peak_lists.append(peak_list)
            for peak_list in user_lists:
                if str(peak_list.id) not in selected_lists:
                    current_user.peak_lists.remove(peak_list)
            db_session.commit()
            return redirect(url_for('manage_list'))
        else:
            flash("Please login to manage your lists.")
            return redirect('/')


@app.route('/login/<int:user_id>')
def login(user_id):
    session['user_id'] = user_id
    flash("Logged in as {user_id}")
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

