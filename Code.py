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

# Calcula el FRAME_SKIP automáticamente según los FPS del video
fps = cap.get(cv2.CAP_PROP_FPS)
SAMPLE_EVERY_N_SECONDS = 0.2          # 1 muestra cada 0.2 segundos
FRAME_SKIP = max(1, int(fps * SAMPLE_EVERY_N_SECONDS))
print(f"FPS del video: {fps:.1f} | Analizando 1 frame cada {FRAME_SKIP} frames")

# =========================
# PROCESS VIDEO
# =========================
while True:
    success, img = cap.read()
    if not success:
        break
    frame_num += 1

    # Saltar frames según FRAME_SKIP
    if frame_num % FRAME_SKIP != 0:
        continue

    img = detector.findPose(img)
    lmList, _ = detector.findPosition(img, draw=False)

    if lmList:
        # Ángulos principales
        left_arm, img = detector.findAngle(
            lmList[11][:2], lmList[13][:2], lmList[15][:2], img)
        right_arm, img = detector.findAngle(
            lmList[12][:2], lmList[14][:2], lmList[16][:2], img)
        left_wrist, img = detector.findAngle(
            lmList[13][:2], lmList[15][:2], lmList[19][:2], img)
        right_wrist, img = detector.findAngle(
            lmList[14][:2], lmList[16][:2], lmList[20][:2], img)

        # Guardar datos
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
prompt = """
Eres un entrenador experto en ping pong de alto rendimiento.
Recibirás una serie de datos frame por frame de un saque, con ángulos del cuerpo del jugador.
Tu tarea es hacer un análisis técnico profundo, profesional y claro.
Debes:
- Analizar la consistencia del saque
- Detectar patrones en brazos y muñecas
- Identificar errores técnicos
- Dar recomendaciones de mejora
- Usar un tono profesional con acento argentino suave
A continuación tienes todos los frames del saque:
"""

for d in serie_angulos:
    prompt += f"""
Frame {d['frame']}:
- Brazo izquierdo: {d['left_arm']}°
- Muñeca izquierda: {d['left_wrist']}°
- Brazo derecho: {d['right_arm']}°
- Muñeca derecha: {d['right_wrist']}°
"""

prompt += """
Ahora realiza el análisis completo del saque.
"""

# =========================
# OUTPUT
# =========================
print("\n===== PROMPT FINAL =====\n")
print(prompt)
print("\n===== RESUMEN =====")
print(f"Frames analizados: {len(serie_angulos)}")
print(f"Muestreo: 1 frame cada {FRAME_SKIP} frames ({SAMPLE_EVERY_N_SECONDS}s)")