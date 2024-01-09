import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from pytube import YouTube

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', '161630')


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        link = request.form.get("link")
        try:
            yt = YouTube(link)
            video = yt.streams.get_highest_resolution()

            # Pass video information directly to the template
            return render_template("download.html", video=video)
        except Exception as e:
            # Handle errors gracefully
            return render_template("download.html", error=f"An error occurred: {e}")

    if request.method == "GET":
        return render_template("download.html")

@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == "GET":
        return render_template("download.html")
    if request.method == "POST":

        link = request.form.get("link")  # Retrieve link from URL argument
        try:
            yt = YouTube(link)
            video = yt.streams.get_highest_resolution()

            # Download and provide the video file
            video_path = os.path.join('downloads', video.title + '.mp4')
            video.download(output_path='downloads', filename=video.title + '.mp4')
            return send_file(video_path, as_attachment=True)
        except Exception as e:
            # Handle errors gracefully
            return render_template("download.html", error=f"An error occurred: {e}")