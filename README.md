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

## Twilio Integration

To use Twilio in your project, you will need your Twilio `account_sid` and `auth_token`. Follow the steps below to retrieve them:

1. **Sign in to Twilio:**
   Go to the [Twilio website](https://www.twilio.com/) and sign in to your account. If you don't have an account, you'll need to create one.

2. **Navigate to the Console:**
   Once you're signed in, click on the "Console" link at the top right of the page.

3. **Find your Account SID and Auth Token:**
   In the Console, you'll see your Account SID and Auth Token on the dashboard. They are located under the "Project Info" section.

   - **Account SID**: This is a unique identifier for your Twilio account.
   - **Auth Token**: This is a secret key used to authenticate requests to the Twilio API.
   - **Twilio-Whatsapp_number**: This is the Number given after making a Twilio account.

4. **Copy the Credentials:**
   Copy your `account_sid` and `auth_token` from the dashboard. Be careful with the `auth_token`, as it is sensitive information.
   Twilio-Whatsapp_number can be found in Twilio Console under  Messaging -> Try it out-> Send a Whatsapp Message.

## How to Run

1. Install the required dependencies using `pip install requirements.txt`.
2. Go to Violence Detection System directory using `cd '.\Violence Detection System\'`
3. Replace the placeholder paths in the code for the violence detection model (`modelnew.h5`) and audio alarm tone (`alarm_tone.mp3`).
4. Configure your Twilio account credentials (`account_sid` ,`auth_token` and `from_whatsapp_number`) for WhatsApp messaging.
5. Run the application using `python '.\test copy.py'`.

## Usage

* Login or register a new user.
* Select "Live Video" or "Video File" as the source.
* Start video analysis.
* The application will display the analysis result and send an alert message if violence is detected.

NOTE: You need to re-run the code after signing up

## Disclaimer

This application is for educational purposes only. It is not intended for real-world deployment and may not be fully accurate in detecting violence in all scenarios.
