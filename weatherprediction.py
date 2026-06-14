import tkinter as tk
from tkinter import messagebox
import requests

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name!")
        return
        
    # Your active OpenWeatherMap API Key
    api_key = "2399e835e21801777eaa832a76818008" 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url).json()
        
        if response.get("cod") != 200:
            messagebox.showerror("City Not Found", f"Error: {response.get('message', 'Could not fetch data')}")
            return
            
        # Safe Parsing using .get() to prevent unexpected KeyErrors
        city_name = response.get("name", "Unknown City")
        country = response.get("sys", {}).get("country", "")
        
        main_data = response.get("main", {})
        temp = main_data.get("temp", 0.0)
        humidity = main_data.get("humidity", 0)
        
        weather_list = response.get("weather", [{}])[0]
        condition = weather_list.get("main", "UNKNOWN").upper()
        desc = weather_list.get("description", "No description available").capitalize()
        
        # Dynamic Styling Configuration based on Weather Conditions
        if "CLEAR" in condition:
            weather_bg = "#fef9c3"  # Sunny Yellow Card
            weather_fg = "#a16207"  # Golden Amber Text
            status_icon = "☀️"
        elif "RAIN" in condition or "DRIZZLE" in condition:
            weather_bg = "#dbeafe"  # Soft Rain Blue Card
            weather_fg = "#1d4ed8"  # Deep Royal Blue Text
            status_icon = "🌧️"
        elif "CLOUD" in condition or "CLOUDS" in condition:
            weather_bg = "#f1f5f9"  # Overcast Gray Card
            weather_fg = "#475569"  # Slate Gray Text
            status_icon = "☁️"
        elif "SNOW" in condition:
            weather_bg = "#f0fdfa"  # Crisp Ice Teal Card
            weather_fg = "#0f766e"  # Deep Teal Text
            status_icon = "❄️"
        else:
            weather_bg = "#fae8ff"  # Purple tint for Storm/Mist/Atmosphere
            weather_fg = "#86198f"  # Rich Magenta
            status_icon = "🌫️"

        # Update Card Canvas and Labels dynamically
        results_card.config(bg=weather_bg, highlightbackground=weather_fg, highlightthickness=2)
        
        location_string = f"📍 {city_name}, {country}" if country else f"📍 {city_name}"
        location_lbl.config(text=location_string, bg=weather_bg, fg="#0f172a")
        
        temp_lbl.config(text=f"{temp:.1f}°C", bg=weather_bg, fg=weather_fg)
        metrics_lbl.config(text=f"{status_icon} {condition} ({desc})\n💧 Humidity: {humidity}%", bg=weather_bg, fg="#334155")
        
    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error", "Unable to connect to the weather network. Check internet connection!")

# --- UI Setup ---
root = tk.Tk()
root.title("Vibrant Weather Tracker")
root.geometry("420x550")
root.configure(bg="#f1f5f9") 

# Top Header Banner - Ocean Teal Accent
header_frame = tk.Frame(root, bg="#0d9488", height=90)
header_frame.pack(fill="x")
header_frame.pack_propagate(False)

title_lbl = tk.Label(header_frame, text="⚡ METEOROLOGICAL METRICS ⚡", font=("Helvetica", 13, "bold"), fg="#ffffff", bg="#0d9488")
title_lbl.pack(pady=32)

# Central Content Frame
main_frame = tk.Frame(root, bg="#f1f5f9")
main_frame.pack(pady=20, padx=40, fill="both", expand=True)

# Input Field setup
lbl = tk.Label(main_frame, text="🔍 ENTER CITY OR ZIP CODE", font=("Helvetica", 10, "bold"), fg="#0f172a", bg="#f1f5f9")
lbl.pack(anchor="w", pady=(5, 2))

city_entry = tk.Entry(main_frame, font=("Helvetica", 13, "bold"), bg="#ffffff", fg="#0f172a", 
                      insertbackground="#0d9488", bd=1, relief="solid")
city_entry.pack(fill="x", ipady=8, pady=(0, 5))

# Action Button - Coral Pink / Red
fetch_btn = tk.Button(
    main_frame, 
    text="FETCH LIVE WEATHER", 
    font=("Helvetica", 11, "bold"), 
    bg="#e11d48", 
    fg="white", 
    activebackground="#be123c", 
    activeforeground="white",
    bd=0, 
    relief="flat",
    command=get_weather,
    cursor="hand2"
)
fetch_btn.pack(fill="x", ipady=10, pady=20)

# Display Results Card
results_card = tk.Frame(main_frame, bg="#ffffff", highlightbackground="#cbd5e1", highlightthickness=1)
results_card.pack(fill="x", ipady=20, pady=5)

location_lbl = tk.Label(results_card, text="Awaiting location...", font=("Helvetica", 12, "bold"), fg="#64748b", bg="#ffffff")
location_lbl.pack(pady=(5, 2))

temp_lbl = tk.Label(results_card, text="--°C", font=("Helvetica", 28, "bold"), fg="#94a3b8", bg="#ffffff")
temp_lbl.pack(pady=2)

metrics_lbl = tk.Label(results_card, text="Status: IDLE", font=("Helvetica", 11, "normal"), fg="#94a3b8", bg="#ffffff")
metrics_lbl.pack(pady=(2, 5))

root.mainloop()