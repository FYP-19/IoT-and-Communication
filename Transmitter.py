from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
import RPi.GPIO as GPIO
import sys

GPIO.setwarnings(False)  # Disable GPIO warnings

BOARD.setup()


class LoRaTransmitter(LoRa):

    def __init__(self, verbose=False):
        super(LoRaTransmitter, self).__init__(verbose)
        self.set_mode(MODE.STDBY)  # Set mode to STDBY initially
        self.set_dio_mapping([0] * 6)

    def send_packet(self, data):
        self.set_mode(MODE.STDBY)
        sleep(0.1)
        self.write_payload(data)
        self.set_mode(MODE.TX)
        while (self.get_irq_flags()['tx_done'] == 0):
            sleep(0.1)
        # self.clear_irq_flags()
        self.set_mode(MODE.STDBY)
    
    def on_tx_done(self):
        print("\nSend: ")
        self.clear_irq_flags(TxDone=1)
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()

cage_id = int(sys.argv[1])
animal_id = int(sys.argv[2])
accuracy = int(sys.argv[3])

lora = LoRaTransmitter(verbose=False)
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(spreading_factor = 12)

try:
    data = [cage_id,animal_id,accuracy]
    lora.send_packet(data)
    print("Data Transmitted Sucessfully!")
    sleep(5)

except KeyboardInterrupt:
    print("Keyboard Interrupt")

finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
