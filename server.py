from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import linked_list
import hashtable
import random
import binarysearchtree
import queue
import stack

# app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

# configure sqlite3 to enforce foreign key constraints


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


db = SQLAlchemy(app)
now = datetime.now()


# models

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")


class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# routes


@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name=data["name"],
        email=data["email"],
        address=data["address"],
        phone=data["phone"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User Created"}), 200


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )
    return jsonify(all_users_ll.to_list()), 200


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )
    return jsonify(all_users_ll.to_list()), 200


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )

    user = all_users_ll.get_user_by_id(user_id)
    return jsonify(user), 200


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"message": "User not found."}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User (and his blogs) deleted successfully."}), 200


@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    data = request.get_json()

    # user_id passed must be valid user
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User does not exist!"}), 400

    # new_blog_post = BlogPost(
    #     title=data["title"],
    #     body=data["body"],
    #     date=now,
    #     user_id=user_id
    # )
    # db.session.add(new_blog_post)
    # db.session.commit()
    # return jsonify({"message": "New Blog Post Created"}), 200

    ht = hashtable.HashTable(10)

    ht.add_key_value("title", data["title"])
    ht.add_key_value("body", data["body"])
    ht.add_key_value("date", now)
    ht.add_key_value("user_id", user_id)

    new_blog_post = BlogPost(
        title=ht.get_value("title"),
        body=ht.get_value("body"),
        date=ht.get_value("date"),
        user_id=ht.get_value("user_id"),
    )
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify({"message": "New blog post created successfully."}), 200


@app.route("/blog_posts", methods=["GET"])
def get_all_blog_posts():
    blog_posts = BlogPost.query.all()
    #blog_posts = BlogPost.query.filter_by(id='5').first()
    #print(f"id: {blog_posts.id}, title: {blog_posts.title}, body: {blog_posts.body}, user_id: {blog_posts.user_id}")
    all_posts = []
    for post in blog_posts:
        all_posts.append({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "user_id": post.user_id
        })

    return jsonify(all_posts)


@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)  # So that BST is not skewed

    bst = binarysearchtree.BinarySearchTree()
    blog_count = 0
    for post in blog_posts:
        # print(post.id)
        # print("\n")
        #blog_count += 1
        bst.insert({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "user_id": post.user_id
        })

    #print(f"No. of Blogs: {blog_count}")
    post = bst.search(blog_post_id)
    if not post:
        return jsonify({"message": "Post not found!"})

    return jsonify(post)


@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    blogposts = BlogPost.query.all()
    q = queue.Queue()
    for post in blogposts:
        q.enqueue(post)

    return_list = []

    for i in range(len(blogposts)):
        post = q.dequeue()
        numeric_body = 0
        for char in post.data.body:
            numeric_body += ord(char)

        post.body = numeric_body
        return_list.append({
            "id": post.data.id,
            "title": post.data.title,
            "body": post.body,
            "user_id": post.data.user_id
        })

    return jsonify(return_list)


@app.route("/blog_post/<blog_post_id>", methods=["DELETE"])
def delete_one_blog_post(blog_post_id):
    post = BlogPost.query.filter_by(id=blog_post_id).first()
    if post is None:
        return jsonify({"message": "Post not found!"}), 404
    # print("Post =", post)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully!"}), 200


@app.route("/blog_post/delete_last_blog_post", methods=["DELETE"])
def delete_last_blog_post():
    blog_posts = BlogPost.query.all()

    if blog_posts is None:
        return jsonify({"message": "No posts found!"}), 404
    blog_stack = stack.Stack()
    for post in blog_posts:
        blog_stack.push(post)

    post_to_delete = blog_stack.pop()
    # print("post_to_delete:", post_to_delete)
    db.session.delete(post_to_delete.data)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True)
