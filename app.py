from flask import Flask, render_template, request, redirect, send_from_directory
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_type = request.form['type']
    quality = request.form['quality']

    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best' if download_type == 'mp4' else 'bestaudio',
        'quiet': True,
        'skip_download': True,
        'noplaylist': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            download_link = info['url']
            return redirect(download_link)
    except Exception as e:
        return f"❌ Error generating download link: {str(e)}"

@app.route('/propeller-verification-file.js')
def serve_verification_file():
    return send_from_directory('static', 'propeller-verification-file.js')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
