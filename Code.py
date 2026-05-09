from cvzone.PoseModule import PoseDetector
import cv2

# Ruta del video
video_path = "Video.mp4"

cap = cv2.VideoCapture(video_path)
detector = PoseDetector()

# Lista donde se guardarán los datos
serie_angulos = []

frame_num = 0

while True:
    success, img = cap.read()

    if not success:
        break

    frame_num += 1

    img = detector.findPose(img)
    lmList, _ = detector.findPosition(img, draw=False)

    if lmList:
        # Ángulos
        left_arm, img = detector.findAngle(
            lmList[11][:2], lmList[13][:2], lmList[15][:2], img)

        left_wrist, img = detector.findAngle(
            lmList[13][:2], lmList[15][:2], lmList[19][:2], img)

        right_arm, img = detector.findAngle(
            lmList[12][:2], lmList[14][:2], lmList[16][:2], img)

        right_wrist, img = detector.findAngle(
            lmList[14][:2], lmList[16][:2], lmList[20][:2], img)

        # Guardar datos en lista
        serie_angulos.append({
            "frame": frame_num,
            "left_arm": int(left_arm),
            "left_wrist": int(left_wrist),
            "right_arm": int(right_arm),
            "right_wrist": int(right_wrist)
        })

        # Mostrar texto
        cv2.putText(img, f"L Arm: {int(left_arm)}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.putText(img, f"R Arm: {int(right_arm)}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Pose Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Mostrar algunos datos al final
print("\n===== DATOS CAPTURADOS =====\n")

for dato in serie_angulos[:10]:
    print(dato)

print(f"\nTotal de frames analizados: {len(serie_angulos)}")