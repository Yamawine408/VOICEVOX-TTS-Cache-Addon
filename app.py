from flask import Flask, request, send_file, abort
import hashlib
import os
import requests

VOICEVOX_API = 'http://voicevox-engine:50021'
CACHE_DIR = '/share/tts_cache'

app = Flask(__name__)

def text_to_filename(text):
    hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return os.path.join(CACHE_DIR, f'{hash}.wav')

def synthesize(text, filepath):
    # 1. audio_query作成
    res = requests.post(
        f"{VOICEVOX_API}/audio_query",
        params={"text": text, "speaker": 3}
    )
    if res.status_code != 200:
        return False
    audio_query = res.json()

    # 2. synthesis
    res = requests.post(
        f"{VOICEVOX_API}/synthesis",
        params={"speaker": 1},
        json=audio_query
    )
    if res.status_code != 200:
        return False

    # 3. キャッシュ保存
    with open(filepath, 'wb') as f:
        f.write(res.content)
    return True

@app.route('/api/tts')
def tts():
    text = request.args.get('text')
    if not text:
        return abort(400, 'Missing "text" parameter')

    os.makedirs(CACHE_DIR, exist_ok=True)
    filepath = text_to_filename(text)

    if not os.path.exists(filepath):
        success = synthesize(text, filepath)
        if not success:
            return abort(500, 'Voicevox synthesis failed')

    return send_file(filepath, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8125)
