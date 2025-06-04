import requests
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
def create_gradient(canvas, width, height, color1, color2):
    """Creates a vertical gradient on the given canvas."""
    gradient_steps = 256
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    r_ratio = (r2 - r1) / gradient_steps
    g_ratio = (g2 - g1) / gradient_steps
    b_ratio = (b2 - b1) / gradient_steps
    for i in range(gradient_steps):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
        canvas.create_line(0, i * (height / gradient_steps), width, i * (height / gradient_steps), fill=color)
def fetch_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return
    api_key = "d4e551e5caa31684451260a637d3243f"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        data = response.json()
        if data["cod"] != 200:
            messagebox.showerror("Error", data["message"].capitalize())
            return
        city_name = data["name"]
        temperature = data["main"]["temp"]
        weather = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        visibility = data["visibility"]
        icon_code = data["weather"][0]["icon"]
        weather_label.config(text=f"{city_name}")
        temp_label.config(text=f"{temperature}°C")
        desc_label.config(text=f"{weather}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        pressure_label.config(text=f"Pressure: {pressure} hPa")
        visibility_label.config(text=f"Visibility: {visibility} m")
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        try:
            icon_img = ImageTk.PhotoImage(Image.open(requests.get(icon_url, stream=True).raw))
            weather_icon.config(image=icon_img)
            weather_icon.image = icon_img
        except Exception:
            weather_icon.config(text="(Icon not available)", image="")
        if city_name not in search_history:
            search_history.insert(0, city_name)
            update_history_listbox()
    except Exception as e:
        messagebox.showerror("Error", f"Unable to fetch data: {e}")
def update_history_listbox():
    """Update the ListBox with the current search history."""
    location_list.delete(0, END)
    for location in search_history:
        location_list.insert(END, location)
def reset_app():
    city_entry.delete(0, END)
    weather_label.config(text="City")
    temp_label.config(text="Temp")
    desc_label.config(text="Condition")
    humidity_label.config(text="Humidity")
    pressure_label.config(text="Pressure")
    visibility_label.config(text="Visibility")
    weather_icon.config(image="")
def exit_app():
    app.destroy()
app = Tk()
app.title("Modern Weather App")
app.geometry("1200x700")
app.resizable(False, False)
canvas = Canvas(app, width=1200, height=700, highlightthickness=0)
canvas.pack(fill="both", expand=True)
create_gradient(canvas, 1200, 700, "#dfefff", "#367ce8")
sidebar = Frame(app, bg="#1e1e1e", width=300)
sidebar.place(relx=0, rely=0, relheight=1)
sidebar_title = Label(sidebar, text="Weather App", bg="#1e1e1e", fg="#ffffff", font=("Arial", 20))
sidebar_title.pack(pady=20)
city_entry = Entry(sidebar, font=("Helvetica", 16), width=20, bd=2, relief=FLAT)
city_entry.pack(pady=10, padx=20)
search_button = Button(sidebar, text="Search 🔍", font=("Helvetica", 14), bg="#ecf0f1", fg="#2c3e50",
                       command=fetch_weather, bd=0, padx=10, pady=5, activebackground="#bdc3c7")
search_button.pack(pady=10)
location_list = Listbox(sidebar, bg="#1e1e1e", fg="#ffffff", font=("Arial", 14), selectbackground="#333")
location_list.pack(pady=10, padx=20, fill="both", expand=True)
footer_buttons = Frame(sidebar, bg="#2a2a2a")
footer_buttons.pack(side="bottom", fill="x", pady=10)
for text in ["Hourly", "7 Days", "Radar", "Messages"]:
    Button(footer_buttons, text=text, font=("Helvetica", 12), bg="#2a2a2a", fg="#ffffff").pack(side=LEFT, padx=10)
content = Frame(app, bg="#ecf0f1", bd=10, relief=FLAT)
content.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
weather_icon = Label(content, bg="#ecf0f1")
weather_icon.place(relx=0.05, rely=0.2)
weather_label = Label(content, text="City", font=("Helvetica", 24, "bold"), bg="#ecf0f1", fg="#34495e")
weather_label.place(relx=0.3, rely=0.2)
temp_label = Label(content, text="Temp", font=("Helvetica", 48, "bold"), bg="#ecf0f1", fg="#2c3e50")
temp_label.place(relx=0.3, rely=0.3)
desc_label = Label(content, text="Condition", font=("Helvetica", 16), bg="#ecf0f1", fg="#7f8c8d")
desc_label.place(relx=0.3, rely=0.45)
humidity_label = Label(content, text="Humidity", font=("Helvetica", 16), bg="#ecf0f1", fg="#2c3e50")
humidity_label.place(relx=0.3, rely=0.6)
pressure_label = Label(content, text="Pressure", font=("Helvetica", 16), bg="#ecf0f1", fg="#2c3e50")
pressure_label.place(relx=0.3, rely=0.7)
visibility_label = Label(content, text="Visibility", font=("Helvetica", 16), bg="#ecf0f1", fg="#2c3e50")
visibility_label.place(relx=0.3, rely=0.8)
button_frame = Frame(content, bg="#ecf0f1")
button_frame.place(relx=0.3, rely=0.9, relwidth=0.7)
Button(button_frame, text="Reset", font=("Helvetica", 12, "bold"), bg="#e74c3c", fg="white", command=reset_app,
       padx=15, pady=5).pack(side=LEFT, padx=10)
Button(button_frame, text="Exit", font=("Helvetica", 12, "bold"), bg="#e74c3c", fg="white", command=exit_app,
       padx=15, pady=5).pack(side=LEFT, padx=10)
search_history = []
app.mainloop()