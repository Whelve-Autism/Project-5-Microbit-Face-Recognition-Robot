<div align="center">

# Project 5 · micro:bit Face Recognition Robot

**Tinybit · Yahboom K210 · Serial communication**

A coursework demonstration in which a K210 vision module recognises enrolled faces and a BBC micro:bit displays the corresponding number on its LED matrix.

</div>

[Project code](#repository-layout) · [Setup](#setup) · [Demo](#demo) · [Data handling](#data-handling)

## How it works

The K210 detects and aligns a face, extracts its feature vector, and compares it with the templates enrolled for the current session. It sends a recognition result over UART. The micro:bit runs the Yahboom receiver firmware and displays the matching enrolment index, starting at `0`.

## Repository layout

| Entry | Description |
| --- | --- |
| [face_signature.py](./face_signature.py) | Computes and records a 64-bit signature from an enrolled feature vector. |
| [tools/prepare_k210.py](./tools/prepare_k210.py) | Adds signature recording to the official K210 example and produces a standalone `main.py` for deployment. |

## Setup

You need a BBC micro:bit, a Tinybit chassis, a Yahboom K210 vision module with an SD card, and Python 3 on your computer.

1. Use [Yahboom's face recognition tutorial](https://www.yahboom.net/public/upload/upload-html/1692934122/2.8%20Facial%20recognition.html) and [official download index](https://github.com/YahboomTechnology/k210-module-EN/blob/main/Data%20download%20link%20URL.txt) to obtain `2.8_face_recog.py`, `microbit-face_rec.hex`, and the three models listed below. Place `2.8_face_recog.py` at `k210/2.8_face_recog.py` in your local checkout.
2. From the repository root, run the following command to build `build/main.py`. The builder accepts an alternate `--output` path for a subsequent build.

   ```bash
   python3 tools/prepare_k210.py k210/2.8_face_recog.py
   ```

3. Copy the generated `main.py` to the root of the K210 SD card and use the vendor's offline startup procedure. Put the model files at the following SD card paths.

   ```text
   KPU/yolo_face_detect/face_detect_320x240.kmodel
   KPU/face_recognization/ld5.kmodel
   KPU/face_recognization/feature_extraction.kmodel
   ```

4. Flash `microbit-face_rec.hex` onto the micro:bit. Connect the K210 TX line to micro:bit P2 (RX) with a common ground, following the [Yahboom wiring guide](https://www.yahboom.net/public/upload/upload-html/1697538055/microbit_%20K210%20facial%20recognition.html). The receiver uses UART at `115200` baud.

## Demo

1. Start the hardware with one volunteer in view. Press **BOOT** on the K210 to enrol the face.
2. Repeat with a second volunteer. Show each volunteer to the camera separately and check the K210 status and the micro:bit number against the enrolment order.
3. Check that the K210 has written one entry per enrolment to `data.txt`. Restart the K210 to begin a fresh enrolment session.

## Data handling

Live matching uses feature vectors held in K210 memory. At enrolment, the project records a 64-bit signature derived from the signs of the coefficients in the device's local `data.txt`. Signatures can collide and are unsuitable for cryptographic protection or identity verification. Keep the generated data file on the device.

## Credits

The device-side recognition workflow, MakeCode receiver firmware, and models come from [Yahboom's K210 course materials](https://github.com/YahboomTechnology/k210-module-EN). The receiver uses the [Yahboom K210 MakeCode extension](https://github.com/YahboomTechnology/K210-Module). This project adds local signature recording and a build step for the original example.
