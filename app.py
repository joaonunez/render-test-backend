import os
from flask import Flask, request, jsonify
from models import db, User, Post, Comment
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db.init_app(app)
Migrate(app, db)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "<h1>Blog API Server</h1>"


@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User()
    if data:
        email = request.json.get("email")
        if email:
            user.email = email
        else:
            return jsonify({
                "msg": "Email No PUEDE Estar Vacio"
            }), 400
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]

        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "Usuario creado", "data": user.serialize()}), 200
    else:
        return jsonify({"msg": "No Hya Cuerpo en la consulta"}), 400
    



@app.route("/post", methods=["POST"])
def create_post():
    post = Post()
    data = request.get_json()
    post.title = data["title"]
    post.subtitle = data["subtitle"]
    post.body = data["body"]
    

    user_id = request.json.get("user_id")
    if user_id is not None:
        post.user_id = user_id
    else:
        return jsonify({"msg": "el autor es requerido"}), 400

    db.session.add(post)
    db.session.commit()
    return jsonify({"msg": "Post creado", "data": post.serialize()}), 200


@app.route("/comment", methods=["POST"])
def create_comment():
    comment = Comment()
    data = request.get_json()
    user_id = request.json.get("user_id")
    post_id = request.json.get("post_id")
    if user_id is not None and post_id is not None:
        comment.user_id = user_id
        comment.post_id = post_id
    else:
        return jsonify({"msg": "el id de autor y el id de post es requerido"}), 400

    comment.text = data["text"]

    db.session.add(comment)
    db.session.commit()

    return jsonify({"msg": "Comentario creado", "data": comment.serialize()}), 200



#obtener todos los posts
@app.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    posts = list(map(lambda post: post.serialize(), posts))
    return jsonify({
        "data": posts
    }), 200

#obtener un post
@app.route("/post/<int:id>", methods=["GET"])
def get_post_by_id(id):
    post = Post.query.get(id)
    return jsonify({
        "data": post.serialize()##esimportante serializar para que pueda leer bien el post tal como en el get anterior
    }), 200


# Eliminar un post por ID
@app.route("/post/<int:id>", methods=["DELETE"])
def delete_post_by_id(id):
    post = Post.query.get(id)
    
    if not post:
        return jsonify({"message": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted successfully"}), 200



#obtener comentarios de un post
@app.route("/comments/<int:post_id>", methods=["GET"])
def get_comments_by_post(post_id):
    comments = Comment.query.filter_by(post_id = post_id).all() #filtrara por columna cuando la columna post_id sea igual al parametro pasado ala funcion
    comments = list(map(lambda comment: comment.serialize(), comments))
    return jsonify({
        "data": comments
    }), 200


#borrar comentarios por id
@app.route("/comment/<int:id>", methods=["DELETE"])
def delete_coment_by_id(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({"message:" "comentario no encontrado"}), 404
    
    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Comentario eliminado correctamente"}), 200









if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
