# ANTI-POACHING-DETECTION-SYSTEM
This project implements an AI-powered Anti-Poaching Detection System using YOLO for real-time identification of guns, hunters, and poachers from video or webcam. On detecting danger, it triggers alerts with snapshots via email, optional sound and popup warnings, and saves annotated video output through a user-friendly GUI.
# 🦌 Anti-Poaching Detection System  

## 📌 Overview  
Poaching poses a serious threat to wildlife conservation. This project presents an **AI-powered Anti-Poaching Detection System** that uses **YOLO-based object detection** to automatically identify dangerous activities such as the presence of guns, hunters, or poachers in real time.  

The system supports both **video file input** and **live webcam streams**, enabling its deployment in diverse field conditions. Once a potential threat is detected, the system triggers an alert by:  
- Sending an **email notification with snapshot evidence** 📧  
- Displaying a **popup warning message** ⚠️  
- Producing an **optional sound alarm** 🔊  
- Saving an **annotated video** with detection results 🎥  

---

## 🚀 Features  
- **Real-time Detection** using YOLO for guns, hunters, and poachers.  
- **Dual Input Modes**: Webcam (live) or pre-recorded video.  
- **Automated Alerts**: Email with attached snapshot when a danger is detected.  
- **Multi-modal Notifications**: Popup, sound, and status updates in GUI.  
- **User-Friendly GUI** built with Tkinter for easy operation.  
- **Secure Email Integration** using Gmail’s SMTP protocol.  

---

## ⚙️ Tech Stack  
- **Language**: Python  
- **Libraries**: OpenCV, Tkinter, smtplib, ultralytics (YOLO), threading, platform  
- **Model**: YOLO (custom trained `best.pt` weights)  
- **Alerts**: Email + Popup + Beep  

---

## 🌍 Applications  
- Wildlife sanctuaries and protected reserves.  
- Anti-poaching surveillance in forests.  
- Integration with drone or CCTV monitoring systems.  
- Real-time monitoring in sensitive conservation zones.  



