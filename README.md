# Video Violence Detection with User Authentication

This project implements a video violence detection application with user authentication and alert functionalities. Users can register and log in to the application. The application analyzes live video or video files for violence and sends an alert message if violence is detected for a certain number of consecutive frames.

## Features

* User authentication with registration and login
* Live video and video file analysis for violence detection
* Alert notification with WhatsApp message upon violence detection
* Device location and time logging for violence alerts

## Dependencies

* Python 3.x
* tkinter
* sqlite3
* OpenCV
* NumPy
* threading
* Pygame
* Twilio (for WhatsApp messaging)
* tensorflow (for violence detection model)
* requests

## How to Run

1. Install the required dependencies using `pip install requirements.txt`.
2. Replace the placeholder paths in the code for the violence detection model (`modelnew.h5`) and audio alarm tone (`alarm_tone.mp3`).
3. Configure your Twilio account credentials (`account_sid` and `auth_token`) for WhatsApp messaging.
4. Run the application using `python main.py`.

## Usage

* Login or register a new user.
* Select "Live Video" or "Video File" as the source.
* Start video analysis.
* The application will display the analysis result and send an alert message if violence is detected.

NOTE: You need to re-run the code after signing up

## Disclaimer

This application is for educational purposes only. It is not intended for real-world deployment and may not be fully accurate in detecting violence in all scenarios.
