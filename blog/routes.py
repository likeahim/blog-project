from flask import flash, redirect, url_for, render_template, request
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

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
def create_entry():
    return handle_entry_form()

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    return handle_entry_form(entry_id)