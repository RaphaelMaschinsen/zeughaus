# Zeughaus Footswitch Audio Player

This project uses USB footswitches to play different audio files on a Raspberry Pi. The system is set up as a service that starts on boot and listens for footswitch inputs to play corresponding audio files.

## Table of Contents

- [Setup](#setup)
  - [Installing Raspberry Pi OS](#installing-raspberry-pi-os)
  - [Updating the Raspberry Pi](#updating-the-raspberry-pi)
  - [Cloning the Repository](#cloning-the-repository)
  - [Installing Required Packages](#installing-required-packages)
  - [Configuring ALSA for Audio Output](#configuring-alsa-for-audio-output)
  - [Creating and Deploying Udev Rules](#creating-and-deploying-udev-rules)
  - [Creating and Enabling the Service](#creating-and-enabling-the-service)
- [Checking the Logs](#checking-the-logs)
- [Troubleshooting](#troubleshooting)

## Setup

### Installing Raspberry Pi OS

1. Download the Raspberry Pi Imager from the official Raspberry Pi website: [Raspberry Pi Imager](https://www.raspberrypi.org/software/)
2. Install and run the Raspberry Pi Imager.
3. Select "Raspberry Pi OS (32-bit)" as the operating system.
4. Choose your SD card and click "WRITE" to start the installation process.
5. Once the process is complete, insert the SD card into your Raspberry Pi and power it on.

### Updating the Raspberry Pi

First, ensure your Raspberry Pi is up-to-date. Open a terminal and run:

    sudo apt update
    sudo apt upgrade -y

### Cloning the Repository

Clone the GitHub repository to your Raspberry Pi:

    git clone https://github.com/your-username/zeughaus-switch.git
    cd zeughaus-switch

### Installing Required Packages

You need to install Python and necessary libraries, as well as `alsa-utils` for sound management:

    sudo apt install python3 python3-venv python3-pip alsa-utils

Next, create a virtual environment for your project:

    python3 -m venv ~/zeughaus-switch/env
    source ~/zeughaus-switch/env/bin/activate

### Installing Python Libraries

Install the required Python libraries using pip:

    pip install evdev

### Configuring ALSA for Audio Output

To configure ALSA to use the audio jack, open the `alsa.conf` file:

    sudo nano /usr/share/alsa/alsa.conf

Find the following lines:

    defaults.ctl.card 0
    defaults.pcm.card 0

Change them to:

    defaults.ctl.card 1
    defaults.pcm.card 1

Save and exit the file.

### Creating and Deploying Udev Rules

Copy your `99-footswitch.rules` file to the correct directory to set up udev rules:

    sudo cp /home/pi/zeughaus-switch/99-footswitch.rules /etc/udev/rules.d/
    sudo udevadm control --reload-rules
    sudo udevadm trigger

### Creating and Enabling the Service

Copy your service file to the systemd directory:

    sudo cp /home/pi/zeughaus-switch/zeughaus.service /etc/systemd/system/

Reload the systemd daemon to recognize the new service:

    sudo systemctl daemon-reload

Enable the service to start on boot:

    sudo systemctl enable zeughaus.service

Start the service:

    sudo systemctl start zeughaus.service

## Checking the Logs

To see the logs for the service and troubleshoot any issues, you can use the following command:

    sudo journalctl -u zeughaus.service -f

## Troubleshooting

If the footswitches are not recognized after a reboot, make sure the udev rules are correctly applied and check for any errors in the logs.

To stop the service:

    sudo systemctl stop zeughaus.service

To restart the service:

    sudo systemctl restart zeughaus.service

To check the status of the service:

    sudo systemctl status zeughaus.service

For any issues with audio output, ensure that ALSA is configured correctly and that the correct audio device is set.
