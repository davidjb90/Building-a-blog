from flask import render_template

from . import app
from .database import session, Entry


@app.route("/")
@app.route("/page/<int:page>/")
def entries(page=1, limit=10):
    # Zero-indexed page
    
    PAGINATE_BY = int(request.args.get("limit", limit))
    
    page_index = page - 1

    count = session.query(Entry).count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]
    
    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages,
    )
    
@app.route("/entry/add", methods=["GET"])
def add_entry_get():
    return render_template("add_entry.html")
    
from flask import request, redirect, url_for

@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
    
    
@app.route("/entry/<id>", methods=["GET"])
def display_single_entry(id):
    entry = session.query(Entry).filter_by(id=id).first()
    return render_template("display_single.html", entry=entry)

@app.route("/entry/<id>/edit", methods=["GET"])
def edit_entry_get(id):
    entry = session.query(Entry).filter_by(id=id).first()
    return render_template("prepopulated_edit.html", entry=entry)
    
    
@app.route("/entry/<id>/edit", methods=["POST"])
def edit_entry_post(id):
    entry = session.query(Entry).filter_by(id=id).first()
    entry.title = request.form["title"]
    entry.content = request.form["content"]
    session.commit()
    return redirect(url_for("entries"))
    
@app.route("/entry/<id>/delete", methods=["GET"])
def delete_entry(id):
    entry = session.query(Entry).filter_by(id=id).first()
    session.delete(entry)
    session.commit()
    return redirect(url_for("entries"))