"""
=============================================================================
         🌌 NEURAL CONNECT PRO 2.0: HOLOGRAPHIC BIOMETRICS & SYNC OS 🌌
=============================================================================
Next-Generation Computer Vision Suite featuring:
  • Multi-Threaded Low-Latency Vision Architecture
  • Dual-Hand Quantum Energy Arcs & Electric Plasma Discharge Engine
  • 3D Spatial Proximity & Quantum Resonance Calculation
  • 52-Blendshape Biometric Facial Affective Engine (Emotion & Mood Matrix)
  • Ergonomic Eye-Strain & Posture Health Guardian
  • Glassmorphic Cyberpunk Jarvis HUD with Animated Telemetry & Starfield Particles
  • Instant Timestamped Shutter Snapshots to Screenshots/
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
from mediapipe.tasks.python.vision import hand_landmarker, face_landmarker, drawing_utils
from mediapipe.tasks.python.vision.core import image as image_lib
from mediapipe.tasks.python.vision.core import vision_task_running_mode

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# --- ASSETS SETUP ---
HAND_MODEL = os.path.join(os.path.dirname(__file__), 'hand_landmarker.task')
FACE_MODEL = os.path.join(os.path.dirname(__file__), 'face_landmarker.task')
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), 'Screenshots')
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def ensure_model(url, path):
    if not os.path.exists(path):
        print(f"[*] Downloading {os.path.basename(path)}...")
        urllib.request.urlretrieve(url, path)

ensure_model('https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task', HAND_MODEL)
ensure_model('https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task', FACE_MODEL)

# --- THREADED CAMERA PIPELINE ---
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

# --- AUDIO CUES ---
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

# --- PLASMA SPARK PARTICLES ---
class PlasmaParticle:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2.0, 7.0)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.life = 1.0
        self.decay = random.uniform(0.04, 0.08)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay
        return self.life > 0

    def draw(self, img):
        if self.life > 0:
            radius = max(1, int(self.life * 4))
            alpha = self.life
            cv2.circle(img, (int(self.x), int(self.y)), radius, self.color, -1, cv2.LINE_AA)

# --- DRAWING UTILITIES ---
def draw_glass_panel(img, pt1, pt2, color=(15, 18, 22), alpha=0.75, border_color=(0, 255, 180)):
    """Draws sleek cyber glassmorphism panel."""
    overlay = img.copy()
    cv2.rectangle(overlay, pt1, pt2, color, -1)
    cv2.addWeighted(overlay, alpha, img, 1.0 - alpha, 0, img)
    cv2.rectangle(img, pt1, pt2, border_color, 1)

def draw_lightning_arc(img, p1, p2, color, segments=7, jitter=12):
    """Draws an electric lightning energy arc between two points."""
    x1, y1 = p1
    x2, y2 = p2
    pts = [p1]
    dx = (x2 - x1) / segments
    dy = (y2 - y1) / segments
    for i in range(1, segments):
        jx = random.randint(-jitter, jitter)
        jy = random.randint(-jitter, jitter)
        pts.append((int(x1 + i * dx + jx), int(y1 + i * dy + jy)))
    pts.append(p2)

    for i in range(len(pts) - 1):
        # Outer glow
        cv2.line(img, pts[i], pts[i + 1], color, 4, cv2.LINE_AA)
        # Inner white core
        cv2.line(img, pts[i], pts[i + 1], (255, 255, 255), 1, cv2.LINE_AA)

# =============================================================================
#  MAIN EXECUTION PIPELINE
# =============================================================================
def main():
    global AUDIO_ENABLED

    print("\n" + "="*65)
    print(" 🌌 INITIALIZING NEURAL CONNECT PRO 2.0 (HOLOGRAPHIC BIOMETRICS)")
    print("="*65)
    print(" [S] Toggle Audio Feedback")
    print(" [SPACE] Take Shutter Snapshot")
    print(" [ESC] / [Q] Exit")
    print("="*65 + "\n")

    # 1. Initialize Detectors
    base_hand_opts = base_options.BaseOptions(model_asset_path=HAND_MODEL)
    hand_detector = hand_landmarker.HandLandmarker.create_from_options(
        hand_landmarker.HandLandmarkerOptions(
            base_options=base_hand_opts,
            running_mode=vision_task_running_mode.VisionTaskRunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7,
        )
    )

    base_face_opts = base_options.BaseOptions(model_asset_path=FACE_MODEL)
    face_detector = face_landmarker.FaceLandmarker.create_from_options(
        face_landmarker.FaceLandmarkerOptions(
            base_options=base_face_opts,
            running_mode=vision_task_running_mode.VisionTaskRunningMode.VIDEO,
            output_face_blendshapes=True,
            num_faces=1
        )
    )

    cam = ThreadedWebcam(src=0, width=1280, height=720).start()
    time.sleep(0.3)

    window_name = "NEURAL CONNECT PRO 2.0 - BIOMETRIC MATRIX"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # Fingertips & Palette
    fingertips = [4, 8, 12, 16, 20] # Thumb, Index, Middle, Ring, Pinky
    finger_names = ["THUMB", "INDEX", "MIDDLE", "RING", "PINKY"]
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

    particles = []
    shutter_flash_time = 0
    pTime = time.time()
    last_sync_beep = 0

    # Face Telemetry Storage
    face_state = {
        "mood": "NEUTRAL",
        "jaw_open": 0.0,
        "blink_l": False,
        "blink_r": False,
        "posture": "OPTIMAL",
        "blink_count": 0,
        "last_blink_time": time.time()
    }
    was_blinking = False

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

        # Vision Pipeline Inference
        hand_res = hand_detector.detect_for_video(mp_image, ts)
        face_res = face_detector.detect_for_video(mp_image, ts)

        display_frame = frame.copy()

        # ---------------------------------------------------------------------
        # 1. BIOMETRIC FACE TELEMETRY & TESSELLATION
        # ---------------------------------------------------------------------
        if face_res.face_landmarks:
            flm = face_res.face_landmarks[0]
            # Draw Holographic Subtle Facial Wireframe
            drawing_utils.draw_landmarks(
                display_frame, flm, face_landmarker.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION,
                None, drawing_utils.DrawingSpec(color=(0, 220, 100), thickness=1, circle_radius=0)
            )

            # Posture check
            face_h = abs(flm[152].y - flm[10].y)
            if face_h > 0.45:
                face_state["posture"] = "TOO CLOSE"
            elif face_h < 0.17:
                face_state["posture"] = "TOO FAR / SLOUCH"
            else:
                face_state["posture"] = "OPTIMAL"

            if face_res.face_blendshapes:
                s = {b.category_name: b.score for b in face_res.face_blendshapes[0]}
                face_state["jaw_open"] = s.get('jawOpen', 0.0)
                is_l_blink = s.get('eyeBlinkLeft', 0.0) > 0.45
                is_r_blink = s.get('eyeBlinkRight', 0.0) > 0.45
                face_state["blink_l"] = is_l_blink
                face_state["blink_r"] = is_r_blink

                if (is_l_blink or is_r_blink) and not was_blinking:
                    face_state["blink_count"] += 1
                    was_blinking = True
                elif not (is_l_blink or is_r_blink):
                    was_blinking = False

                if s.get('mouthSmileLeft', 0.0) > 0.35 or s.get('mouthSmileRight', 0.0) > 0.35:
                    face_state["mood"] = "HAPPY :D"
                elif s.get('eyeWideLeft', 0.0) > 0.35 or s.get('eyeWideRight', 0.0) > 0.35:
                    face_state["mood"] = "SURPRISED!"
                elif s.get('browDownLeft', 0.0) > 0.35 or s.get('browDownRight', 0.0) > 0.35:
                    face_state["mood"] = "FOCUSED / INTENSE"
                elif s.get('jawOpen', 0.0) > 0.35:
                    face_state["mood"] = "VOCAL / SPEAKING"
                else:
                    face_state["mood"] = "NEUTRAL"

        # ---------------------------------------------------------------------
        # 2. DUAL-HAND QUANTUM SYNC & LIGHTNING ARCS
        # ---------------------------------------------------------------------
        hands_detected = len(hand_res.hand_landmarks) if hand_res.hand_landmarks else 0
        sync_strength = 0.0
        index_dist = 999.0

        if hand_res.hand_landmarks:
            for hand_lms in hand_res.hand_landmarks:
                drawing_utils.draw_landmarks(
                    display_frame, hand_lms, hand_landmarker.HandLandmarksConnections.HAND_CONNECTIONS,
                    drawing_utils.DrawingSpec(color=(0, 255, 200), thickness=2, circle_radius=2),
                    drawing_utils.DrawingSpec(color=(40, 160, 255), thickness=1)
                )

            if hands_detected >= 2:
                h1_lms = hand_res.hand_landmarks[0]
                h2_lms = hand_res.hand_landmarks[1]

                for i, tip in enumerate(fingertips):
                    c1 = (int(h1_lms[tip].x * w), int(h1_lms[tip].y * h))
                    c2 = (int(h2_lms[tip].x * w), int(h2_lms[tip].y * h))

                    # 1-Euro style exponential smoothing
                    if smooth_pt1[i] is None: smooth_pt1[i] = c1
                    if smooth_pt2[i] is None: smooth_pt2[i] = c2

                    smooth_pt1[i] = (
                        int(smooth_pt1[i][0] * (1 - SMOOTHING_FACTOR) + c1[0] * SMOOTHING_FACTOR),
                        int(smooth_pt1[i][1] * (1 - SMOOTHING_FACTOR) + c1[1] * SMOOTHING_FACTOR)
                    )
                    smooth_pt2[i] = (
                        int(smooth_pt2[i][0] * (1 - SMOOTHING_FACTOR) + c2[0] * SMOOTHING_FACTOR),
                        int(smooth_pt2[i][1] * (1 - SMOOTHING_FACTOR) + c2[1] * SMOOTHING_FACTOR)
                    )

                    p1 = smooth_pt1[i]
                    p2 = smooth_pt2[i]
                    dist = math.hypot(p1[0] - p2[0], p1[1] - p2[1])

                    if tip == 8: # Index Finger Distance
                        index_dist = dist
                        sync_strength = float(np.clip(1.0 - (dist / 450.0), 0.0, 1.0))

                    col = neon_colors[i]

                    # If close, emit lightning energy arcs & plasma particles
                    if dist < 85:
                        draw_lightning_arc(display_frame, p1, p2, (0, 255, 255), segments=6, jitter=10)
                        mid = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
                        cv2.circle(display_frame, mid, max(2, int(85 - dist)), (255, 255, 255), 2, cv2.LINE_AA)

                        # Emit plasma explosion particles
                        for _ in range(3):
                            particles.append(PlasmaParticle(mid[0], mid[1], col))

                        if tip == 8 and dist < 40 and now - last_sync_beep > 0.4:
                            play_sound(1600, 40)
                            last_sync_beep = now
                    else:
                        # Smooth glowing cyber connection
                        cv2.line(display_frame, p1, p2, col, 2, cv2.LINE_AA)
                        cv2.circle(display_frame, p1, 5, col, -1)
                        cv2.circle(display_frame, p2, 5, col, -1)

        # Update & Render Plasma Particles
        particles = [p for p in particles if p.update()]
        for p in particles:
            p.draw(display_frame)

        # ---------------------------------------------------------------------
        # 3. JARVIS GLASSMORPHIC CYBER HUD
        # ---------------------------------------------------------------------
        # Left Telemetry Panel
        panel_w = 340
        draw_glass_panel(display_frame, (15, 15), (panel_w, h - 20), (15, 18, 22), 0.75, (0, 255, 180))

        cv2.putText(display_frame, "NEURAL CONNECT 2.0", (30, 48), cv2.FONT_HERSHEY_TRIPLEX, 0.72, (0, 255, 180), 2)
        cv2.line(display_frame, (30, 60), (panel_w - 20, 60), (0, 255, 180), 1)

        # System Sync Status
        sys_status = "QUANTUM SYNCED" if hands_detected == 2 else "SCANNING FIELD"
        sys_col = (0, 255, 0) if hands_detected == 2 else (0, 165, 255)
        cv2.putText(display_frame, f"STATUS: {sys_status}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.58, sys_col, 2)
        cv2.putText(display_frame, f"HANDS TRACKED: {hands_detected}", (30, 118), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1)

        # Sync Resonance Bar
        sync_pct = int(sync_strength * 100)
        cv2.putText(display_frame, f"RESONANCE: {sync_pct}%", (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (200, 255, 255), 1)
        cv2.rectangle(display_frame, (30, 160), (panel_w - 30, 175), (40, 45, 50), -1)
        cv2.rectangle(display_frame, (30, 160), (30 + int((panel_w - 60) * sync_strength), 175), (0, 255, 255), -1)
        cv2.putText(display_frame, f"INDEX PROXIMITY: {int(index_dist)} px", (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (180, 220, 255), 1)

        # Biometric Affective Telemetry
        cv2.line(display_frame, (30, 220), (panel_w - 20, 220), (50, 70, 80), 1)
        cv2.putText(display_frame, "FACIAL BIOMETRICS MATRIX", (30, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        cv2.putText(display_frame, f"MOOD: {face_state['mood']}", (30, 268), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 2)

        # Posture Status
        post_col = (0, 255, 0) if face_state["posture"] == "OPTIMAL" else (0, 120, 255)
        cv2.putText(display_frame, f"POSTURE: {face_state['posture']}", (30, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.5, post_col, 1)

        # Blink Telemetry
        blink_txt = "EYES: " + ("BLINK-L " if face_state["blink_l"] else "OPEN-L ") + ("BLINK-R" if face_state["blink_r"] else "OPEN-R")
        cv2.putText(display_frame, blink_txt, (30, 322), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (200, 200, 200), 1)

        # Vocal Spectrum Bar
        vocal_pct = int(face_state["jaw_open"] * 100)
        cv2.putText(display_frame, f"VOCAL ACTIVITY: {vocal_pct}%", (30, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (180, 180, 180), 1)
        cv2.rectangle(display_frame, (30, 360), (panel_w - 30, 372), (40, 45, 50), -1)
        cv2.rectangle(display_frame, (30, 360), (30 + int((panel_w - 60) * face_state["jaw_open"]), 372), (0, 255, 120), -1)

        # Live Controls Info
        cv2.line(display_frame, (30, 395), (panel_w - 20, 395), (50, 70, 80), 1)
        cv2.putText(display_frame, "CONTROLS & SHORTCUTS:", (30, 415), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 180), 1)
        cv2.putText(display_frame, "- Touch Index Fingers: Plasma Discharge", (30, 438), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 220, 220), 1)
        cv2.putText(display_frame, "- [SPACE]: High-Res Screenshot", (30, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 220, 220), 1)
        cv2.putText(display_frame, "- [S]: Audio Cues Toggle", (30, 482), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 220, 220), 1)
        cv2.putText(display_frame, "- [ESC] / [Q]: Exit", (30, 504), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 220, 220), 1)

        # Engine Stats (Top Right)
        stat_w = 190
        draw_glass_panel(display_frame, (w - stat_w - 15, 15), (w - 15, 75), (20, 25, 30), 0.8, (0, 255, 0))
        cv2.putText(display_frame, f"FPS: {int(fps)}", (w - stat_w, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, f"AUDIO: {'ON' if AUDIO_ENABLED else 'OFF'}", (w - stat_w, 64), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)

        # Shutter Flash Animation
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
            snap_path = os.path.join(SCREENSHOTS_DIR, f"neural_connect_{timestamp_str}.png")
            cv2.imwrite(snap_path, display_frame)
            play_sound(2200, 60)
            shutter_flash_time = now
            print(f"📸 Saved snapshot to: {snap_path}")

    cam.release()
    cv2.destroyAllWindows()
    print("✨ Neural Connect Pro 2.0 Concluded Successfully.")

if __name__ == "__main__":
    main()