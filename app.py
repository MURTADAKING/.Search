from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_user(username):

    url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers)
        data = r.json()

        user = data["graphql"]["user"]

        return {
            "username": user["username"],
            "name": user["full_name"],
            "followers": user["edge_followed_by"]["count"],
            "following": user["edge_follow"]["count"],
            "posts": user["edge_owner_to_timeline_media"]["count"],
            "bio": user["biography"],
            "profile_pic": user["profile_pic_url_hd"]
        }

    except:
        return None


@app.route("/", methods=["GET","POST"])
def index():

    result = None

    if request.method == "POST":

        username = request.form["username"]

        result = get_user(username)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run()
