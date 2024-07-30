import subprocess
import threading
import signal
import sys

audio_file = 'File.wav'  # The file to play on loop

running = True
current_process = None

def play_audio_loop(file_path):
    global current_process
    while running:
        current_process = subprocess.Popen(['aplay', file_path])
        current_process.wait()

def signal_handler(sig, frame):
    global running
    print('Exiting gracefully...')
    running = False
    if current_process:
        current_process.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

print(f'Starting to play {audio_file} on loop...')

# Start the audio loop in a separate thread
thread = threading.Thread(target=play_audio_loop, args=(audio_file,))
thread.start()

# Keep the main thread alive
while running:
    signal.pause()

if current_process:
    current_process.terminate()
