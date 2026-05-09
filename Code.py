from cvzone.PoseModule import PoseDetector
import cv2

# =========================
# VIDEO INPUT
# =========================
video_path = "Video.mp4"
cap = cv2.VideoCapture(video_path)
detector = PoseDetector()
serie_angulos = []
frame_num = 0

fps = cap.get(cv2.CAP_PROP_FPS)
SAMPLE_EVERY_N_SECONDS = 0.2
FRAME_SKIP = max(1, int(fps * SAMPLE_EVERY_N_SECONDS))

# =========================
# PROCESS VIDEO
# =========================
while True:
    success, img = cap.read()
    if not success:
        break
    frame_num += 1

    if frame_num % FRAME_SKIP != 0:
        continue

    img = detector.findPose(img)
    lmList, _ = detector.findPosition(img, draw=False)

    if lmList:
        left_arm, img = detector.findAngle(
            lmList[11][:2], lmList[13][:2], lmList[15][:2], img)
        right_arm, img = detector.findAngle(
            lmList[12][:2], lmList[14][:2], lmList[16][:2], img)
        left_wrist, img = detector.findAngle(
            lmList[13][:2], lmList[15][:2], lmList[19][:2], img)
        right_wrist, img = detector.findAngle(
            lmList[14][:2], lmList[16][:2], lmList[20][:2], img)

        serie_angulos.append({
            "frame": frame_num,
            "left_arm": int(left_arm),
            "left_wrist": int(left_wrist),
            "right_arm": int(right_arm),
            "right_wrist": int(right_wrist)
        })

    cv2.imshow("Pose Detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# =========================
# BUILD FINAL PROMPT
# =========================
prompt = "Eres un entrenador experto en ping pong de alto rendimiento.\n"
prompt += "Recibirás una serie de datos frame por frame de un saque, con ángulos del cuerpo del jugador.\n"
prompt += "Tu tarea es hacer un análisis técnico profundo, profesional y claro.\n"
prompt += "Debes:\n"
prompt += "- Analizar la consistencia del saque\n"
prompt += "- Detectar patrones en brazos y muñecas\n"
prompt += "- Identificar errores técnicos\n"
prompt += "- Dar recomendaciones de mejora\n"
prompt += "- Usar un tono profesional con acento argentino suave\n"
prompt += "A continuación tienes todos los frames del saque:\n"

for d in serie_angulos:
    prompt += f"\nFrame {d['frame']}:\n"
    prompt += f"- Brazo izquierdo: {d['left_arm']}°\n"
    prompt += f"- Muñeca izquierda: {d['left_wrist']}°\n"
    prompt += f"- Brazo derecho: {d['right_arm']}°\n"
    prompt += f"- Muñeca derecha: {d['right_wrist']}°\n"

prompt += "\nAhora realiza el análisis completo del saque."

# =========================
# OUTPUT — solo el prompt listo para la API
# =========================
print(prompt)