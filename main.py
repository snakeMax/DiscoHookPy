import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import requests
import re
import json
import configparser

# init
window = tk.Tk()
toolbar = ttk.Frame(window)
toolbar.pack(side="top", fill="x")
window.title("Discord Webhook Publisher")

def is_valid_url(url):
    regex = re.compile(r'^(?:http|ftp)s?://', re.IGNORECASE)
    return re.match(regex, url) is not None

def get_url():
    config.read('config.ini')
    if 'WebhookURL' in config['DEFAULT'] and is_valid_url(config['DEFAULT']['WebhookURL']):
        url = config['DEFAULT']['WebhookURL']
        print("URL found")
    else:
        print("Invalid URL, or none was provided")
        url = "none"
    return url


# init var
config = configparser.ConfigParser()
webhook_url = get_url()
webhook_urls = ["Choose"]

# save webhooks
def save_webhook_urls():
    # Serialize the list of webhook URLs to a JSON string
    webhook_urls_json = json.dumps(webhook_urls)

    # Write the JSON string to the config file
    with open("config.json", "w") as config_file:
        config_file.write(webhook_urls_json)

# Define the function to edit settings
def show_edit(debug=False):
    # Create a new window
    edit_window = tk.Toplevel(window)
    edit_window.title("Edit Settings")

    # Create a label and a text box for the webhook URL
    url_label = tk.Label(edit_window, text="Webhook URL:")
    url_label.pack(side="left")
    url_entry = tk.Entry(edit_window)
    url_entry.pack(side="left")

    # Create a "Save" button
    save_button = tk.Button(edit_window, text="Save", command=lambda: edit_settings(edit_window, url_entry.get(), debug))
    save_button.pack(side="left")

# Define the function to save settings
def edit_settings(window, url, debug):
    # Write the webhook URL to a configuration file
    config['DEFAULT'] = {'WebhookURL': url}
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

    if debug:
        on_button_click()
    window.destroy()

# function that displays all shortcut keys
def show_shortcuts():
    shortcuts_window = tk.Toplevel(window)
    shortcuts_window.title("Keyboard Shortcuts")

    # Create a label with the message
    message = "Press Ctrl+Enter to send the message (if you don't feel like pressing send)"
    label = tk.Label(shortcuts_window, text=message)
    label.pack()

# functions to send the hook
def send_message(url, message, color):

    hex_color = color
    color = int("0x" + hex_color[1:], 16)

    if is_valid_url(url):
        data = {
        "embeds": [{
            "title": "Message",
            "color": color,
            "description": message
        }]
        }
        requests.post(url, json=data)
    else:
        show_edit()


def on_button_click():
    message = text_box.get("1.0", "end")
    send_message(get_url(), message, color_picker.get())

# textbox where content is typed by user (must be under send function)
text_box = tk.Text(window)
text_box.pack()
text_box.bind("<Control-Return>", lambda: on_button_click())

# create the toolobar menu with dropdowns
settings_menu = tk.Menu(toolbar, tearoff=0)
help_menu = tk.Menu(toolbar, tearoff=0)

# Create the "Webhook url" button under a dropdown called "Settings""
settings_menu.add_command(label="Webhook url", command=show_edit)

settings_dropdown = ttk.Menubutton(toolbar, text="Settings", menu=settings_menu)
settings_dropdown.pack(side="left")

# Create the "Shortcuts" button under a dropdown called "Help"
help_menu.add_command(label="Shortcuts", command=show_shortcuts)

help_dropdown = ttk.Menubutton(toolbar, text="Help", menu=help_menu)
help_dropdown.pack(side="left")

# Create the webhook URL variable and dropdown menu
webhook_url_var = tk.StringVar(value=webhook_urls[0])
webhook_url_menu = ttk.OptionMenu(toolbar, webhook_url_var, *webhook_urls)
webhook_url_menu.pack(side="left")

# Add a label to display the "Webhook URL:" text
webhook_url_label = tk.Label(toolbar, text="Webhook URL:")
webhook_url_label.pack(side="left")

# Create the URL text field and "Add" button
def add_url():
    new_url = url_text_field.get()
    webhook_urls.append(new_url)
    webhook_url_menu.set_menu(*webhook_urls)
    url_text_field.delete()


url_text_field = tk.Entry(toolbar)
url_text_field.pack(side="left")
add_button = tk.Button(toolbar, text="Add", command=add_url)
add_button.pack(side="left")

# Define the function to add a new URL to the list




# color picker
color_picker = tk.StringVar(value="#ff0000")
color_button = tk.Button(toolbar, bg=color_picker.get(), command=lambda: color_picker.set(colorchooser.askcolor()[1]))
color_button.pack(side="right")

color_button.config(height=2, width=5)

color_label = tk.Label(toolbar, text="Color:")
color_label.pack(side="right")

# Update the button's background color when the color picker variable is changed
color_picker.trace("w", lambda *args: color_button.config(bg=color_picker.get()))

# button that sends hook
send_button = tk.Button(window, text="Send", command=on_button_click)
send_button.pack()

window.mainloop()