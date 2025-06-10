from flask import Flask, render_template, request, redirect, send_file, send_from_directory
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

    if download_type == 'mp3':
        command = f'yt-dlp -g -f bestaudio "{url}"'
    else:
        command = f'yt-dlp -g -f "bestvideo[height<={quality}]+bestaudio/best" "{url}"'

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        download_link = result.stdout.strip().split('\n')[0]
        return redirect(download_link)
    else:
        return "❌ Download link could not be generated. Please check the URL."

# ⚙️ Specific route for your propeller verification file
@app.route('/propeller-verification-file.js')
def serve_verification_file():
    import os
    return send_from_directory(os.getcwd(), 'propeller-verification-file.js')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

