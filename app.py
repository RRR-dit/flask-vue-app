from flask import Flask, render_template, request, redirect, jsonify, url_for
from forms import NameForm # Flask-WTFフォーム（名前入力用）
from models import db,User # SQLAlchemyのDBオブジェクトとモデル

app = Flask(__name__)
app.secret_key = "secret_key-0327" # フォームのCSRF対策で必要（Flask-WTFで使用）

#データベース設定 & 初期化
#DBの設定（SQLiteファイルとして保存）
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# モデル変更時に無駄な通知を抑える
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# SQLAlchemyのDBオブジェクトとアプリを紐づける
db.init_app(app)
#GET時はフォーム表示、POST時にバリデーション通ればDBに保存。
#保存後は greeting.html に遷移。
@app.route("/",methods=["GET","POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        username = form.username.data

        #DBに保存
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()

        return render_template("greeting.html",name=username,method=request.method) 
    return render_template("index.html",form=form)
#Flaskの「アプリケーションコンテキスト」内で create_all() を呼ぶことで、テーブルが作成されます。
#models.py 側の User クラスに応じたテーブルが data.db に作られる。
with app.app_context():
    db.create_all()
#ユーザー一覧（テンプレート表示
@app.route("/users")
def show_users():
    users = User.query.all()  # データベースから全ユーザー取得
    return render_template("users.html", users=users)
#削除（HTMLフォーム側
@app.route("/delete/<int:user_id>",methods=["POST"])
def delete_user(user_id):
    user=User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
#：編集画面 + 保存
@app.route("/edit/<int:user_id>",methods=["GET","POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = NameForm(obj=user)# 初期値をフォームに渡す

    if form.validate_on_submit():
        user.username = form.username.data
        db.session.commit()
        return redirect("/users")
    
    return render_template("edit.html", form=form, user=user)
#REST API
#ユーザー一覧（JSON）
@app.route("/api/users",methods=["GET"])
def api_get_users():
    users = User.query.all()
    user_list = [{"id":user.id, "username":user.username}for user in users]
    return jsonify(user_list)
#Vueアプリの表示エントリーポイント→ Vueはここを起点にSPA的な表示を行う
@app.route("/vue")
def vue_index():
    return render_template("vue_index.html")
#ユーザー追加（POST）
@app.route("/api/add_user", methods=["POST"])
def api_add_user():
    data = request.get_json()
    username = data.get("username", "").strip()

    if not username:
        return jsonify({"error": "名前が空です"}), 400

    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "ユーザー追加完了", "user": {"id": new_user.id, "username": new_user.username}})
#ユーザー削除（DELETE）
@app.route("/api/delete/<int:user_id>", methods=["DELETE"])
def api_delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "ユーザーが見つかりません"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "削除完了", "user_id": user_id})
#名前更新（PUT）
@app.route("/api/update/<int:user_id>", methods=["PUT"])
def api_update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    new_username = data.get("username", "").strip()

    if not new_username:
        return jsonify({"error": "名前は必須です"}), 400

    user.username = new_username
    db.session.commit()

    return jsonify({
        "message": "更新完了",
        "user": {"id": user.id, "username": user.username}
    })




if __name__ == "__main__":
    app.run(debug=True)
