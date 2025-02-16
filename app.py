from flask import Flask, request, render_template, redirect
from pytube import YouTube

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        try:
            yt = YouTube(url)
            streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc()
            return render_template("index.html", yt=yt, streams=streams)
        except Exception as e:
            return render_template("index.html", error=f"Error: {e}")

    return render_template("index.html")

@app.route("/download", methods=["GET"])
def download_video():
    url = request.args.get("url")
    itag = request.args.get("itag")
    if not url or not itag:
        return "Invalid request"

    try:
        yt = YouTube(url)
        stream = yt.streams.get_by_itag(itag)
        return redirect(stream.url)  # Redirects to YouTube's direct video link
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
