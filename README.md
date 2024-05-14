# IoT part of the project 🌐🚀

In this project we deploy several deep learning models on the Raspberry Pi 3B+ SBC and measure the inference time of the each model. These DL models are trained to classify animal images with high accurcy. Once the classification process done, communication system responsible for transfer the classification result from the transmitter to the receiver. 

### Circuit Diagram of the project
<img src="https://github.com/FYP-19/IoT/assets/75986133/3cce3e50-2393-4969-a2b9-c611c6560571" alt="image (2)" width="500"/>

### High level circuit diagram for the circuit [Raspberry Pi 3B+ and LoRa Ra-02 SX1278 module]
<img src="https://github.com/FYP-19/IoT/assets/75986133/417c7dd5-e3dc-4637-9271-48e73c0b4da8" alt="image (3)" width="600">

## Used IoT Devices

| Requirement                | IoT Device                                |
|-------------------------|----------------------------------------------|
| Microcontroller    | Raspberry Pi 3B+            |
| Triggering Switch   |  Micro Switch V-1521C25  |
| Camera Module        |  Raspberry Pi NoIR v2 camera board |
| Communication Model        |  LoRa Ra-02 SX1278 |
| Antenna        |  RF 433MHz Antenna 2-3 dBi   |

## Essential Linux Commands 

| Function                | Linux Command                                |
|-------------------------|----------------------------------------------|
| Check camera status    | vcgencmd get_camera            |
| Real time camera feed   | raspivid -t 0            |
| Capture an image        |  raspistill -o <image_name>.jpg |
| Watch the image        |  eog <image_name>.jpg |
