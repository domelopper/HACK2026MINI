import cv2
from cvzone.PoseModule import PoseDetector

class VideoAnalyzer:
    def __init__(self, video_path, sample_every_n_seconds=0.2):
        self.video_path = video_path
        self.sample_every_n_seconds = sample_every_n_seconds

    def get_prompt(self):
        cap = cv2.VideoCapture(self.video_path)
        detector = PoseDetector()
        serie_angulos = []
        frame_num = 0

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_skip = max(1, int(fps * self.sample_every_n_seconds))

        while True:
            success, img = cap.read()
            if not success:
                break
            frame_num += 1
            if frame_num % frame_skip != 0:
                continue

            img = detector.findPose(img)
            lmList, _ = detector.findPosition(img, draw=False)

            if lmList:
                left_arm,    img = detector.findAngle(lmList[11][:2], lmList[13][:2], lmList[15][:2], img)
                right_arm,   img = detector.findAngle(lmList[12][:2], lmList[14][:2], lmList[16][:2], img)
                left_wrist,  img = detector.findAngle(lmList[13][:2], lmList[15][:2], lmList[19][:2], img)
                right_wrist, img = detector.findAngle(lmList[14][:2], lmList[16][:2], lmList[20][:2], img)

                serie_angulos.append({
                    "frame":       frame_num,
                    "left_arm":    int(left_arm),
                    "left_wrist":  int(left_wrist),
                    "right_arm":   int(right_arm),
                    "right_wrist": int(right_wrist)
                })

            cv2.imshow("Pose Detection", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        # Construir y retornar el prompt directamente
        prompt = "Eres un entrenador experto en ping pong de alto rendimiento.\n"
        prompt += "Analizá estos ángulos frame por frame de un saque y dá un análisis técnico completo.\n"
        prompt += "Detectá errores, patrones y dá recomendaciones. Usá acento argentino suave.\n\n"
        for d in serie_angulos:
            prompt += f"Frame {d['frame']}: brazo_izq={d['left_arm']}°, muneca_izq={d['left_wrist']}°, brazo_der={d['right_arm']}°, muneca_der={d['right_wrist']}°\n"
        prompt += "\nAhora realizá el análisis completo."

        return prompt