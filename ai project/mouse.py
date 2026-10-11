"""
=============================================================================
           🚀 NEURAL MASTER X: AI SPATIAL VIRTUAL MOUSE & VISION OS 🚀
=============================================================================
Advanced AI-Powered Vision Interface combining:
  • Ultra-Smooth 1-Euro Adaptive Filter (Zero-Jitter, Zero-Lag Mouse Engine)
  • Multi-Threaded Low-Latency Camera Pipeline
  • Comprehensive Touchless Gesture Suite (Click, Drag, Double Click, Right Click,
    2-Finger Inertial Scroll, Volume Dial, Air Canvas Drawing, Screen Shutter)
  • Holographic Jarvis/Cyberpunk HUD with Animated Targeting Reticles & Shockwaves
  • Face & Emotion Biometrics (Mood, Blink Assist, Ergonomic Posture Guard)
  • Non-Blocking Sci-Fi Audio Synthesizer (Haptic Feedback)
=============================================================================
"""

import os
import sys
import cv2
import time
import math
import queue
import datetime
import threading
import numpy as np
import urllib.request
import pyautogui

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

# Optional sound feedback via Windows winsound
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# --- PERFORMANCE TUNING ---
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
try:
    SCREEN_W, SCREEN_H = pyautogui.size()
except Exception:
    SCREEN_W, SCREEN_H = 1920, 1080

# --- MODELS AUTO-DOWNLOAD ---
HAND_MODEL = os.path.join(os.path.dirname(__file__), 'hand_landmarker.task')
FACE_MODEL = os.path.join(os.path.dirname(__file__), 'face_landmarker.task')

def ensure_model(url, path):
    if not os.path.exists(path):
        print(f"[*] Downloading {os.path.basename(path)}...")
        urllib.request.urlretrieve(url, path)

ensure_model('https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task', HAND_MODEL)
ensure_model('https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task', FACE_MODEL)

# Ensure Screenshots Directory Exists
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), 'Screenshots')
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


# =============================================================================
#  1-EURO ADAPTIVE FILTER (Precision Anti-Jitter & Instant Velocity Tracking)
# =============================================================================
class OneEuroFilter:
    """
    Gold-standard 1€ Filter used in high-end AR/VR spatial tracking.
    Eliminates micro-tremors when holding still, zero lag during rapid swipes.
    """
    def __init__(self, t0, x0, dx0=0.0, min_cutoff=0.8, beta=0.015, d_cutoff=1.0):
        self.min_cutoff = float(min_cutoff)
        self.beta = float(beta)
        self.d_cutoff = float(d_cutoff)
        self.x_prev = float(x0)
        self.dx_prev = float(dx0)
        self.t_prev = float(t0)

    def alpha(self, cutoff, dt):
        tau = 1.0 / (2.0 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / dt)

    def filter(self, t, x):
        dt = max(1e-5, t - self.t_prev)
        dx = (x - self.x_prev) / dt
        a_d = self.alpha(self.d_cutoff, dt)
        dx_hat = a_d * dx + (1.0 - a_d) * self.dx_prev

        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = self.alpha(cutoff, dt)
        x_hat = a * x + (1.0 - a) * self.x_prev

        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t_prev = t
        return x_hat


# =============================================================================
#  THREADED WEBCAM PIPELINE (Decouples Camera I/O from Vision Processing)
# =============================================================================
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


# =============================================================================
#  AUDIO SYNTHESIZER (Non-Blocking Sci-Fi Haptic Sound FX)
# =============================================================================
AUDIO_ENABLED = True

def play_sound(effect_name):
    """Triggers non-blocking audio cues for tactile confirmation."""
    if not AUDIO_ENABLED or not HAS_WINSOUND:
        return

    def _worker():
        try:
            if effect_name == "click":
                winsound.Beep(1250, 35)
            elif effect_name == "drag":
                winsound.Beep(950, 60)
            elif effect_name == "right_click":
                winsound.Beep(750, 45)
            elif effect_name == "double_click":
                winsound.Beep(1400, 25)
                winsound.Beep(1700, 35)
            elif effect_name == "scroll":
                winsound.Beep(650, 15)
            elif effect_name == "snapshot":
                winsound.Beep(2100, 40)
                winsound.Beep(2600, 70)
            elif effect_name == "mode_switch":
                winsound.Beep(850, 35)
                winsound.Beep(1150, 45)
        except Exception:
            pass

    threading.Thread(target=_worker, daemon=True).start()


# =============================================================================
#  SHOCKWAVE RIPPLE & PARTICLE ENGINE
# =============================================================================
class VisualRipple:
    def __init__(self, x, y, color=(0, 255, 255), max_radius=45, duration=0.35):
        self.x = int(x)
        self.y = int(y)
        self.color = color
        self.max_radius = max_radius
        self.start_time = time.time()
        self.duration = duration

    def draw(self, img):
        elapsed = time.time() - self.start_time
        if elapsed > self.duration:
            return False
        progress = elapsed / self.duration
        radius = int(progress * self.max_radius)
        alpha = max(0.0, 1.0 - progress)
        thickness = max(1, int(3 * (1 - progress)))

        # Create overlay for transparent ripple
        overlay = img.copy()
        cv2.circle(overlay, (self.x, self.y), radius, self.color, thickness, cv2.LINE_AA)
        cv2.circle(overlay, (self.x, self.y), max(1, radius // 2), (255, 255, 255), 1, cv2.LINE_AA)
        cv2.addWeighted(overlay, alpha, img, 1.0 - alpha, 0, img)
        return True


# =============================================================================
#  MAIN AI SPATIAL CONTROLLER
# =============================================================================
def main():
    global AUDIO_ENABLED

    print("\n" + "="*60)
    print(" 🚀 INITIALIZING NEURAL MASTER X (AI SPATIAL OS)")
    print("="*60)
    print(" [M] Toggle Mode (Mouse <-> Air Canvas)")
    print(" [S] Toggle Audio Feedback")
    print(" [C] Clear Air Canvas")
    print(" [SPACE] Take Shutter Snapshot")
    print(" [ESC] / [Q] Exit")
    print("="*60 + "\n")

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

    # 2. Camera Setup
    cam = ThreadedWebcam(src=0, width=1280, height=720).start()
    time.sleep(0.3)

    window_name = "NEURAL MASTER X - AI SPATIAL OS"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # 3. Filters & State Variables
    filter_x = None
    filter_y = None
    last_raw_x, last_raw_y = 0, 0
    smooth_x, smooth_y = SCREEN_W // 2, SCREEN_H // 2

    # Gesture Thresholds & Timers
    PINCH_TRIGGER_DIST = 32
    PINCH_RELEASE_DIST = 46

    is_left_down = False
    is_right_down = False
    pinch_start_time = 0
    last_click_time = 0
    last_scroll_time = 0
    prev_scroll_y = None

    # Visual FX
    ripples = []
    trail_points = []
    shutter_flash_time = 0

    # Air Canvas
    current_mode = "MOUSE" # "MOUSE" or "CANVAS"
    canvas_mask = None
    canvas_colors = [
        (255, 255, 0),   # Cyan
        (0, 255, 128),   # Neon Emerald
        (255, 0, 255),   # Magenta
        (0, 200, 255),   # Amber Gold
        (0, 0, 255)      # Laser Red
    ]
    current_color_idx = 0
    brush_thickness = 6

    # Face Telemetry Cache
    face_telemetry = {
        "mood": "NEUTRAL",
        "jaw_open": 0.0,
        "blink_l": False,
        "blink_r": False,
        "posture": "OPTIMAL",
        "face_box": None
    }
    face_check_frame_counter = 0

    # Reticle Rotation Angle
    reticle_angle = 0
    pTime = time.time()

    # Dynamic Control Box (Inner margin for comfortable hand reach)
    BOX_MARGIN_X = 220
    BOX_MARGIN_Y = 120

    last_hand_ts = -1
    last_face_ts = -1

    while True:
        success, frame = cam.read()
        if not success or frame is None:
            time.sleep(0.01)
            continue

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        if canvas_mask is None or canvas_mask.shape[:2] != (h, w):
            canvas_mask = np.zeros((h, w, 3), dtype=np.uint8)

        now = time.time()
        fps = 1.0 / max(1e-4, now - pTime)
        pTime = now

        reticle_angle = (reticle_angle + 6) % 360

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = image_lib.Image(image_format=image_lib.ImageFormat.SRGB, data=rgb_image)
        curr_ms = int(now * 1000)

        # Monotonically increasing timestamps for MediaPipe Video mode
        ts = max(last_hand_ts + 1, curr_ms)
        last_hand_ts = ts

        # Run Hand Detection (Every Frame)
        hand_res = hand_detector.detect_for_video(mp_image, ts)

        # Run Face Detection (Every 2nd Frame for Peak Performance)
        face_check_frame_counter += 1
        if face_check_frame_counter % 2 == 0:
            face_ts = max(last_face_ts + 1, curr_ms)
            last_face_ts = face_ts
            face_res = face_detector.detect_for_video(mp_image, face_ts)
            if face_res.face_landmarks:
                flm = face_res.face_landmarks[0]
                # Posture check from face height
                top_y = flm[10].y
                bot_y = flm[152].y
                face_height = abs(bot_y - top_y)
                if face_height > 0.45:
                    face_telemetry["posture"] = "TOO CLOSE"
                elif face_height < 0.18:
                    face_telemetry["posture"] = "TOO FAR / SLOUCH"
                else:
                    face_telemetry["posture"] = "OPTIMAL"

                # Expression Blendshapes
                if face_res.face_blendshapes:
                    s = {b.category_name: b.score for b in face_res.face_blendshapes[0]}
                    face_telemetry["jaw_open"] = s.get('jawOpen', 0.0)
                    face_telemetry["blink_l"] = s.get('eyeBlinkLeft', 0.0) > 0.45
                    face_telemetry["blink_r"] = s.get('eyeBlinkRight', 0.0) > 0.45

                    if s.get('mouthSmileLeft', 0.0) > 0.35 or s.get('mouthSmileRight', 0.0) > 0.35:
                        face_telemetry["mood"] = "HAPPY :D"
                    elif s.get('eyeWideLeft', 0.0) > 0.35 or s.get('eyeWideRight', 0.0) > 0.35:
                        face_telemetry["mood"] = "SURPRISED!"
                    elif s.get('browDownLeft', 0.0) > 0.35 or s.get('browDownRight', 0.0) > 0.35:
                        face_telemetry["mood"] = "FOCUSED"
                    elif s.get('jawOpen', 0.0) > 0.35:
                        face_telemetry["mood"] = "TALKING"
                    else:
                        face_telemetry["mood"] = "NEUTRAL"

        display_frame = frame.copy()

        # Visual Control Bounding Box
        box_x1, box_y1 = BOX_MARGIN_X, BOX_MARGIN_Y
        box_x2, box_y2 = w - BOX_MARGIN_X, h - BOX_MARGIN_Y

        # Draw Futuristic Cyber Brackets on Bounds
        b_col = (0, 255, 255) if current_mode == "MOUSE" else (255, 0, 255)
        # Top-Left
        cv2.line(display_frame, (box_x1, box_y1), (box_x1 + 35, box_y1), b_col, 2)
        cv2.line(display_frame, (box_x1, box_y1), (box_x1, box_y1 + 35), b_col, 2)
        # Top-Right
        cv2.line(display_frame, (box_x2, box_y1), (box_x2 - 35, box_y1), b_col, 2)
        cv2.line(display_frame, (box_x2, box_y1), (box_x2, box_y1 + 35), b_col, 2)
        # Bottom-Left
        cv2.line(display_frame, (box_x1, box_y2), (box_x1 + 35, box_y2), b_col, 2)
        cv2.line(display_frame, (box_x1, box_y2), (box_x1, box_y2 - 35), b_col, 2)
        # Bottom-Right
        cv2.line(display_frame, (box_x2, box_y2), (box_x2 - 35, box_y2), b_col, 2)
        cv2.line(display_frame, (box_x2, box_y2), (box_x2, box_y2 - 35), b_col, 2)

        gesture_status = "IDLE"
        active_cursor_pos = None

        if hand_res.hand_landmarks:
            control_hand = hand_res.hand_landmarks[0]

            # Landmark coordinates in pixels
            pts = {}
            for i in [4, 8, 12, 16, 20]: # Thumb, Index, Middle, Ring, Pinky
                pts[i] = (int(control_hand[i].x * w), int(control_hand[i].y * h))

            # Finger extension checks (Tip Y < PIP Y)
            is_index_up = control_hand[8].y < control_hand[6].y
            is_middle_up = control_hand[12].y < control_hand[10].y
            is_ring_up = control_hand[16].y < control_hand[14].y
            is_pinky_up = control_hand[20].y < control_hand[18].y

            ix, iy = pts[8]
            tx, ty = pts[4]
            mx, my = pts[12]
            rx, ry = pts[16]
            px, py = pts[20]

            # Draw Hand Mesh with Sci-Fi Neon Connections
            drawing_utils.draw_landmarks(
                display_frame, control_hand, hand_landmarker.HandLandmarksConnections.HAND_CONNECTIONS,
                drawing_utils.DrawingSpec(color=(0, 255, 180), thickness=2, circle_radius=2),
                drawing_utils.DrawingSpec(color=(50, 150, 255), thickness=1)
            )

            # Distances for Gestures
            dist_thumb_index = math.hypot(ix - tx, iy - ty)
            dist_thumb_middle = math.hypot(mx - tx, my - ty)
            dist_thumb_ring = math.hypot(rx - tx, ry - ty)
            dist_thumb_pinky = math.hypot(px - tx, py - ty)

            active_cursor_pos = (ix, iy)

            # -----------------------------------------------------------------
            # 1. MOUSE CURSOR POSITION WITH 1-EURO ADAPTIVE FILTERING
            # -----------------------------------------------------------------
            # Map camera box coordinate to full desktop resolution
            norm_x = np.interp(ix, (box_x1, box_x2), (0, SCREEN_W))
            norm_y = np.interp(iy, (box_y1, box_y2), (0, SCREEN_H))

            # Non-linear dynamic acceleration:
            norm_x = np.clip(norm_x, 0, SCREEN_W)
            norm_y = np.clip(norm_y, 0, SCREEN_H)

            if filter_x is None:
                filter_x = OneEuroFilter(now, norm_x, min_cutoff=0.8, beta=0.015)
                filter_y = OneEuroFilter(now, norm_y, min_cutoff=0.8, beta=0.015)
                smooth_x = norm_x
                smooth_y = norm_y
            else:
                smooth_x = filter_x.filter(now, norm_x)
                smooth_y = filter_y.filter(now, norm_y)

            # Add to motion trail
            trail_points.append((ix, iy))
            if len(trail_points) > 12:
                trail_points.pop(0)

            # -----------------------------------------------------------------
            # 2. GESTURE DISPATCHER
            # -----------------------------------------------------------------
            if current_mode == "MOUSE":
                # A. SCROLL GESTURE: Peace Sign (Index + Middle UP, Ring & Pinky DOWN)
                if is_index_up and is_middle_up and not is_ring_up and not is_pinky_up and dist_thumb_index > 50:
                    gesture_status = "TWO-FINGER SCROLL"
                    mid_y = (iy + my) / 2.0
                    if prev_scroll_y is not None:
                        dy = mid_y - prev_scroll_y
                        if abs(dy) > 3:
                            scroll_amount = int(-dy * 3.5)
                            try:
                                pyautogui.scroll(scroll_amount)
                            except Exception:
                                pass
                            play_sound("scroll")
                    prev_scroll_y = mid_y
                    # Visual Scroll Indicator
                    cv2.line(display_frame, (ix, iy), (mx, my), (255, 255, 0), 3, cv2.LINE_AA)
                    cv2.putText(display_frame, "SCROLLING", ((ix+mx)//2, (iy+my)//2 - 15), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

                else:
                    prev_scroll_y = None

                    # B. VOLUME DIAL GESTURE: Thumb + Pinky Pinch
                    if dist_thumb_pinky < PINCH_TRIGGER_DIST:
                        gesture_status = "VOLUME DIAL"
                        cv2.line(display_frame, (tx, ty), (px, py), (0, 165, 255), 3, cv2.LINE_AA)
                        # Upwards moves volume up, downwards moves volume down
                        if now - last_scroll_time > 0.12:
                            try:
                                if py < ty:
                                    pyautogui.press('volumeup')
                                else:
                                    pyautogui.press('volumedown')
                            except Exception:
                                pass
                            last_scroll_time = now

                    # C. DOUBLE CLICK GESTURE: Thumb + Ring Pinch
                    elif dist_thumb_ring < PINCH_TRIGGER_DIST:
                        if now - last_click_time > 0.4:
                            try:
                                pyautogui.doubleClick()
                            except Exception:
                                pass
                            play_sound("double_click")
                            ripples.append(VisualRipple(rx, ry, color=(255, 100, 255), max_radius=60))
                            last_click_time = now
                            gesture_status = "DOUBLE CLICK"

                    # D. RIGHT CLICK GESTURE: Thumb + Middle Pinch
                    elif dist_thumb_middle < PINCH_TRIGGER_DIST:
                        if not is_right_down:
                            try:
                                pyautogui.rightClick()
                            except Exception:
                                pass
                            play_sound("right_click")
                            ripples.append(VisualRipple(mx, my, color=(0, 0, 255), max_radius=50))
                            is_right_down = True
                            gesture_status = "RIGHT CLICK"
                    else:
                        is_right_down = False

                        # E. LEFT CLICK & HOLD / DRAG: Thumb + Index Pinch
                        if dist_thumb_index < PINCH_TRIGGER_DIST:
                            if not is_left_down:
                                pinch_start_time = now
                                is_left_down = True
                                try:
                                    pyautogui.mouseDown()
                                except Exception:
                                    pass
                                play_sound("click")
                                ripples.append(VisualRipple(ix, iy, color=(0, 255, 0), max_radius=40))

                            hold_duration = now - pinch_start_time
                            if hold_duration > 0.25:
                                gesture_status = "DRAGGING / HOLD"
                            else:
                                gesture_status = "LEFT CLICK"

                            # Visual lock line between thumb & index
                            cv2.line(display_frame, (ix, iy), (tx, ty), (0, 255, 0), 4, cv2.LINE_AA)
                            cv2.circle(display_frame, ((ix+tx)//2, (iy+ty)//2), 12, (0, 255, 0), -1)

                        elif dist_thumb_index > PINCH_RELEASE_DIST:
                            if is_left_down:
                                try:
                                    pyautogui.mouseUp()
                                except Exception:
                                    pass
                                is_left_down = False
                                gesture_status = "RELEASED"

                        # F. CURSOR POSITION EXECUTION
                        try:
                            pyautogui.moveTo(int(smooth_x), int(smooth_y))
                        except Exception:
                            pass
                        if gesture_status == "IDLE":
                            gesture_status = "TRACKING CURSOR"

            elif current_mode == "CANVAS":
                # AIR CANVAS DRAWING MODE
                gesture_status = "AIR CANVAS"
                if dist_thumb_index < PINCH_TRIGGER_DIST:
                    # Draw on Canvas
                    col = canvas_colors[current_color_idx]
                    cv2.circle(canvas_mask, (ix, iy), brush_thickness, col, -1)
                    if len(trail_points) >= 2:
                        cv2.line(canvas_mask, trail_points[-2], trail_points[-1], col, brush_thickness * 2, cv2.LINE_AA)
                    gesture_status = "PAINTING"
                    cv2.circle(display_frame, (ix, iy), brush_thickness + 4, col, 2)
                else:
                    cv2.circle(display_frame, (ix, iy), brush_thickness, (255, 255, 255), 2)

        # ---------------------------------------------------------------------
        # 3. DRAW MOTION TRAILS & PARTICLES
        # ---------------------------------------------------------------------
        if len(trail_points) > 1:
            for t_i in range(1, len(trail_points)):
                t_alpha = t_i / len(trail_points)
                t_thick = max(1, int(t_alpha * 4))
                cv2.line(display_frame, trail_points[t_i - 1], trail_points[t_i], 
                         (0, int(255 * t_alpha), 255), t_thick, cv2.LINE_AA)

        # ---------------------------------------------------------------------
        # 4. DRAW ANIMATED CYBERNETIC RETICLE AROUND ACTIVE CURSOR
        # ---------------------------------------------------------------------
        if active_cursor_pos:
            cx, cy = active_cursor_pos
            # Rotating crosshairs
            rad = math.radians(reticle_angle)
            cos_a = math.cos(rad)
            sin_a = math.sin(rad)
            r_len = 22

            # Reticle Circles
            cv2.circle(display_frame, (cx, cy), 18, (0, 255, 255), 1, cv2.LINE_AA)
            cv2.circle(display_frame, (cx, cy), 6, (255, 255, 255), -1, cv2.LINE_AA)

            # Four rotating ticks
            for ang_offset in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
                cur_a = rad + ang_offset
                p1 = (int(cx + math.cos(cur_a) * 14), int(cy + math.sin(cur_a) * 14))
                p2 = (int(cx + math.cos(cur_a) * r_len), int(cy + math.sin(cur_a) * r_len))
                cv2.line(display_frame, p1, p2, (0, 255, 255), 2, cv2.LINE_AA)

        # ---------------------------------------------------------------------
        # 5. DRAW ACTIVE SHOCKWAVE RIPPLES
        # ---------------------------------------------------------------------
        ripples = [r for r in ripples if r.draw(display_frame)]

        # Blend Air Canvas Mask
        if current_mode == "CANVAS":
            display_frame = cv2.addWeighted(display_frame, 1.0, canvas_mask, 0.85, 0)

        # ---------------------------------------------------------------------
        # 6. HOLOGRAPHIC SCI-FI HUD PANELS
        # ---------------------------------------------------------------------
        # Left Panel (System Telemetry & Face Matrix)
        panel_w = 340
        overlay = display_frame.copy()
        cv2.rectangle(overlay, (15, 15), (panel_w, h - 20), (15, 18, 22), -1)
        cv2.addWeighted(overlay, 0.72, display_frame, 0.28, 0, display_frame)
        cv2.rectangle(display_frame, (15, 15), (panel_w, h - 20), (0, 255, 200), 1)

        # Panel Header
        cv2.putText(display_frame, "NEURAL MASTER X", (30, 48), cv2.FONT_HERSHEY_TRIPLEX, 0.75, (0, 255, 200), 2)
        cv2.line(display_frame, (30, 60), (panel_w - 20, 60), (0, 255, 200), 1)

        # Mode Badge
        mode_color = (0, 255, 0) if current_mode == "MOUSE" else (255, 0, 255)
        cv2.putText(display_frame, f"MODE: [{current_mode}]", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, mode_color, 2)
        cv2.putText(display_frame, f"ACTION: {gesture_status}", (30, 118), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1)

        # Smooth Virtual Cursor Coordinates
        cv2.putText(display_frame, f"SCREEN: ({int(smooth_x)}, {int(smooth_y)})", (30, 145), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 220, 255), 1)

        # Biometric Face Telemetry
        cv2.line(display_frame, (30, 165), (panel_w - 20, 165), (50, 70, 80), 1)
        cv2.putText(display_frame, "BIOMETRIC AFFECTIVE AI", (30, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        cv2.putText(display_frame, f"MOOD: {face_telemetry['mood']}", (30, 212), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 2)
        
        # Posture Status
        posture_col = (0, 255, 0) if face_telemetry["posture"] == "OPTIMAL" else (0, 120, 255)
        cv2.putText(display_frame, f"POSTURE: {face_telemetry['posture']}", (30, 238), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, posture_col, 1)

        # Eye Blink Indicators
        blink_str = "BLINK: " + ("L " if face_telemetry["blink_l"] else "- ") + ("R" if face_telemetry["blink_r"] else "-")
        cv2.putText(display_frame, blink_str, (30, 264), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # Vocal Activity Meter
        jaw_pct = int(face_telemetry["jaw_open"] * 100)
        cv2.putText(display_frame, f"VOCAL: {jaw_pct}%", (30, 292), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
        cv2.rectangle(display_frame, (110, 282), (panel_w - 30, 294), (40, 45, 50), -1)
        cv2.rectangle(display_frame, (110, 282), (110 + int((panel_w - 140) * face_telemetry["jaw_open"]), 294), (0, 255, 120), -1)

        # Quick Gesture Controls Guide
        cv2.line(display_frame, (30, 315), (panel_w - 20, 315), (50, 70, 80), 1)
        cv2.putText(display_frame, "SPATIAL GESTURES:", (30, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 200), 1)
        gestures_guide = [
            "- Index Tip: Cursor Move",
            "- Thumb+Index Pinch: Left Click/Drag",
            "- Thumb+Middle Pinch: Right Click",
            "- Thumb+Ring Pinch: Double Click",
            "- 2-Fingers (Peace): Inertial Scroll",
            "- Thumb+Pinky: Volume Dial",
            "- [M] Switch to Air Canvas Draw",
            "- [S] Audio Toggle",
            "- [SPACE] Instant Screenshot"
        ]
        for g_idx, g_text in enumerate(gestures_guide):
            cv2.putText(display_frame, g_text, (30, 358 + g_idx * 21), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 220, 220), 1)

        # Performance Stats (Top Right)
        stat_w = 190
        cv2.rectangle(display_frame, (w - stat_w - 15, 15), (w - 15, 75), (20, 25, 30), -1)
        cv2.rectangle(display_frame, (w - stat_w - 15, 15), (w - 15, 75), (0, 255, 0), 1)
        cv2.putText(display_frame, f"FPS: {int(fps)}", (w - stat_w, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, f"SOUND: {'ON' if AUDIO_ENABLED else 'OFF'}", (w - stat_w, 64), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)

        # Shutter Flash Animation (Screen Snapshot)
        if now - shutter_flash_time < 0.2:
            flash_alpha = max(0.0, 1.0 - (now - shutter_flash_time) / 0.2)
            white_overlay = np.full_like(display_frame, 255)
            cv2.addWeighted(white_overlay, flash_alpha * 0.75, display_frame, 1.0 - flash_alpha * 0.75, 0, display_frame)

        cv2.imshow(window_name, display_frame)

        # ---------------------------------------------------------------------
        # 7. KEYBOARD CONTROLS
        # ---------------------------------------------------------------------
        key = cv2.waitKey(1) & 0xFF
        if key in [27, ord('q'), ord('Q')]:
            break
        elif key in [ord('m'), ord('M')]:
            current_mode = "CANVAS" if current_mode == "MOUSE" else "MOUSE"
            play_sound("mode_switch")
        elif key in [ord('s'), ord('S')]:
            AUDIO_ENABLED = not AUDIO_ENABLED
            play_sound("click")
        elif key in [ord('c'), ord('C')]:
            canvas_mask = np.zeros((h, w, 3), dtype=np.uint8)
            play_sound("mode_switch")
        elif key == 32: # SPACE: Take Shutter Snapshot
            timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            snap_path = os.path.join(SCREENSHOTS_DIR, f"snapshot_{timestamp_str}.png")
            cv2.imwrite(snap_path, display_frame)
            play_sound("snapshot")
            shutter_flash_time = now
            print(f"📸 Saved snapshot to: {snap_path}")
        elif key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
            current_color_idx = (key - ord('1')) % len(canvas_colors)
            play_sound("click")

    cam.release()
    cv2.destroyAllWindows()
    print("✨ Neural Master X Session Concluded Successfully.")

if __name__ == "__main__":
    main()