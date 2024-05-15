from time import sleep
import sys
from SX127x.LoRa import *
from SX127x.board_config import BOARD
import RPi.GPIO as GPIO
from datetime import datetime
import subprocess
GPIO.setwarnings(False)  # Disable GPIO warnings

BOARD.setup()

class LoRaRcvCont(LoRa):

    def print_output(animal_id):
        labels_path = '/home/fyp/fyp-19/scripts/labels.txt'
        with open(labels_path,'r') as f:
            labels = f.read().splitlines()
        
        predicted_label = labels[animal_id]
        print("Predicted Animal Label: " + predicted_label)
 

    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.STDBY)  # Set mode to STDBY initially
        self.set_dio_mapping([0] * 6)
        print("============ Receiver Started ============")
        # Perform mode check here before calibration
        if self.mode not in [MODE.SLEEP, MODE.STDBY, MODE.FSK_STDBY]:
            self.set_mode(MODE.STDBY)  # Set mode to STDBY if not in the required modes

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(0.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()

    #Execute once data is received
    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        
        labels_path = '/home/fyp/fyp-19/scripts/labels.txt'
        with open(labels_path,'r') as f:
            labels = f.read().splitlines()
        try:
            cage_ID = str(payload[0])
            cat_ID = str(payload[1])
            Accuracy = str(payload[2])

            current_date = datetime.now()
            print("Message Received at: " + current_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
            print(f"Cage ID: {cage_ID}")
            print(f"Category ID: {cat_ID}")
            print(f"Accuracy: {Accuracy}")
            predicted_label = labels[payload[1]]
            print("Predicted Animal Label: " + predicted_label)

            print(f"Data Received Sucessfully! \n")

            #Upload data to firebase database
            subprocess.run(["python","DB_manager.py",str(cage_ID), str(Accuracy), str(predicted_label)])
        
        except Exception as e:
            print("Something went wrong!")

        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)


lora = LoRaRcvCont(verbose=False)
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(spreading_factor=12)

try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
