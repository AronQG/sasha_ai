import cv2
import mediapipe as mp
import numpy as np
import os
import datetime
from core.memory import Memory

# === Чувствительность: подбиралось для 30-60 см от камеры ===
EYE_CLOSED_THRESHOLD = 0.03   # увеличено, чтобы ловить моргание дальше от камеры
MOUTH_OPEN_THRESHOLD = 0.018  # рот открыт (минимальный порог)
HAND_NEAR_MOUTH_THRESHOLD = 0.16  # чем больше — тем дальше видно жест

BLINK_FRAME_THRESHOLD = 2      # сколько кадров считать морганием
SLEEP_FRAME_THRESHOLD = 70     # сколько кадров подряд — сон (примерно 2-3 сек)

class CameraWatcher:
    def __init__(self, memory=None, user="local_user", photo_dir="snapshots"):
        self.memory = memory or Memory()
        self.user = user
        self.photo_dir = photo_dir
        os.makedirs(photo_dir, exist_ok=True)
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
        self.pose = mp.solutions.pose.Pose(static_image_mode=False)
        self.blink_counter = 0
        self.blink_frames = 0
        self.sleep_frames = 0
        self.last_event_time = dict(eat=0, drink=0, sleep=0)

    def run(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_result = self.face_mesh.process(rgb)
            pose_result = self.pose.process(rgb)
            now = datetime.datetime.now()

            # ==== BLINK (моргает)
            if face_result.multi_face_landmarks:
                face = face_result.multi_face_landmarks[0]
                left_eye_top = np.array([face.landmark[159].x, face.landmark[159].y])
                left_eye_bot = np.array([face.landmark[145].x, face.landmark[145].y])
                right_eye_top = np.array([face.landmark[386].x, face.landmark[386].y])
                right_eye_bot = np.array([face.landmark[374].x, face.landmark[374].y])
                left_dist = np.linalg.norm(left_eye_top - left_eye_bot)
                right_dist = np.linalg.norm(right_eye_top - right_eye_bot)
                dist = (left_dist + right_dist) / 2
                if dist < EYE_CLOSED_THRESHOLD:
                    self.blink_frames += 1
                else:
                    if self.blink_frames >= BLINK_FRAME_THRESHOLD:
                        self.blink_counter += 1
                        self.memory.log_event("blink", self.user, f"blink_{self.blink_counter}", "", now.isoformat())
                        print(f"BLINK #{self.blink_counter}")
                    self.blink_frames = 0

            # ==== ЕДА/ПИТЬЁ
            if face_result.multi_face_landmarks and pose_result.pose_landmarks:
                face = face_result.multi_face_landmarks[0]
                lm = pose_result.pose_landmarks.landmark
                mouth_open = self._get_mouth_open(face)
                hand_near_mouth = self._hand_near_mouth(lm, face)
                if mouth_open and hand_near_mouth and (now.timestamp() - self.last_event_time['eat'] > 60):
                    self.last_event_time['eat'] = now.timestamp()
                    self.save_event(frame, "eat")
                    print("EAT detected")
                elif hand_near_mouth and not mouth_open and (now.timestamp() - self.last_event_time['drink'] > 60):
                    self.last_event_time['drink'] = now.timestamp()
                    self.save_event(frame, "drink")
                    print("DRINK detected")

            # ==== СОН ====
            if face_result.multi_face_landmarks:
                if dist < EYE_CLOSED_THRESHOLD / 1.5:
                    self.sleep_frames += 1
                else:
                    if self.sleep_frames >= SLEEP_FRAME_THRESHOLD:
                        self.save_event(frame, "sleep")
                        print("SLEEP detected")
                    self.sleep_frames = 0

            cv2.imshow('Sasha Camera', frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
            if key == ord('s'):
                self.save_event(frame, "snapshot")
                print("Snapshot saved")
        cap.release()
        cv2.destroyAllWindows()

    def save_event(self, frame, event_type):
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        path = os.path.join(self.photo_dir, f"{event_type}_{now}.jpg")
        cv2.imwrite(path, frame)
        self.memory.log_event(event_type, self.user, "camera", media_path=path)

    def _get_mouth_open(self, face):
        top = np.array([face.landmark[13].x, face.landmark[13].y])
        bot = np.array([face.landmark[14].x, face.landmark[14].y])
        dist = np.linalg.norm(top - bot)
        return dist > MOUTH_OPEN_THRESHOLD

    def _hand_near_mouth(self, lm, face):
        mouth = np.array([(face.landmark[13].x + face.landmark[14].x) / 2,
                          (face.landmark[13].y + face.landmark[14].y) / 2])
        left_wrist = np.array([lm[15].x, lm[15].y])
        right_wrist = np.array([lm[16].x, lm[16].y])
        return (
            np.linalg.norm(left_wrist - mouth) < HAND_NEAR_MOUTH_THRESHOLD or
            np.linalg.norm(right_wrist - mouth) < HAND_NEAR_MOUTH_THRESHOLD
        )
