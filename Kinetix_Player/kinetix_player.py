import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import time
import os

# Styling Constants for the "Kinetix Player" Brand
BG_DARK = "#121212"      
PANEL_DARK = "#1E1E1E"   
ACCENT_CYAN = "#00E5FF"  
TEXT_WHITE = "#FFFFFF"   
TEXT_MUTED = "#888888"   

class KinetixPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kinetix Player - Performance Engine v1.3")
        self.root.geometry("450x580")  
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        self.create_header()
        self.create_settings_panel() 
        self.create_status_panel()
        self.create_controls()
        self.create_footer()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=BG_DARK, pady=15)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="KINETIX PLAYER", font=("Helvetica", 24, "bold"), fg=ACCENT_CYAN, bg=BG_DARK).pack()
        tk.Label(header_frame, text="Optimized Low-End Linux Gaming Android Core", font=("Helvetica", 10), fg=TEXT_MUTED, bg=BG_DARK).pack(pady=5)

    def create_settings_panel(self):
        """Interactive dropdown selector for Resolution customization."""
        config_frame = tk.Frame(self.root, bg=PANEL_DARK, bd=0, highlightbackground=ACCENT_CYAN, highlightthickness=1)
        config_frame.pack(padx=30, pady=5, fill="x")

        tk.Label(config_frame, text="ENGINE CONFIGURATION", font=("Helvetica", 10, "bold"), fg=TEXT_WHITE, bg=PANEL_DARK).pack(pady=8)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=BG_DARK, background=PANEL_DARK, foreground=TEXT_WHITE, arrowcolor=ACCENT_CYAN)

        res_frame = tk.Frame(config_frame, bg=PANEL_DARK, pady=5)
        res_frame.pack(fill="x", padx=20, pady=(0, 10))
        tk.Label(res_frame, text="Display Resolution:", font=("Helvetica", 11), fg=TEXT_WHITE, bg=PANEL_DARK).pack(side="left")
        
        self.res_choice = ttk.Combobox(res_frame, width=15, state="readonly")
        self.res_choice['values'] = ("1920x1080 (1080p)", "1600x900 (900p)", "1280x720 (720p)", "960x540 (Ultra Low-End)")
        self.res_choice.current(2)  # Default to 1280x720
        self.res_choice.pack(side="right")

    def create_status_panel(self):
        panel = tk.Frame(self.root, bg=PANEL_DARK, bd=0, highlightbackground=ACCENT_CYAN, highlightthickness=1)
        panel.pack(padx=30, pady=10, fill="both", expand=True)

        tk.Label(panel, text="ENGINE STATUS MONITOR", font=("Helvetica", 10, "bold"), fg=TEXT_WHITE, bg=PANEL_DARK).pack(pady=10)

        self.docker_status = self.create_status_line(panel, "Docker Engine Service:")
        self.container_status = self.create_status_line(panel, "Android Core Container:")
        self.adb_status = self.create_status_line(panel, "ADB Input Mapping Bridge:")

        self.update_status(self.docker_status, "READY", ACCENT_CYAN)
        self.update_status(self.container_status, "OFFLINE", TEXT_MUTED)
        self.update_status(self.adb_status, "OFFLINE", TEXT_MUTED)

    def create_status_line(self, parent, text):
        frame = tk.Frame(parent, bg=PANEL_DARK, pady=6)
        frame.pack(fill="x", padx=20)
        tk.Label(frame, text=text, font=("Helvetica", 11), fg=TEXT_WHITE, bg=PANEL_DARK, anchor="w").pack(side="left")
        status_val = tk.Label(frame, text="CHECKING", font=("Helvetica", 11, "bold"), fg=TEXT_MUTED, bg=PANEL_DARK, anchor="e")
        status_val.pack(side="right")
        return status_val

    def update_status(self, label_obj, text, color):
        label_obj.config(text=text, fg=color)

    def create_controls(self):
        control_frame = tk.Frame(self.root, bg=BG_DARK, pady=15)
        control_frame.pack(fill="x")

        self.launch_btn = tk.Button(
            control_frame,
            text="START KINETIX PLAYER",
            font=("Helvetica", 14, "bold"),
            bg=ACCENT_CYAN,
            fg=BG_DARK,
            activebackground="#00B2CC",
            activeforeground=BG_DARK,
            bd=0,
            padx=40,
            pady=12,
            cursor="hand2",
            command=self.start_engine_thread
        )
        self.launch_btn.pack()

    def create_footer(self):
        tk.Label(self.root, text="Designed for the Low-End PC Community • Build Your Career", font=("Helvetica", 9, "italic"), fg=TEXT_MUTED, bg=BG_DARK, pady=10).pack(side="bottom")

    def start_engine_thread(self):
        self.launch_btn.config(state="disabled", text="BOOTING ENGINE...", bg=PANEL_DARK, fg=TEXT_MUTED)
        threading.Thread(target=self.run_engine_backend, daemon=True).start()

    def inject_keymap(self):
        kcm_content = """
        type FULL
        key W { label: 'W' base: fallback DPAD_UP }
        key A { label: 'A' base: fallback DPAD_LEFT }
        key S { label: 'S' base: fallback DPAD_DOWN }
        key D { label: 'D' base: fallback DPAD_RIGHT }
        key SPACE    { label: 'SPACE'    base: fallback BUTTON_A }
        key C        { label: 'C'        base: fallback BUTTON_B }
        key R        { label: 'R'        base: fallback BUTTON_X }
        key F        { label: 'F'        base: fallback BUTTON_Y }
        key 1        { label: '1'        base: fallback 1 }
        key 2        { label: '2'        base: fallback 2 }
        key 3        { label: '3'        base: fallback 3 }
        """
        kcm_path = os.path.expanduser("~/swag_keys.kcm")
        with open(kcm_path, "w") as f:
            f.write(kcm_content.strip())
            
        subprocess.run(f"adb push {kcm_path} /data/system/devices/keychars/", shell=True, capture_output=True)
        subprocess.run("adb shell dumpsys input", shell=True, capture_output=True)
        if os.path.exists(kcm_path):
            os.remove(kcm_path)

    def apply_anti_cheat_spoof(self):
        spoof_commands = [
            "adb shell setprop ro.product.brand google",
            "adb shell setprop ro.product.manufacturer Google",
            "adb shell setprop ro.product.model 'Pixel 7 Pro'",
            "adb shell setprop ro.product.device cheetah",
            "adb shell setprop ro.build.product cheetah",
            "adb shell setprop ro.build.tags release-keys",
            "adb shell setprop ro.kernel.qemu 0",
            "adb shell setprop ro.hardware redroid_pixel"
        ]
        for cmd in spoof_commands:
            subprocess.run(cmd, shell=True, capture_output=True)

    def run_engine_backend(self):
        try:
            # Parse selected resolution format
            selected_res = self.res_choice.get().split(" ")[0] 
            width, height = selected_res.split("x")

            # 1. Clean old containers
            subprocess.run("docker rm -f swag-player-core", shell=True, capture_output=True)
            
            # 2. Boot Container Core locked down to high-performance 90 FPS
            self.update_status(self.container_status, "STARTING...", "#FFCA28")
            docker_cmd = (
                f"docker run -itd --rm --privileged "
                f"--name=swag-player-core "
                f"-v ~/swag-player-data:/data "
                f"-p 5555:5555 "
                f"redroid/redroid:11.0.0-latest "
                f"androidboot.redroid_width={width} "
                f"androidboot.redroid_height={height} "
                f"androidboot.redroid_fps=90 "
                f"androidboot.redroid_gpu_mode=host"
            )
            subprocess.run(docker_cmd, shell=True, check=True)
            self.update_status(self.container_status, "RUNNING (90 FPS)", "#4CAF50")

            # 3. Initialization window
            time.sleep(15)

            # 4. Connect Bridge and Apply Safeguards
            self.update_status(self.adb_status, "BRIDGING...", "#FFCA28")
            subprocess.run("adb kill-server && adb start-server && adb connect localhost:5555", shell=True, check=True)
            
            self.inject_keymap()
            self.apply_anti_cheat_spoof()

            self.update_status(self.adb_status, "SECURE (CLOAKED)", "#4CAF50")

            # 5. Bring input layout target selections configurations forward
            subprocess.run("adb shell am start -a android.settings.HARD_KEYBOARD_SETTINGS", shell=True)

            # 6. Execute highly fluid mirrored screen layout with live FPS counter print flag active
            scrcpy_cmd = (
                f"scrcpy -s localhost:5555 "
                f"--keyboard=uhid --mouse=uhid "
                f"--shortcut-mod=lctrl "
                f"--print-fps "
                f"--video-bit-rate=8M --max-fps=90 --max-size={width}"
            )
            subprocess.Popen(scrcpy_cmd, shell=True)

        except Exception as e:
            messagebox.showerror("Engine Failure", f"Critical boot breakdown:\n{str(e)}")
        finally:
            self.launch_btn.config(state="normal", text="START KINETIX PLAYER", bg=ACCENT_CYAN, fg=BG_DARK)

if __name__ == "__main__":
    root = tk.Tk()
    app = KinetixPlayerApp(root)
    root.mainloop()
