from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_type = request.form['type']
    quality = request.form['quality']

    save_path = os.path.join(os.getcwd(), "downloads")
    os.makedirs(save_path, exist_ok=True)

    if download_type == 'mp3':
        command = f'yt-dlp -f bestaudio --extract-audio --audio-format mp3 -o "{save_path}/%(title)s.%(ext)s" "{url}"'
    else:
        command = f'yt-dlp -f "bestvideo[height<={quality}]+bestaudio/best" -o "{save_path}/%(title)s.%(ext)s" "{url}"'

    subprocess.run(command, shell=True)

    return "Download Successful!"

if __name__ == '__main__':
    app.run(debug=True)
