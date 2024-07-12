import os
import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess
import threading
import signal
import sys

# Path to audio files
audio_files = {
    'KEY_A': 'File1.wav',
    'KEY_B': 'File2.wav',
    'KEY_Y': 'File3.wav',
}

# Path to the input devices (footswitches)
device_paths = ['/dev/footswitch1', '/dev/footswitch2', '/dev/footswitch3']

# Initialize the input devices
devices = [InputDevice(path) for path in device_paths]

# A flag to indicate if the program is running
running = True
# Lock for thread-safe audio control
playback_lock = threading.Lock()

def play_audio(file_path):
    with playback_lock:
        # Stop any currently playing audio
        subprocess.run(['pkill', 'aplay'])
        # Play the new audio file
        subprocess.run(['aplay', file_path])

def monitor_device(device):
    print(f'Start monitoring {device.path}')
    device.grab()  # Grab the device to get exclusive access
    try:
        while running:
            for event in device.read_loop():
                if not running:
                    break
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    if key_event.keystate == key_event.key_down:
                        key_code = key_event.keycode
                        if key_code in audio_files:
                            print(f'Key {key_code} pressed on {device.path}, playing {audio_files[key_code]}')
                            play_audio(audio_files[key_code])
                            # Break the loop to handle the next input immediately
                            break
    finally:
        device.ungrab()

def signal_handler(sig, frame):
    global running
    print('Exiting gracefully...')
    running = False
    for device in devices:
        device.close()
    sys.exit(0)

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

print(f'Listening for key presses on {device_paths}...')

# Create a separate thread for each device to handle events concurrently
threads = []
for device in devices:
    thread = threading.Thread(target=monitor_device, args=(device,))
    threads.append(thread)
    thread.start()

# Keep the main thread alive
while running:
    signal.pause()

# Clean up and close devices
for device in devices:
    device.close()
