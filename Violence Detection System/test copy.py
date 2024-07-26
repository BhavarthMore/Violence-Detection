import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
from collections import deque
import cv2
import numpy as np
import threading
import pygame
from geopy.geocoders import Nominatim
from twilio.rest import Client
from tensorflow.keras.models import load_model
import requests
from datetime import datetime
import os
import pycountry  # Import pycountry for country code validation

# Initialize pygame mixer for sound
pygame.mixer.init()
# Initialize the Twilio client
account_sid = 'YOUR_TWILIO_SID'
auth_token = 'YOUR_TWILIO_TOKEN'
client = Client(account_sid, auth_token)
audio_stop_event = threading.Event()
audio_playing = False
# Create a variable to count continuous violence frames
continuous_violence_frames = 0
url='http://ipinfo.io/json'
# Create a flag to check if a message has been sent for the current video
message_sent = False
# Create a list to store frames with detected violence
violence_frames = []

# Define result_text and result_label as global variables
result_text = None
result_label = None

from PIL import Image, ImageTk

# Function to generate QR code for WhatsApp verification
def generate_qr_code(whatsapp_number):
    # Use Twilio's API to generate QR code
    # Here, you'll use the Twilio API to generate the QR code for WhatsApp verification
    # You'll receive the QR code as a PNG file

    # Generate a dynamic file path for saving the QR code image
    qr_code_file = f"C:/Users/Admin/Violence/whatsapp_qr_code.PNG"
    return qr_code_file

# Function to display QR code as an image in the GUI
def display_qr_code(qr_image_file):
    qr_code_window = tk.Toplevel()
    qr_code_window.title("QR Code Verification")

    # Load the QR code image
    image = Image.open(qr_image_file)
    photo = ImageTk.PhotoImage(image)

    # Display the QR code image in a label
    qr_code_label = tk.Label(qr_code_window, image=photo)
    qr_code_label.image = photo  # To prevent garbage collection
    qr_code_label.pack()

# Function to create a SQLite database and table for storing user credentials
def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, whatsapp TEXT)''')  # Added WhatsApp column
    conn.commit()
    conn.close()

# Function to check if a user exists in the database
def check_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

# Function to register a new user
def register_user(username, password, whatsapp):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, whatsapp))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False  # User already exists

# Function to authenticate user login
def authenticate_user(username, password):
    user = check_user(username)
    if user and user[1] == password:
        return True  # Authentication successful
    else:
        return False  # Authentication failed

# Function to handle login button click event
def login():
    username = username_entry.get()
    password = password_entry.get()
    if authenticate_user(username, password):
        login_window.destroy()  # Close login window
        open_main_gui(username)
    else:
        login_status.set("Invalid username or password")

def open_signup_window():
    global signup_window, username_entry, password_entry, country_code_entry, whatsapp_entry, signup_status
    signup_window = tk.Toplevel()
    signup_window.title("Sign Up")

    # Create username entry
    username_label = tk.Label(signup_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(signup_window)
    username_entry.pack()

    # Create password entry
    password_label = tk.Label(signup_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(signup_window, show="*")
    password_entry.pack()

    # Create country code and WhatsApp number entry
    country_code_label = tk.Label(signup_window, text="Country Code (e.g., +1):")
    country_code_label.pack()
    country_code_entry = tk.Entry(signup_window)
    country_code_entry.pack()

    whatsapp_label = tk.Label(signup_window, text="WhatsApp Number:")
    whatsapp_label.pack()
    whatsapp_entry = tk.Entry(signup_window)
    whatsapp_entry.pack()

    # Create sign-up button
    signup_button = tk.Button(signup_window, text="Sign Up", command=sign_up)
    signup_button.pack()

    # Display sign-up status
    signup_status = tk.StringVar()
    signup_status_label = tk.Label(signup_window, textvariable=signup_status)
    signup_status_label.pack()

# Function to validate the provided mobile number
def validate_mobile_number(whatsapp_number):
    return len(whatsapp_number) >= 10 # Basic validation for mobile number length

# Function to handle sign up
def sign_up():
    username = username_entry.get()
    password = password_entry.get()
    country_code = country_code_entry.get()
    whatsapp_number = whatsapp_entry.get()
    full_whatsapp_number = country_code + whatsapp_number

    if validate_mobile_number(whatsapp_number):
        if register_user(username, password, full_whatsapp_number):
            signup_status.set("User registered successfully. Please log in.")
            # Generate QR code for WhatsApp verification
            qr_code_file = generate_qr_code(full_whatsapp_number)
            display_qr_code(qr_code_file)
        else:
            signup_status.set("Username already exists. Please choose another.")
    else:
        signup_status.set("Invalid WhatsApp number length.")

# Function to open the main application GUI
def open_main_gui(username):
    global result_text, result_label  # Declare result_text and result_label as global
    # Create the main application window
    root = tk.Tk()
    root.title("Video Violence Detection")

    # Create radio buttons to select between live video and video file
    source_var = tk.StringVar()
    live_video_button = tk.Radiobutton(root, text="Live Video", variable=source_var, value="live")
    live_video_button.pack()
    video_file_button = tk.Radiobutton(root, text="Video File", variable=source_var, value="file")
    video_file_button.pack()

    # Create a button to start video analysis based on the selected source
    start_analysis_button = tk.Button(root, text="Start Video Analysis", command=lambda: analyze_video(source_var.get(), username))
    start_analysis_button.pack(pady=10)

    # Create a label to display the analysis result
    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, fg="black")
    result_label.pack()

    # Run the GUI main loop
    root.mainloop()

def play_audio():
    global audio_playing
    try:
        pygame.mixer.music.load("alarm_tone.mp3")  # Adjust the path as needed
        pygame.mixer.music.set_volume(1.0)  # Adjust the volume if needed
        pygame.mixer.music.play()
        audio_playing = True
    except pygame.error as e:
        print("Error playing audio:", e)

def send_whatsapp_message(username, message):
    # Retrieve user details including the WhatsApp number
    user = check_user(username)
    if user:
        to_whatsapp_number = 'whatsapp:' + user[2]  # Index 2 corresponds to the WhatsApp number in the database
        from_whatsapp_number = 'whatsapp:+14155238886'  # Your Twilio WhatsApp number

        # Send the WhatsApp message using Twilio
        client.messages.create(
            body=message,
            from_=from_whatsapp_number,
            to=to_whatsapp_number
        )
        
    else:
        print("User not found.")

import requests

def get_location_info():
    try:
        response = requests.get('https://ipinfo.io/json')
        response.raise_for_status()  # Check for HTTP errors

        # Check if the response is not empty and has a valid JSON
        if response.text:
            try:
                data = response.json()
                location = data.get('loc')
                if location:
                    # Split the location data into latitude and longitude
                    lat, lon = location.split(',')
                    return str(lat), str(lon)
                else:
                    print("Location information not found in response.")
                    return None, None
            except ValueError as json_err:
                print(f'JSON decoding error: {json_err}')
                print('Response content:', response.text)
                return None, None
        else:
            print('Empty response received')
            return None, None

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None, None
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occurred: {req_err}')
        return None, None


# Define the function to analyze live video
def analyze_live_video():
    result_text.set("Analyzing live video...")
    analyze_video(source="live")

def analyze_video_file():
    result_text.set("Analyzing video file...")
    analyze_video(source="file")

    if is_violence_detected:
        result_text.set("Violence Detected")
        messagebox.showinfo("Result", "Violence Detected")
    else:
        messagebox.showinfo("Result", "No Violence Detected")

# Define a function to get the device's location
def get_device_location():
    latitude, longitude = get_location_info()
    if latitude and longitude:
        try:
            url = f'https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json'
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors

            data = response.json()
            if 'display_name' in data:
                location = data['display_name']
                return location
            else:
                return "Error: Unable to fetch location information."
        except requests.exceptions.RequestException as req_err:
            print(f'Request error occurred: {req_err}')
            return "Error: Unable to fetch location information."
        except ValueError as json_err:
            print(f'JSON decoding error: {json_err}')
            return "Error: Unable to fetch location information."
    else:
        return "Error: No location information available."

    

# Define a function to get the current time
def get_current_time():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define the function to analyze video from the selected source
def analyze_video(source, username):
    global result_text, result_label  # Declare result_text and result_label as global
    # Load the pre-trained violence detection model
    model = load_model('modelnew.h5')  # Adjust the path as needed
    Q = deque(maxlen=128)

    if source == "live":
        # Initialize video capture from the camera (0 is usually the default camera)
        cap = cv2.VideoCapture(0)
        pass
    elif source == "file":
        video_path = filedialog.askopenfilename()
        if not video_path:
            return
        cap = cv2.VideoCapture(video_path)
        pass

    count = 0
    violence_count = 0  # Counter for frames indicating violence
    continuous_violence_frames = 0  # Counter for continuous violence frames
    total_frames = 0
    violence_frame_count = 0  # Counter for consecutive frames with violence

    while True:
        # Read a frame from the video source
        ret, frame = cap.read()

        if not ret:
            break

        total_frames += 1

        # Clone the frame
        output = frame.copy()

        # Preprocess the frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (128, 128)).astype("float32")
        frame = frame.reshape(128, 128, 3) / 255

        # Make predictions on the frame and update the predictions queue
        preds = model.predict(np.expand_dims(frame, axis=0))[0]
        Q.append(preds)

        # Check if the frame indicates violence
        is_violence = (preds > 0.50)[0]
        violence_count += int(is_violence)
        result_text.set(f"Violence Detected: {violence_count / total_frames * 100:.2f}%")
        result_label.config(fg="red" if is_violence else "green")

        if is_violence:
            violence_frame_count += 1
        else:
            violence_frame_count = 0

        if is_violence and continuous_violence_frames < 30:
            continuous_violence_frames += 1
        elif continuous_violence_frames == 30 and not audio_playing:
            audio_thread = threading.Thread(target=play_audio)
            audio_thread.start()

            # Get the device location
            device_location = get_device_location()
            # Get the current date and time
            current_time = get_current_time()

            # Replace 'Camera 1' with your camera identifier
            camera_identifier = 'Camera 1'

            # Send a message if 5 consecutive frames with violence are detected
            message = f"{camera_identifier} detected violence at {device_location} on {current_time}. ALERT!"
            send_whatsapp_message(username, message)

        elif not is_violence:
            continuous_violence_frames = 0

        # Calculate the percentage of the video analyzed
        percent_analyzed = (total_frames / cap.get(cv2.CAP_PROP_FRAME_COUNT)) * 100
        result_text.set(f"Violence Detected: {violence_count / total_frames * 100:.2f}%   Analyzed: {percent_analyzed:.2f}%")

        # Display the video frame with the analysis result
        cv2.imshow("Video Analysis", output)

        # Check for the 'q' key to exit the video analysis
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # Stop audio if it's playing
    if audio_playing:
        pygame.mixer.music.stop()

    # Release the video capture and close the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    return violence_count / total_frames > 0.10  # Define your threshold for violence detection

# Create the login window
login_window = tk.Tk()
login_window.title("Login")

# Create username entry
username_label = tk.Label(login_window, text="Username:")
username_label.pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

# Create password entry
password_label = tk.Label(login_window, text="Password:")
password_label.pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

# Create login button
login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack()

# Display login status
login_status = tk.StringVar()
login_status_label = tk.Label(login_window, textvariable=login_status)
login_status_label.pack()

# Create sign-up button
signup_button = tk.Button(login_window, text="Sign Up", command=open_signup_window)
signup_button.pack()

# Create the SQLite database and table for storing user credentials
create_database()

# Run the login window main loop
login_window.mainloop()
