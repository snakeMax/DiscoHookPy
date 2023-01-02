import tkinter as tk
from tkinter import ttk
import requests
import configparser

# init
window = tk.Tk()
toolbar = ttk.Frame(window)
toolbar.pack(side="top", fill="x")
window.title("Discord Webhook")

def get_url():
    config.read('config.ini')
    if 'WebhookURL' in config['DEFAULT']:
        url = config['DEFAULT']['WebhookURL']
    else:
        url = "none"
    return url

# init
config = configparser.ConfigParser()
webhook_url = get_url()

# functions executed from toolbar buttons

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

def show_help():
    pass

# functions to send the hook
def send_message(message):
    data = {"content": message}
    webhook_url = get_url()
    if webhook_url == "none":
        show_edit()
    else:
        requests.post(webhook_url, json=data)

def on_button_click():
    message = text_box.get("1.0", "end")
    send_message(message)

# textbox where content is typed by user (must be under send function)
text_box = tk.Text(window)
text_box.pack()
text_box.bind("<Control-Return>", lambda event: on_button_click())

# buttons in toolbar
edit_button = ttk.Button(toolbar, text="Edit", command=show_edit)
edit_button.pack(side="left")

help_button = ttk.Button(toolbar, text="Help", command=show_help)
help_button.pack(side="left")

# button that sends hook
send_button = tk.Button(window, text="Send", command=on_button_click)
send_button.pack()

window.mainloop()