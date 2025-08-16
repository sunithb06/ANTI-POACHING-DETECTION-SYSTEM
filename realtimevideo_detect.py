import os
import sys
import cv2
import smtplib
import threading
import platform
from tkinter import Tk, Label, Button, filedialog, StringVar, Frame, BOTTOM, X, BOTH
from email.message import EmailMessage
from datetime import datetime
from ultralytics import YOLO


EMAIL_ADDRESS = 'sunithb306@gmail.com'
EMAIL_PASSWORD = 'cbjv uxoa kwke oiwk'
TO_EMAIL = 'sunithb06@gmail.com'


model = YOLO('best.pt')
danger_classes = {'gun', 'poacher', 'hunter'}

def send_email_alert(image_path):
    msg = EmailMessage()
    msg['Subject'] = '🚨 Poacher/Hunter/Gun Detected Alert'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg.set_content('Alert: A poacher, hunter, or gun was detected. See the attached snapshot.')

    with open(image_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename=os.path.basename(image_path))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("📧 Email sent!")
    except Exception as e:
        print("❌ Failed to send email:", e)


def detect_objects(video_path, status_var):
    cap = cv2.VideoCapture(0 if video_path == 'webcam' else video_path)
    if not cap.isOpened():
        status_var.set("❌ Error opening video/camera")
        return

    if video_path != 'webcam':
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))
    else:
        out = None

    email_sent = False
    status_var.set("🔍 Detecting... Press 'Q' to stop preview")
    status_var_label.config(fg="blue")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame, conf=0.5, verbose=False)
        r = results[0]
        alert_triggered = False

        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            label = model.names[cls].lower()

            if label in danger_classes:
                color = (0, 0, 255)
                alert_triggered = True
            else:
                color = (0, 255, 0)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        if alert_triggered and not email_sent:
            snapshot_path = f"alert_frame_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(snapshot_path, frame)
            send_email_alert(snapshot_path)
            email_sent = True
            status_var.set("🚨 ALERT! Detected danger. Email sent.")
            status_var_label.config(fg="red", font=("Helvetica", 12, "bold"))

            # Optional beep (Windows only)
            if platform.system() == 'Windows':
                import winsound
                winsound.Beep(1000, 500)

            # Popup alert
            def show_alert_popup():
                popup = Tk()
                popup.title("🚨 ALERT DETECTED")
                popup.geometry("300x150")
                popup.configure(bg='red')
                Label(popup, text="⚠️ DANGER DETECTED ⚠️", font=("Helvetica", 16, "bold"),
                      fg="white", bg="red").pack(expand=True)
                Button(popup, text="Dismiss", command=popup.destroy,
                       bg="white", fg="red", font=("Helvetica", 12, "bold")).pack(pady=10)
                popup.mainloop()

            threading.Thread(target=show_alert_popup).start()

        cv2.imshow('Detection Preview', frame)
        if out:
            out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()

    if video_path != 'webcam':
        status_var.set("✅ Detection completed. Output saved as output.mp4")
    else:
        status_var.set("✅ Real-time detection session ended.")
    status_var_label.config(fg="green")

# -------------------- GUI --------------------
def start_gui():
    def browse_file():
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            video_path_var.set(file_path)
            status_var.set("🎬 Video selected. Ready to start.")
            status_var_label.config(fg="blue")

    def start_detection_thread(source=None):
        if source == 'webcam':
            video_path = 'webcam'
        else:
            video_path = video_path_var.get()
            if not video_path:
                status_var.set("❗ Please select a video first.")
                status_var_label.config(fg="orange")
                return
        thread = threading.Thread(target=detect_objects, args=(video_path, status_var))
        thread.start()

    global status_var_label
    root = Tk()
    root.title("🎯 Anti-Poaching Detection System")
    root.geometry("600x380")
    root.configure(bg="#f2f2f2")

    # Header
    top_frame = Frame(root, bg="#003366", height=60)
    top_frame.pack(fill=X)
    Label(top_frame, text="ANTI POACHING DETECTION SYSTEM", bg="#003366", fg="white",
          font=("Helvetica", 18, "bold")).pack(pady=10)

    # Body
    mid_frame = Frame(root, bg="#f2f2f2", pady=20)
    mid_frame.pack(fill=BOTH, expand=True)

    video_path_var = StringVar()
    status_var = StringVar()
    status_var.set("📂 Please select a video file or start webcam")

    Button(mid_frame, text="📁 Browse Video", font=("Helvetica", 12), width=25,
           command=browse_file, bg="#4CAF50", fg="white").pack(pady=5)
    Button(mid_frame, text="▶️ Start Detection", font=("Helvetica", 12), width=25,
           command=lambda: start_detection_thread(), bg="#2196F3", fg="white").pack(pady=5)
    Button(mid_frame, text="🎥 Start Real-Time Detection", font=("Helvetica", 12), width=25,
           command=lambda: start_detection_thread('webcam'), bg="#FF5722", fg="white").pack(pady=5)

    Label(mid_frame, textvariable=video_path_var, wraplength=550,
          fg="#333", bg="#f2f2f2", font=("Helvetica", 10)).pack(pady=5)
    status_var_label = Label(mid_frame, textvariable=status_var, wraplength=550,
                             fg="darkgreen", bg="#f2f2f2", font=("Helvetica", 12, "italic"))
    status_var_label.pack(pady=10)

    # Footer
    footer = Frame(root, bg="#dddddd", height=30)
    footer.pack(fill=X, side=BOTTOM)
    Label(footer, text="Developed by Sunith B  |  Wildlife Protection", bg="#dddddd",
          fg="black", font=("Helvetica", 9)).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    start_gui()
