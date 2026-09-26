import os
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


APP_DIR = os.path.dirname(os.path.abspath(__file__))


def find_ffmpeg():
    bundled = os.path.join(APP_DIR, "ffmpeg.exe")
    if os.path.isfile(bundled):
        return bundled
    return shutil.which("ffmpeg")


class USALBBroadcaster:
    def __init__(self, root):
        self.root = root
        self.root.title("USALB Radio 24 Broadcaster")
        self.root.geometry("760x560")
        self.root.minsize(680, 500)
        self.process = None

        self.server = tk.StringVar(value="79.106.124.110")
        self.port = tk.StringVar(value="8005")
        self.mount = tk.StringVar(value="/")
        self.username = tk.StringVar(value="usalb")
        self.password = tk.StringVar()
        self.audio_file = tk.StringVar()
        self.microphone = tk.StringVar()
        self.status = tk.StringVar(value="OFFLINE")

        self.build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def build_ui(self):
        outer = ttk.Frame(self.root, padding=16)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="USALB Radio 24", font=("Segoe UI", 22, "bold")).pack(anchor="w")
        ttk.Label(outer, text="Live Broadcaster").pack(anchor="w", pady=(0, 14))

        connection = ttk.LabelFrame(outer, text="AzuraCast / Icecast", padding=10)
        connection.pack(fill="x", pady=6)
        self.add_field(connection, "Server", self.server, 0)
        self.add_field(connection, "Port", self.port, 1)
        self.add_field(connection, "Mount", self.mount, 2)
        self.add_field(connection, "Username", self.username, 3)

        ttk.Label(connection, text="Password", width=12).grid(row=4, column=0, sticky="w", pady=4)
        ttk.Entry(connection, textvariable=self.password, show="*", width=58).grid(row=4, column=1, sticky="ew", padx=6, pady=4)

        source = ttk.LabelFrame(outer, text="Audio source", padding=10)
        source.pack(fill="x", pady=6)
        ttk.Label(source, text="Audio file").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(source, textvariable=self.audio_file, width=56).grid(row=0, column=1, padx=6, pady=4)
        ttk.Button(source, text="Browse", command=self.choose_file).grid(row=0, column=2, pady=4)
        ttk.Label(source, text="Microphone (optional)").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(source, textvariable=self.microphone, width=56).grid(row=1, column=1, padx=6, pady=4)
        ttk.Label(source, text="Example: Microphone (Realtek(R) Audio)").grid(row=1, column=2, sticky="w", padx=4)

        controls = ttk.Frame(outer)
        controls.pack(fill="x", pady=14)
        self.start_button = ttk.Button(controls, text="START LIVE", command=self.start)
        self.start_button.pack(side="left")
        self.stop_button = ttk.Button(controls, text="STOP", command=self.stop, state="disabled")
        self.stop_button.pack(side="left", padx=8)
        ttk.Label(controls, textvariable=self.status, font=("Segoe UI", 12, "bold")).pack(side="left", padx=16)

        log_frame = ttk.LabelFrame(outer, text="Broadcast log", padding=6)
        log_frame.pack(fill="both", expand=True, pady=6)
        self.log = tk.Text(log_frame, height=12, state="disabled", wrap="word")
        self.log.pack(fill="both", expand=True)
        ttk.Label(outer, text="Your password stays in this app and is never written to GitHub.").pack(anchor="w", pady=(6, 0))

    def add_field(self, parent, label, variable, row):
        ttk.Label(parent, text=label, width=12).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(parent, textvariable=variable, width=58).grid(row=row, column=1, sticky="ew", padx=6, pady=4)

    def choose_file(self):
        filename = filedialog.askopenfilename(
            title="Choose audio",
            filetypes=[("Audio files", "*.mp3 *.wav *.m4a *.aac *.flac *.ogg"), ("All files", "*.*")]
        )
        if filename:
            self.audio_file.set(filename)

    def write_log(self, message):
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def build_command(self):
        ffmpeg = find_ffmpeg()
        if not ffmpeg:
            raise FileNotFoundError("FFmpeg not found. Install FFmpeg or place ffmpeg.exe beside the broadcaster.")

        server = self.server.get().strip()
        port = self.port.get().strip()
        mount = self.mount.get().strip() or "/"
        username = self.username.get().strip()
        password = self.password.get()
        audio = self.audio_file.get().strip()
        microphone = self.microphone.get().strip()

        if not server or not port or not username or not password:
            raise ValueError("Server, Port, Username and Password are required.")
        if not audio and not microphone:
            raise ValueError("Choose an audio file or enter a microphone device.")

        command = [ffmpeg, "-hide_banner", "-loglevel", "warning"]
        if audio:
            command += ["-re", "-stream_loop", "-1", "-i", audio]
        if microphone:
            command += ["-f", "dshow", "-i", f"audio={microphone}"]

        if audio and microphone:
            command += [
                "-filter_complex",
                "[0:a][1:a]amix=inputs=2:duration=longest:dropout_transition=2[a]",
                "-map", "[a]"
            ]
        else:
            command += ["-map", "0:a"]

        safe_password = (password.replace("%", "%25").replace("@", "%40")
                         .replace(":", "%3A").replace("/", "%2F")
                         .replace("#", "%23").replace("?", "%3F"))
        destination = f"icecast://{username}:{safe_password}@{server}:{port}{mount}"

        command += [
            "-vn", "-c:a", "libmp3lame", "-b:a", "128k",
            "-ar", "44100", "-ac", "2", "-content_type", "audio/mpeg",
            "-f", "mp3", destination
        ]
        return command

    def start(self):
        if self.process is not None:
            return
        try:
            command = self.build_command()
            self.process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
        except FileNotFoundError as exc:
            messagebox.showerror("FFmpeg not found", str(exc))
            return
        except ValueError as exc:
            messagebox.showerror("Missing information", str(exc))
            return
        except Exception as exc:
            messagebox.showerror("Could not start", str(exc))
            return

        self.status.set("LIVE")
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.write_log("Connecting to USALB Radio 24...")
        threading.Thread(target=self.read_process, daemon=True).start()

    def read_process(self):
        process = self.process
        if process is None:
            return
        for line in iter(process.stdout.readline, ""):
            if line:
                self.root.after(0, self.write_log, line.rstrip())
        code = process.wait()
        self.root.after(0, self.process_finished, code)

    def process_finished(self, code):
        if self.process is not None:
            self.write_log(f"Broadcast stopped (FFmpeg exit code {code}).")
        self.process = None
        self.status.set("OFFLINE")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def stop(self):
        if self.process is None:
            return
        self.write_log("Stopping broadcast...")
        try:
            self.process.terminate()
        except Exception:
            pass
        self.status.set("STOPPING")

    def close(self):
        if self.process is not None:
            try:
                self.process.terminate()
            except Exception:
                pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = USALBBroadcaster(root)
    root.mainloop()
