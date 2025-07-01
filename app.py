from flask import Flask, render_template, request, send_file
import io
import wave
import numpy as np

app = Flask(__name__)

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
}
REVERSE_MORSE_CODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

# Morse code timing (in seconds)
DOT = 0.1
DASH = DOT * 3
SYMBOL_SPACE = DOT
LETTER_SPACE = DOT * 3
WORD_SPACE = DOT * 7
FREQ = 700  # Hz
SAMPLE_RATE = 44100


def text_to_morse(text):
    return ' '.join(MORSE_CODE_DICT.get(c.upper(), '') for c in text)

def morse_to_text(morse):
    words = morse.strip().split(' / ')
    decoded = []
    for word in words:
        letters = word.split()
        decoded.append(''.join(REVERSE_MORSE_CODE_DICT.get(l, '') for l in letters))
    return ' '.join(decoded)

def morse_to_wav(morse):
    audio = np.array([], dtype=np.float32)
    for symbol in morse:
        if symbol == '.':
            audio = np.concatenate([audio, tone(DOT), silence(SYMBOL_SPACE)])
        elif symbol == '-':
            audio = np.concatenate([audio, tone(DASH), silence(SYMBOL_SPACE)])
        elif symbol == ' ':
            audio = np.concatenate([audio, silence(LETTER_SPACE)])
        elif symbol == '/':
            audio = np.concatenate([audio, silence(WORD_SPACE)])
    # Normalize
    audio = np.int16(audio / np.max(np.abs(audio)) * 32767)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())
    buf.seek(0)
    return buf

def tone(duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    return 0.5 * np.sin(2 * np.pi * FREQ * t)

def silence(duration):
    return np.zeros(int(SAMPLE_RATE * duration))

@app.route('/', methods=['GET', 'POST'])
def index():
    text = morse = result = ''
    direction = 'text-to-morse'
    if request.method == 'POST':
        direction = request.form.get('direction')
        if direction == 'text-to-morse':
            text = request.form.get('text', '')
            morse = text_to_morse(text)
            result = morse
        else:
            morse = request.form.get('morse', '')
            text = morse_to_text(morse)
            result = text
    return render_template('index.html', text=text, morse=morse, result=result, direction=direction, morseDict=MORSE_CODE_DICT)

@app.route('/play_morse', methods=['POST'])
def play_morse():
    morse = request.form.get('morse', '')
    buf = morse_to_wav(morse)
    return send_file(buf, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(debug=True) 