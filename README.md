# Real-Time Face Recognition Attendance Monitoring System

An automated computer vision solution designed to streamline classroom attendance logging. Built in Python with a graphical interface via Tkinter, this application replaces traditional roll calls by identifying individuals dynamically through a webcam and recording timestamped presence directly to CSV databases.

##  Core Computer Vision Pipeline

The application optimizes face capture and verification through highly specific image-processing enhancements:
* **Face Detection:** Leverages OpenCV's `CascadeClassifier` with tuned `detectMultiScale` parameters (`scaleFactor=1.1`, `minNeighbors=6`) to filter background noise and maintain stable bounding boxes.
* **LBPH (Local Binary Patterns Histograms):** Utilizes an OOP-based Local Binary Patterns face recognizer to decode spatial patterns and textures, enabling lightweight, rapid recognition without demanding GPU dependencies.
* **Histogram Equalization:** Integrates `cv2.equalizeHist()` globally across both the data collection phase and real-time inference loop to flatten variable room lighting and enhance edge contrast.
* **Multi-Frame Voting Engine:** Implements a strict temporal buffer (`BUFFER_SIZE = 5`) evaluating consecutive frame readings. Attendance is only authorized when a 60% majority consensus is reached alongside an elevated confidence ceiling (< 35 threshold), drastically eliminating false positives.
* **Stable Presence Verification:** Evaluates continuous face locks over a 2.5-second observation window prior to state commits to prevent accidental logging from transient movement.

##  Features

* **Multi-Angle Profile Generation:** Guided interactive image registration capturing structural facial variances (`STRAIGHT`, `LEFT`, `RIGHT`, `UP`, `DOWN`) to populate localized custom training directories.
* **Smart Attendance Classification:** Automatically categorizes entries into `Early`, `On Time`, `Late`, or `Very Late` based on rigid time boundaries and customizable grace windows.
* **Secure Admin Controls:** Built-in password-protected administration gateway governing the compilation and updating of the trained facial weights mapping (`Trainner.yml`).
* **Robust File Handling & Backups:** Implements an asynchronous file fallback routine (`attendance.csv` / `attendance_backup.csv`) to secure record entries even when the primary database is experiencing system permission blocks or open locks.
* **Live Analytics Hub:** Populates an updating real-time `Treeview` dashboard reflecting active session parameters, total registered roster size, and current network sync.

##  Tech Stack

* **Language:** Python 3.x
* **Computer Vision:** OpenCV (`opencv-contrib-python`)
* **Scientific Computing:** NumPy, Pandas
* **Imaging Processing:** Pillow (PIL)
* **GUI Engine:** Tkinter (Standard Library)
* **Data Storage:** Flat CSV Architecture
