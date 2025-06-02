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

@app.route('/manage_user', methods=['GET', 'POST'])
def manage_user():
    current_user = get_current_user()
    if request.method == "GET":
        if current_user:
            user_lists = current_user.peak_lists
            all_peaks_lists = db_session.query(PeakList).all()
            return render_template('manage_user.html', user_lists=user_lists, all_peaks_lists=all_peaks_lists)
        else:
            flash("Please login to manage your lists.")
            return redirect('/')
    elif request.method == "POST":
        if current_user:
            user_lists = current_user.peak_lists
            selected_lists = request.form.getlist('subscribe_list')
            list_to_manage = request.form.getlist('manage_list')
            for peak_list in db_session.query(PeakList).filter(PeakList.id.in_(selected_lists)):
                if peak_list not in user_lists:
                    current_user.peak_lists.append(peak_list)
            for peak_list in user_lists:
                if str(peak_list.id) not in selected_lists:
                    current_user.peak_lists.remove(peak_list)
            db_session.commit()
            return redirect(url_for('manage_user'))
        else:
            flash("Please login to manage your lists.")
            return redirect('/')

@app.route('/manage_list/<int:list_id>', methods=['GET', 'POST'])
def manage_list(list_id):
    peak_list = db_session.query(PeakList).get(list_id)
    user = get_current_user()
    if not user:
        flash("Please login to manage lists.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Process form data to update list details (e.g., add/remove peaks, mark peaks as completed)
        # For example:
        completed_peaks = request.form.getlist('peaks')
        # Update user's progress based on that
        # (You implement this logic yourself based on your data model)
        db_session.commit()
        flash("List updated.")
        return redirect(url_for('manage_list', list_id=list_id))
    else:
        # Show the current list info, with a form to make changes
        return render_template('manage_list.html', peak_list=peak_list, user=user)
# ***** START HERE, WORKING ON MANAGING PEAKS WITHIN A LIST *****



@app.route('/login/<int:user_id>')
def login(user_id):
    session['user_id'] = user_id
    flash("Logged in as {user_id}")
    return redirect(url_for('manage_user'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()

#
# all peaks in a list:
# peaks = session.query(PeakList).filter_by(name="RMNP").first().peaks

