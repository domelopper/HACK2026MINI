from cvzone.PoseModule import PoseDetector
import cv2

# Ruta del video
video_path = "Video.mp4"

cap = cv2.VideoCapture(video_path)
detector = PoseDetector()

while True:
    success, img = cap.read()

    # Termina cuando el video acaba
    if not success:
        break

    img = detector.findPose(img)
    lmList, _ = detector.findPosition(img, draw=False)

    if lmList:
        # Ángulos de brazos
        left_arm, img = detector.findAngle(
            lmList[11][:2], lmList[13][:2], lmList[15][:2], img)

        right_arm, img = detector.findAngle(
            lmList[12][:2], lmList[14][:2], lmList[16][:2], img)

        # Ángulos de muñecas
        left_wrist, img = detector.findAngle(
            lmList[13][:2], lmList[15][:2], lmList[19][:2], img)

        right_wrist, img = detector.findAngle(
            lmList[14][:2], lmList[16][:2], lmList[20][:2], img)

        # Mostrar texto
        cv2.putText(img, f"L Arm: {int(left_arm)}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.putText(img, f"R Arm: {int(right_arm)}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.putText(img, f"L Wrist: {int(left_wrist)}", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.putText(img, f"R Wrist: {int(right_wrist)}", (20, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Pose Detection", img)

    # Presiona Q para salir
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()