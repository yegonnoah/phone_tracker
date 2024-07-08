import tkinter as tk
from tkinter import messagebox, Text
from tkinter.ttk import Button, Style, Label, Frame, Entry
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
from geopy.geocoders import Nominatim
import tkintermapview
from key import key  

# Login Functionality
def login():
    user = username.get()
    pwd = password.get()
    
    # Simple username and password check
    if user == "admin" and pwd == "password":
        login_window.destroy()
        show_main_app()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

# Main Application Functionality
def show_main_app():
    root = tk.Tk()  
    root.geometry("800x600")  

    label1 = Label(root, text="Phone Number Tracker", font=('Helvetica', 18, 'bold'))
    label1.pack(pady=10)

    def getResult():
        num = number.get("1.0", tk.END).strip()
        try:
            num1 = phonenumbers.parse(num)
        except:
            messagebox.showerror("Error", "Number box is empty or the input is not numeric!!")
            return

        location = geocoder.description_for_number(num1, "en")
        service_provider = carrier.name_for_number(num1, "en")

        ocg = OpenCageGeocode(key)
        query = str(location)
        results = ocg.geocode(query)

        if not results:
            messagebox.showerror("Error", "Could not get location data!!")
            return

        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']

        # Clear previous map and results
        if hasattr(root, 'map_frame'):
            root.map_frame.destroy()

        # Create a frame for the map
        map_frame = Frame(root)
        map_frame.pack(pady=20)
        root.map_frame = map_frame  # Store a reference to map_frame in root

        # Assuming tkintermapview provides a map widget
        map_widget = tkintermapview.TkinterMapView(map_frame, width=600, height=400)
        map_widget.set_position(lat, lng)
        map_widget.set_marker(lat, lng, text="Phone Location")
        map_widget.set_zoom(15)  
        map_widget.pack()

        # Reverse geocode using geopy's Nominatim
        geolocator = Nominatim(user_agent="phone_tracker")
        location = geolocator.reverse((lat, lng))

        # Display other details in the result Text widget
        result.delete(1.0, tk.END)
        result.insert(tk.END, "The country of this number is: " + location.address.split(',')[-1] + "\n")
        result.insert(tk.END, "The service provider of this number is: " + service_provider + "\n")
        result.insert(tk.END, "Latitude is: " + str(lat) + "\n")
        result.insert(tk.END, "Longitude is: " + str(lng) + "\n")

    number = Text(root, height=1, font=('Helvetica', 10))
    number.pack(pady=10)

    style = Style()
    style.configure("TButton", font=('Helvetica', 14, 'bold'), borderwidth='4')
    style.map('TButton', foreground=[('active', '!disabled', 'green')],
                         background=[('active', 'black')])

    button = Button(root, text="Search", command=getResult)
    button.pack(pady=10, padx=100)

    result = Text(root, height=7, font=('Helvetica', 12))
    result.pack(pady=10)

    root.mainloop()

# Login Window
login_window = tk.Tk()
login_window.geometry("400x300")
login_window.title("Login")

# Frame for login form
frame = tk.Frame(login_window, bg='#7f8fa6', bd=5)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.75, relheight=0.75)

label_user = tk.Label(frame, text="Username", font=('Arial', 12), bg='#7f8fa6')
label_user.pack(pady=5)
username = tk.Entry(frame, font=('Garamond', 12))
username.pack(pady=5)

label_pwd = tk.Label(frame, text="Password", font=('Arial', 12), bg='#7f8fa6')
label_pwd.pack(pady=5)
password = tk.Entry(frame, show="*", font=('Garamond', 12))
password.pack(pady=5)

login_button = Button(frame, text="Login", command=login)
login_button.pack(pady=20)

login_window.mainloop()
