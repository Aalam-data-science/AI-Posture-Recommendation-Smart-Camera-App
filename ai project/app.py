"""
=============================================================================
         ⚡ HAND CONNECT AI PRO 2.0: HIGH-PERFORMANCE NEURAL HUD ⚡
=============================================================================
Hyper-optimized Hand Tracking Pipeline featuring:
  • Multi-Threaded Video Pipeline for Ultra-High Framerates
  • 5-Fingertip Dual-Hand Quantum Resonance & Energy Arcs
  • Dynamic Neon Glow, Outer Plasma Aura & Laser Connectors
  • Interactive Index Pinch Alert & Touchless Proximity Meter
  • Sleek Cyberpunk Frosted Glassmorphism Telemetry HUD
  • Instant High-Res Snapshot Capture to Screenshots/
=============================================================================
"""

import os
import sys
import cv2
import time
import math
import random
import datetime
import threading
import numpy as np
import urllib.request

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from mediapipe.tasks.python.core import base_options
from mediapipe.tasks.python.vision import hand_landmarker, drawing_utils
from mediapipe.tasks.python.vision.core import image as image_lib
from mediapipe.tasks.python.vision.core import vision_task_running_mode

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# --- CONFIGURATION ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'hand_landmarker.task')
if not os.path.exists(MODEL_PATH):
    print("[*] Downloading Hand Landmarker AI Model...")
    url = 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'
    urllib.request.urlretrieve(url, MODEL_PATH)

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), 'Screenshots')
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# --- THREADED WEBCAM STREAM ---
class ThreadedWebcam:
    def __init__(self, src=0, width=1280, height=720):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.lock = threading.Lock()

    def start(self):
        if self.started:
            return self
        self.started = True
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            if not grabbed:
                continue
            with self.lock:
                self.grabbed = grabbed
                self.frame = frame
            time.sleep(0.003)

    def read(self):
        with self.lock:
            if not self.grabbed or self.frame is None:
                return False, None
            return True, self.frame.copy()

    def release(self):
        self.started = False
        time.sleep(0.05)
        self.cap.release()

# --- AUDIO FEEDBACK ---
AUDIO_ENABLED = True
def play_sound(freq, duration):
    if not AUDIO_ENABLED or not HAS_WINSOUND:
        return
    def _worker():
        try:
            winsound.Beep(freq, duration)
        except Exception:
            pass
    threading.Thread(target=_worker, daemon=True).start()

def draw_glass_rect(img, pt1, pt2, color=(20, 24, 30), alpha=0.72):
    """Draws sleek cyber glassmorphism panel."""
    overlay = img.copy()
    cv2.rectangle(overlay, pt1, pt2, color, -1)
    cv2.addWeighted(overlay, alpha, img, 1.0 - alpha, 0, img)
    cv2.rectangle(img, pt1, pt2, (0, 255, 180), 1)

def draw_neon_line(img, pt1, pt2, color, thickness=2):
    """Draws a glowing sci-fi neon line with inner bright core."""
    cv2.line(img, pt1, pt2, color, thickness + 4, cv2.LINE_AA)
    cv2.line(img, pt1, pt2, (255, 255, 255), thickness, cv2.LINE_AA)

def main():
    global AUDIO_ENABLED

    print("\n" + "="*60)
    print(" ⚡ INITIALIZING HAND CONNECT AI PRO 2.0")
    print("="*60)
    print(" [S] Toggle Sound FX")
    print(" [SPACE] Take Snapshot")
    print(" [ESC] / [Q] Exit")
    print("="*60 + "\n")

    base_options_obj = base_options.BaseOptions(model_asset_path=MODEL_PATH)
    options = hand_landmarker.HandLandmarkerOptions(
        base_options=base_options_obj,
        running_mode=vision_task_running_mode.VisionTaskRunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.7,
        min_hand_presence_confidence=0.7,
        min_tracking_confidence=0.7,
    )
    landmarker = hand_landmarker.HandLandmarker.create_from_options(options)

    cam = ThreadedWebcam(src=0, width=1280, height=720).start()
    time.sleep(0.3)

    window_name = 'HAND CONNECT AI PRO 2.0'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    fingertips = [4, 8, 12, 16, 20]
    neon_colors = [
        (255, 60, 60),   # Neon Blue
        (60, 255, 60),   # Neon Green
        (60, 60, 255),   # Neon Red
        (255, 255, 60),  # Cyan
        (255, 60, 255)   # Magenta
    ]

    smooth_pt1 = [None] * 5
    smooth_pt2 = [None] * 5
    SMOOTHING_FACTOR = 0.28

    pTime = time.time()
    shutter_flash_time = 0
    last_beep_time = 0
    last_ts = -1

    while True:
        success, frame = cam.read()
        if not success or frame is None:
            time.sleep(0.01)
            continue

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        now = time.time()
        fps = 1.0 / max(1e-4, now - pTime)
        pTime = now

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = image_lib.Image(image_format=image_lib.ImageFormat.SRGB, data=rgb_image)
        curr_ms = int(now * 1000)
        ts = max(last_ts + 1, curr_ms)
        last_ts = ts

        results = landmarker.detect_for_video(mp_image, ts)
        display_frame = frame.copy()

        hands_detected = len(results.hand_landmarks) if results.hand_landmarks else 0
        idx_dist = 999.0

        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                drawing_utils.draw_landmarks(
                    display_frame, hand_landmarks, hand_landmarker.HandLandmarksConnections.HAND_CONNECTIONS,
                    drawing_utils.DrawingSpec(color=(0, 255, 200), thickness=2, circle_radius=2),
                    drawing_utils.DrawingSpec(color=(40, 160, 255), thickness=1)
                )

            if hands_detected >= 2:
                h1_landmarks = results.hand_landmarks[0]
                h2_landmarks = results.hand_landmarks[1]

                for i, tip in enumerate(fingertips):
                    curr_pt1 = (int(h1_landmarks[tip].x * w), int(h1_landmarks[tip].y * h))
                    curr_pt2 = (int(h2_landmarks[tip].x * w), int(h2_landmarks[tip].y * h))

                    if smooth_pt1[i] is None: smooth_pt1[i] = curr_pt1
                    if smooth_pt2[i] is None: smooth_pt2[i] = curr_pt2

                    smooth_pt1[i] = (
                        int(smooth_pt1[i][0] * (1 - SMOOTHING_FACTOR) + curr_pt1[0] * SMOOTHING_FACTOR),
                        int(smooth_pt1[i][1] * (1 - SMOOTHING_FACTOR) + curr_pt1[1] * SMOOTHING_FACTOR)
                    )
                    smooth_pt2[i] = (
                        int(smooth_pt2[i][0] * (1 - SMOOTHING_FACTOR) + curr_pt2[0] * SMOOTHING_FACTOR),
                        int(smooth_pt2[i][1] * (1 - SMOOTHING_FACTOR) + curr_pt2[1] * SMOOTHING_FACTOR)
                    )

                    dist = math.hypot(smooth_pt1[i][0] - smooth_pt2[i][0], smooth_pt1[i][1] - smooth_pt2[i][1])
                    if tip == 8:
                        idx_dist = dist

                    color = neon_colors[i]
                    if tip == 8 and dist < 65:
                        # Index Pinch Aura Alert
                        draw_neon_line(display_frame, smooth_pt1[i], smooth_pt2[i], (255, 255, 255), 5)
                        mid = ((smooth_pt1[i][0] + smooth_pt2[i][0]) // 2, (smooth_pt1[i][1] + smooth_pt2[i][1]) // 2)
                        cv2.circle(display_frame, mid, max(2, int(65 - dist)), (0, 255, 255), 2, cv2.LINE_AA)
                        if dist < 35 and now - last_beep_time > 0.4:
                            play_sound(1700, 35)
                            last_beep_time = now
                    else:
                        draw_neon_line(display_frame, smooth_pt1[i], smooth_pt2[i], color, 2)

        # --- ADVANCED HUD OVERLAY ---
        panel_w = 340
        draw_glass_rect(display_frame, (15, 15), (panel_w, h - 20), (15, 18, 22), 0.75)

        cv2.putText(display_frame, "NEURAL CONNECT PRO", (30, 48), cv2.FONT_HERSHEY_TRIPLEX, 0.72, (0, 255, 180), 2)
        cv2.line(display_frame, (30, 60), (panel_w - 20, 60), (0, 255, 180), 1)

        # Hand Status
        status_color = (0, 255, 0) if hands_detected >= 2 else (0, 165, 255)
        status_label = "STABLE / QUANTUM LINKED" if hands_detected >= 2 else "SCANNING ENVIRONMENT"
        cv2.putText(display_frame, f"SYSTEM: {status_label}", (30, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.48, status_color, 1)
        cv2.putText(display_frame, f"HANDS DETECTED: {hands_detected}", (30, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1)

        # Connection Strength Bar
        if hands_detected >= 2:
            strength = float(np.clip(1.0 - (idx_dist / 450.0), 0.0, 1.0))
            bar_w = int(strength * (panel_w - 60))
            cv2.putText(display_frame, f"SYNC STRENGTH: {int(strength * 100)}%", (30, 165), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1)
            cv2.rectangle(display_frame, (30, 175), (panel_w - 30, 190), (45, 50, 55), -1)
            cv2.rectangle(display_frame, (30, 175), (30 + bar_w, 190), (0, 255, 255), -1)
            cv2.putText(display_frame, f"PROXY DISTANCE: {int(idx_dist)} units", (30, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (180, 220, 255), 1)

        # Guide
        cv2.line(display_frame, (30, 245), (panel_w - 20, 245), (50, 70, 80), 1)
        cv2.putText(display_frame, "SYSTEM DIRECTIVES:", (30, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 180), 1)
        cv2.putText(display_frame, "- Bring both hands into frame", (30, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 220, 220), 1)
        cv2.putText(display_frame, "- Touch index fingers for Quantum Lock", (30, 318), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 220, 220), 1)
        cv2.putText(display_frame, "- [SPACE]: High-Res Snapshot", (30, 341), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 220, 220), 1)
        cv2.putText(display_frame, "- [S]: Audio Cues Toggle", (30, 364), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 220, 220), 1)
        cv2.putText(display_frame, "- [ESC] / [Q]: Exit", (30, 387), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 220, 220), 1)

        # Top Right FPS & Status
        stat_w = 180
        draw_glass_rect(display_frame, (w - stat_w - 15, 15), (w - 15, 75), (20, 25, 30), 0.8)
        cv2.putText(display_frame, f"FPS: {int(fps)}", (w - stat_w, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, f"SOUND: {'ON' if AUDIO_ENABLED else 'OFF'}", (w - stat_w, 64), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)

        # Shutter Flash
        if now - shutter_flash_time < 0.2:
            flash_alpha = max(0.0, 1.0 - (now - shutter_flash_time) / 0.2)
            white_overlay = np.full_like(display_frame, 255)
            cv2.addWeighted(white_overlay, flash_alpha * 0.75, display_frame, 1.0 - flash_alpha * 0.75, 0, display_frame)

        cv2.imshow(window_name, display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key in [27, ord('q'), ord('Q')]:
            break
        elif key in [ord('s'), ord('S')]:
            AUDIO_ENABLED = not AUDIO_ENABLED
            play_sound(1200, 40)
        elif key == 32: # SPACE: Shutter Screenshot
            timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            snap_path = os.path.join(SCREENSHOTS_DIR, f"hand_connect_{timestamp_str}.png")
            cv2.imwrite(snap_path, display_frame)
            play_sound(2100, 50)
            shutter_flash_time = now
            print(f"📸 Saved snapshot to: {snap_path}")

    cam.release()
    cv2.destroyAllWindows()
    print("✨ Hand Connect AI Pro 2.0 Concluded Successfully.")

if __name__ == "__main__":
    main()