import re
from pytubefix import YouTube, Playlist
from pytube import extract, request
from urllib.request import Request, urlopen

extract._video_id_regex = re.compile(r"(?:v=|\/)([0-9A-Za-z_-]{11})")

def patched_get(url, headers=None):
    headers = headers or {"User-Agent": "Mozilla/5.0"}
    req = Request(url, headers=headers)
    return urlopen(req).read().decode()

request.get = patched_get

import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import timedelta, datetime
from tqdm import tqdm
import matplotlib.pyplot as plt

def format_time(seconds):
    return str(timedelta(seconds=int(seconds)))

def save_results_to_txt(filename, report_text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)
    return filename

def daily_breakdown(total_hours, daily_hours):
    days = total_hours / daily_hours
    plan = "\n📅 Daily Study Breakdown\n"
    plan += "Day\tHours\n"
    plan += "-" * 15 + "\n"

    remaining = total_hours
    day = 1
    while remaining > 0:
        today = min(daily_hours, remaining)
        plan += f"{day}\t{today:.2f}\n"
        remaining -= today
        day += 1

    finish_date = datetime.now().date() + timedelta(days=days)
    plan += f"\n🎯 Expected Finish Date: {finish_date}\n"
    return plan

#MAIN FUNCTION
def analyze_playlist_gui():
    url = url_entry.get().strip()
    hours_per_day = hours_entry.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a playlist URL")
        return

    try:
        hours_per_day = float(hours_per_day)
        if hours_per_day <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Enter valid hours per day")
        return

    output_box.config(state="normal")
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "⏳ Analyzing playlist...\n\n")
    window.update()

    try:
        playlist = Playlist(url)
        videos = playlist.video_urls

        report = ""
        output_box.insert(tk.END, f"📂 Playlist: {playlist.title}\n")
        output_box.insert(tk.END, f"🎬 Total Videos: {len(videos)}\n\n")

        total_seconds = processed = skipped = 0

        #progress bar in terminal
        for i, video_url in enumerate(tqdm(videos, desc="Analyzing", unit="video")):
            try:
                yt = YouTube(video_url)

                #Skip Shorts
                if yt.length < 50:
                    skipped += 1
                    continue

                total_seconds += yt.length
                processed += 1

            except:
                skipped += 1

            #Update GUI progress in title
            percent = int((i+1) / len(videos) * 100)
            window.title(f"YouTube Playlist Analyzer — {percent}%")

        if processed == 0:
            messagebox.showerror("Error", "Failed to process playlist")
            return

        avg_seconds = total_seconds / processed
        total_hours = total_seconds / 3600

        output_box.insert(tk.END, "✅ Finished!\n\n")
        output_box.insert(tk.END, f"🕒 Total Time: {format_time(total_seconds)}\n")
        output_box.insert(tk.END, f"📉 Videos Skipped (Shorts/errors): {skipped}\n")
        output_box.insert(tk.END, f"⏱ Avg Video Length: {format_time(avg_seconds)}\n\n")

        speeds = [1, 1.25, 1.5, 1.75, 2]
        time_hours = []

        output_box.insert(tk.END, "⚡ Speed vs Days\n")
        output_box.insert(tk.END, "Speed | Total Time | Days\n")
        output_box.insert(tk.END, "-" * 35 + "\n")

        for s in speeds:
            time_at_speed = total_seconds / s
            hours = time_at_speed / 3600
            time_hours.append(hours)
            days = hours / hours_per_day
            output_box.insert(tk.END, f"{s}x  | {format_time(time_at_speed)} | {days:.2f} days\n")

        #Daily breakdown
        breakdown = daily_breakdown(total_hours, hours_per_day)
        output_box.insert(tk.END, "\n" + breakdown)

        report = output_box.get(1.0, tk.END)
        file = save_results_to_txt("playlist_report.txt", report)
        output_box.insert(tk.END, f"\n📁 Report saved → {file}")

        output_box.config(state="disabled")

        # chart
        # plt.figure()
        # plt.plot(speeds, time_hours, marker='o')
        # plt.title("Playlist Completion Time vs Speed")
        # plt.xlabel("Playback Speed (x)")
        # plt.ylabel("Total Time (hours)")
        # plt.grid(True)
        # plt.show()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI
window = tk.Tk()
window.title("YouTube Playlist Analyzer")
window.geometry("1360x1300")
window.config(bg="#121212")

header = tk.Label(window, text="YouTube Playlist Analyzer",
    font=("Segoe UI", 18, "bold"), fg="#33FF57", bg="#121212")
header.pack(pady=15)

frame = tk.Frame(window, bg="#121212")
frame.pack(pady=5)

tk.Label(frame, text="Playlist URL:", font=("Segoe UI", 10), fg="white", bg="#121212").pack(anchor="w")
url_entry = tk.Entry(frame, width=60, font=("Segoe UI", 10))
url_entry.pack(pady=5)

tk.Label(frame, text="Hours per day:", font=("Segoe UI", 10), fg="white", bg="#121212").pack(anchor="w")
hours_entry = tk.Entry(frame, width=10, font=("Segoe UI", 10))
hours_entry.insert(0, "1")
hours_entry.pack(pady=5)

def on_enter(e): analyze_btn.config(bg="#00cc44")
def on_leave(e): analyze_btn.config(bg="#1DB954")

analyze_btn = tk.Button(window, text="Analyze Playlist", command=analyze_playlist_gui,
    font=("Segoe UI", 11, "bold"), bg="#1DB954", fg="black", padx=20, pady=5)
analyze_btn.pack(pady=12)
analyze_btn.bind("<Enter>", on_enter)
analyze_btn.bind("<Leave>", on_leave)

output_box = scrolledtext.ScrolledText(window, width=80, height=20,
    font=("Consolas", 10), bg="#1e1e1e", fg="white")
output_box.pack(pady=10)
output_box.config(state="disabled")

window.mainloop()
