"""
=============================================================================
         🛸 NEURAL SPATIAL SUITE: CENTRAL CONTROL LAUNCHER 🛸
=============================================================================
Single unified command center for launching and benchmarking all AI modules.
"""

import os
import sys
import time
import subprocess
import webbrowser

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def print_banner():
    banner = r"""
  =======================================================================
     _   _  ______  _   _  _____         _      __  __           _____ 
    | \ | ||  ____|| | | ||  __ \  /\   | |    |  \/  |   /\    / ____|
    |  \| || |__   | | | || |__) |/  \  | |    | \  / |  /  \  | (___  
    | . ` ||  __|  | | | ||  _  // /\ \ | |    | |\/| | / /\ \  \___ \ 
    | |\  || |____ | |_| || | \ \  __  \| |____| |  | |/ ____ \ ____) |
    |_| \_||______| \___/ |_|  \_\/  \_\____/|_|_|  |_/_/    \_\_____/ 
                           NEURAL SPATIAL SUITE 2.0
  =======================================================================
    [1]  >>  Neural Master X (Virtual AI Mouse & Air Canvas OS)
    [2]  >>  Neural Connect Pro 2.0 (Dual-Hand Quantum Sync & Biometrics)
    [3]  >>  Hand Connect AI Pro (Dual-Hand Neon HUD)
    [4]  >>  NeuralTouch Spatial Web Playground (In Browser)
    [5]  >>  Run Vision Pipeline & Camera Diagnostic Test
    [0]  >>  Exit
  =======================================================================
    """
    print(banner)

def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    python_exe = sys.executable
    print(f"\n[*] Launching [{script_name}] via {python_exe}...\n")
    try:
        subprocess.run([python_exe, script_path])
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"\n[!] Error launching {script_name}: {e}")

def run_web():
    html_path = os.path.join(os.path.dirname(__file__), 'hallo.html')
    print(f"\n[*] Opening NeuralTouch Web Interface: {html_path}\n")
    webbrowser.open(f"file:///{os.path.abspath(html_path)}")

def run_diagnostics():
    print("\n" + "="*50)
    print("[*] RUNNING SYSTEM & CAMERA DIAGNOSTICS...")
    print("="*50)
    import cv2
    import pyautogui

    print(f"[+] Desktop Resolution: {pyautogui.size()}")
    print("[*] Probing Webcam Index 0...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[-] Camera 0 could not be opened!")
        return

    fps_count = 0
    start_t = time.time()
    for _ in range(30):
        ret, frame = cap.read()
        if ret: fps_count += 1
    total_t = time.time() - start_t
    cap.release()

    tested_fps = int(fps_count / max(1e-3, total_t))
    print(f"[+] Camera online! Native capture speed: ~{tested_fps} FPS (Sample shape: {frame.shape})")
    print("[+] MediaPipe models present:")
    for model in ['hand_landmarker.task', 'face_landmarker.task']:
        p = os.path.join(os.path.dirname(__file__), model)
        size_mb = os.path.getsize(p) / (1024 * 1024) if os.path.exists(p) else 0
        print(f"   * {model}: {'FOUND (' + str(round(size_mb, 2)) + ' MB)' if os.path.exists(p) else 'MISSING'}")
    print("="*50 + "\n")

def main():
    while True:
        print_banner()
        choice = input("Enter choice [0-5]: ").strip()
        if choice == '1':
            run_script('mouse.py')
        elif choice == '2':
            run_script('app2.py')
        elif choice == '3':
            run_script('app.py')
        elif choice == '4':
            run_web()
        elif choice == '5':
            run_diagnostics()
        elif choice in ['0', 'exit', 'quit', 'q']:
            print("\nFarewell! System offline.\n")
            break
        else:
            print("[!] Invalid choice. Please enter 0 to 5.")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
