import yt_dlp
from tkinter import Tk, filedialog, Button, Label, Entry, IntVar, StringVar, Radiobutton
from tkinter import ttk

def browse_folder():
    """Open a dialog to browse for the output folder."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder_entry.delete(0, 'end')  # Clear the entry field
        output_folder_entry.insert(0, folder_selected)

def download_video():
    video_url = url_entry.get()
    output_path = output_folder_entry.get()
    file_type = file_type_var.get()

    if not video_url or not output_path:
        status_label.config(text="Please provide both URL and output folder.")
        return

    # Reset the progress bar and status label
    progress_var.set(0)
    status_label.config(text="Starting download...")

    # Define yt-dlp options based on file type selection (MP4 or MP3)
    if file_type == "mp4":
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],  # Hook to update progress bar
        }
    elif file_type == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [progress_hook],  # Hook to update progress bar
        }

    try:
        # Download the video using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    except Exception as e:
        status_label.config(text=f"An error occurred: {e}")

def progress_hook(d):
    """Update the progress bar based on the download progress."""
    if d['status'] == 'downloading':
        total_size = d.get('total_bytes', 0)
        downloaded_size = d.get('downloaded_bytes', 0)

        if total_size > 0:
            percent = int(downloaded_size * 100 / total_size)
            progress_var.set(percent)  # Update the progress bar

        # Update the ETA and progress message
        eta = d.get('eta', 0)
        status_label.config(text=f"Downloading... {percent}% complete, ETA: {eta} seconds")

    elif d['status'] == 'finished':
        progress_var.set(100)  # Set progress bar to 100% on completion
        status_label.config(text="Download complete!")

# Creating the GUI
root = Tk()
root.title("YouTube Video Downloader")

# Labels and input fields
Label(root, text="YouTube Video URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10)
output_folder_entry = Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=10)

# Browse button for folder selection
browse_button = Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=2, padx=10, pady=10)

# File type selection (MP4 or MP3)
file_type_var = StringVar(value="mp4")  # Default to MP4
Label(root, text="Select File Type:").grid(row=2, column=0, padx=10, pady=10)
Radiobutton(root, text="MP4 (Video)", variable=file_type_var, value="mp4").grid(row=2, column=1, sticky="W")
Radiobutton(root, text="MP3 (Audio)", variable=file_type_var, value="mp3").grid(row=2, column=1, padx=150, sticky="W")

# Progress bar
progress_var = IntVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", variable=progress_var, maximum=100)
progress_bar.grid(row=3, column=1, padx=10, pady=10)

# Download button
download_button = Button(root, text="Download", command=download_video)
download_button.grid(row=4, column=1, pady=20)

# Status label
status_label = Label(root, text="")
status_label.grid(row=5, column=1, pady=10)

root.mainloop()
