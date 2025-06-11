import requests
import json
import tkinter as tk
from tkinter import messagebox

# Function to fetch kill data from zKillboard API
def fetch_kill_data(character_id):
    """
    Fetches killmail data for a given EVE Online character ID from zKillboard.

    Args:
        character_id (int): The EVE Online character ID.

    Returns:
        list: A list of killmail dictionaries, or an empty list if fetching fails.
    """
    url = f"https://zkillboard.com/api/kills/characterID/{character_id}/"
    headers = {"Accept-Encoding": "gzip", "User-Agent": "zkillboard-isk-calculator"} # Added a User-Agent header
    try:
        response = requests.get(url, headers=headers, timeout=10) # Added a timeout
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for character ID {character_id}: {e}")
        return []

# Function to calculate total ISK destroyed from unique kills
def calculate_total_isk(character_ids):
    """
    Calculates the total ISK destroyed across unique killmails for a list of character IDs.

    Args:
        character_ids (list): A list of integer character IDs.

    Returns:
        float: The total ISK destroyed.
    """
    unique_kills = {}
    
    for character_id in character_ids:
        kills = fetch_kill_data(character_id)
        for kill in kills:
            kill_id = kill.get('killmail_id')
            # Ensure 'zkb' key exists and then get 'destroyedValue'
            isk_value = kill.get('zkb', {}).get('destroyedValue', 0)
            
            if kill_id and kill_id not in unique_kills: # Ensure kill_id is not None
                unique_kills[kill_id] = isk_value
    
    total_isk = sum(unique_kills.values())
    return total_isk

# --- GUI Part ---

def calculate_isk_gui():
    """
    Handles the calculation when the GUI button is clicked.
    Retrieves character IDs from the input, performs the calculation,
    and displays the result or an error message.
    """
    ids_input = id_entry.get()
    if not ids_input:
        messagebox.showwarning("Input Error", "Please enter at least one character ID.")
        return

    character_ids_str = ids_input.split(',')
    character_ids = []
    for id_str in character_ids_str:
        try:
            character_ids.append(int(id_str.strip()))
        except ValueError:
            messagebox.showerror("Input Error", f"Invalid character ID: '{id_str.strip()}'. Please enter numbers only, separated by commas.")
            return
    
    # Clear previous result
    result_label.config(text="Calculating...")
    root.update_idletasks() # Update GUI to show "Calculating..." immediately

    total_isk_destroyed = calculate_total_isk(character_ids)
    result_label.config(text=f"Total ISK destroyed (unique kills only): {total_isk_destroyed:,.2f} ISK")

# Setup the main application window
root = tk.Tk()
root.title("zKillboard ISK Calculator")
root.geometry("1350x750") # Increased window size to 3 times (450*3=1350, 250*3=750)
root.resizable(False, False) # Prevent resizing for simplicity

# Styling
bg_color = "#343a40" # Dark grey
text_color = "#f8f9fa" # Light grey
button_color = "#007bff" # Blue
button_active_color = "#0056b3" # Darker blue
entry_bg = "#495057" # Medium grey
entry_fg = "#f8f9fa" # Light grey

root.configure(bg=bg_color)

# Frame for better layout
main_frame = tk.Frame(root, bg=bg_color, padx=20, pady=20)
main_frame.pack(expand=True, fill="both")

# Instructions Label
instruction_label = tk.Label(
    main_frame,
    text="Enter EVE Online Character IDs (comma-separated):",
    bg=bg_color,
    fg=text_color,
    font=("Inter", 16, "bold") # Increased font size
)
instruction_label.pack(pady=(0, 20))

# Entry widget for IDs
id_entry = tk.Entry(
    main_frame,
    width=70, # Increased width to accommodate larger window
    bg=entry_bg,
    fg=entry_fg,
    insertbackground=entry_fg, # Cursor color
    font=("Inter", 14), # Increased font size
    relief="flat",
    bd=2
)
id_entry.pack(pady=10, ipady=10) # Add more inner padding

# Example text (placeholder)
id_entry.insert(0, "e.g., 93382481, 2113893486")
# Clear placeholder on focus
def clear_placeholder(event):
    if id_entry.get() == "e.g., 93382481, 2113893486":
        id_entry.delete(0, tk.END)
        id_entry.config(fg=entry_fg) # Set text color to normal after clearing

def restore_placeholder(event):
    if not id_entry.get():
        id_entry.insert(0, "e.g., 93382481, 2113893486")
        id_entry.config(fg="grey") # Set text color to grey for placeholder

id_entry.bind("<FocusIn>", clear_placeholder)
id_entry.bind("<FocusOut>", restore_placeholder)


# Calculate Button
calculate_button = tk.Button(
    main_frame,
    text="Calculate ISK",
    command=calculate_isk_gui,
    bg=button_color,
    fg=text_color,
    font=("Inter", 16, "bold"), # Increased font size
    relief="raised",
    bd=0,
    padx=20, # Increased padding
    pady=10, # Increased padding
    activebackground=button_active_color,
    activeforeground=text_color,
    cursor="hand2"
)
calculate_button.pack(pady=30)

# Result Label
result_label = tk.Label(
    main_frame,
    text="Total ISK destroyed (unique kills only): 0.00 ISK",
    bg=bg_color,
    fg=text_color,
    font=("Inter", 20, "bold") # Increased font size significantly for result
)
result_label.pack(pady=(0, 20))

# Start the Tkinter event loop
root.mainloop()
