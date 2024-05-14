# IoT and Communication Solution 📡🚀

This project integrates hardware and software components to create a versatile image classification system. Upon activation, triggered by a microswitch, a camera module captures images and saves them to an SD card. A deep learning model deployed on a microcontroller retrieves these images, conducts classification, and transmits the results to a receiver via a transmitter. Once received, the classification results are updated in a Firebase cloud database. 

## Getting Started 🏁
### Prerequisites
Clone the repo: 
```
https://github.com/FYP-19/IoT-and-Communication.git
```
Go to directory and install necessary liberies including:
```
pip install RPi.GPIO
```
```
pip install Pillow
```
```
pip install tflite_runtime
```
* Update the model path in file ``Executor.py``.
* Update the firestore database credential file path in ``DB_manager.py``.  

## System Architecture Diagram
 Provide an overall architectural diagram illustrating how the various components of your system interact with each other.
 
<img src="https://github.com/FYP-19/IoT/assets/75986133/3cce3e50-2393-4969-a2b9-c611c6560571" alt="image (2)" width="500"/>

## Embedded Devices

| Requirement                | IoT Device                                |
|-------------------------|----------------------------------------------|
| Microcontroller    | Raspberry Pi 3B+            |
| Triggering Switch   |  Micro Switch V-1521C25  |
| Camera Module        |  Raspberry Pi NoIR v2 camera board |
| Communication Model        |  LoRa Ra-02 SX1278 |
| Antenna        |  RF 433MHz Antenna 2-3 dBi   |

## Useful Linux Commands 

| Function                | Linux Command                                |
|-------------------------|----------------------------------------------|
| Check camera status    | vcgencmd get_camera            |
| Real time camera feed   | raspivid -t 0            |
| Capture an image        |  raspistill -o <image_name>.jpg |
| Watch the image        |  eog <image_name>.jpg |
