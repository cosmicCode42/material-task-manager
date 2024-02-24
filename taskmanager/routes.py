from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task


@app.route("/")
def home():
    # displays all tasks stored in the database
    tasks = list(Task.query.order_by(Task.id).all()) # displays all tasks in a list
    return render_template("tasks.html", tasks=tasks)


@app.route("/categories")
def categories():
    # displays all categories stored in the database
    categories = list(Category.query.order_by(Category.category_name).all()) # displays all categoriess in a list
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    # Allows new categories to be POSTed (ie added) by a user
    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    # Allows current categories to be edited by a user
    category = Category.query.get_or_404(category_id) #.get_or_404 retrieves the ID, or throws a 404 if the ID doesn't exist
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    # Allows a user to delete a current category
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    # Allows new tasks to be POSTed by a user
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task = Task(
            task_name = request.form.get("task_name"),
            task_description = request.form.get("task_description"),
            is_urgent = bool(True if request.form.get("is_urgent") else False),
            due_date = request.form.get("due_date"),
            category_id = request.form.get("category_id")
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_task.html", categories=categories)
