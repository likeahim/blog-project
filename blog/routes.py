from flask import flash, redirect, url_for, render_template, request, session
from blog import create_app, app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm
from blog.auth import login_required

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)

def handle_entry_form(entry_id=None):
    entry = Entry.query.get(entry_id) if entry_id else None
    form = EntryForm(obj=entry)
    errors = None

    if request.method == 'POST':
        if form.validate_on_submit():
            if entry:
                form.populate_obj(entry)
                flash("Post updated successfully", "success")
            else:
                entry = Entry(
                    title=form.title.data,
                    body=form.body.data,
                    is_published=form.is_published.data
                )
                db.session.add(entry)
                flash("Post added successfully", "success")

            db.session.commit()
            return redirect(url_for("index"))
        else:
            errors = form.errors

    return render_template(
        "entry_form.html",
        form=form,
        errors=errors,
        is_edit=bool(entry),
        form_title="Editing" if entry else "Add new post"
    )


@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_entry():
    return handle_entry_form()

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    return handle_entry_form(entry_id)

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True
            flash('You are now logged in', 'success')
            return redirect(next_url or url_for('index'))
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
    return render_template("drafts.html", drafts=drafts)

@app.route('/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted')
    return redirect(url_for('index'))