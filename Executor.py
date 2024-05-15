import RPi.GPIO as GPIO
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite
import time
import subprocess
from datetime import datetime
from collections import Counter
import threading

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin for the switch
switch_pin = 23
# Set up GPIO pin as input with pull-up resistor
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to run the script when the switch is pressed
def switch_callback(channel):
    current_time = datetime.now()
    print("Switch pressed at: " + current_time.strftime("%Y-%m-%d %H:%M:%S:%f")[:-3])

    capture_thread = threading.Thread(target=capture_Images)
    capture_thread.start()
        
    # classify_Images()    

def capture_Images():
    image_directory = "/home/fyp/fyp-19/images/captured"
    
    print(f"Captured images saved on: {image_directory}")

    num_of_images = 3
    for i in range (num_of_images):
        image_filename = f"cap_image_{i}.jpg"
        image_pathname = f"{image_directory}/{image_filename}"
        subprocess.run(["raspistill", "-o", image_pathname])
        print(f"Image {i+1} captured: {image_filename}")

    classify_Images()
     

def classify_Images():
    # Load the TensorFlow Lite model
    #Change the model path with the model
    model_path = '/home/fyp/fyp-19/models/Compressed_MobilenetV2_stripped_clustered_model.tflite'
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    #store images
    stored_classification_Results_map = {}

    # Load and preprocess the image
    num_of_images_to_classify = 3
    for i in range(num_of_images_to_classify):
        image_path = f"/home/fyp/fyp-19/images/captured_test/cap_image_{i}.jpeg"  # Update with your image path
        # image = Image.open(image_path).resize((input_details[0]['shape'][1], input_details[0]['shape'][2]))
        # input_data = np.expand_dims(image, axis=0)
        # input_data = (np.float32(input_data) - 127.5) / 127.5  # Normalize the input

        # New code for preprocessing
        original_image = Image.open(image_path)
        new_size = (224, 224)
        resized_image = original_image.resize(new_size)

        # Convert the resized image to a numpy array of dtype float32
        input_data = np.array(resized_image, dtype=np.float32)

        # Scale the pixel values to be between -1 and 1
        input_data = (input_data / 127.5) - 1.0

        # Add a batch dimension
        input_data = np.expand_dims(input_data, axis=0)
        # End of preprocessing code

        # Set the input tensor
        interpreter.set_tensor(input_details[0]['index'], input_data)

        # Run inference
        interpreter.invoke()

        # Get the output tensor
        output_data = interpreter.get_tensor(output_details[0]['index'])
        max_classification_result = max(output_data[0])

        print(f"max_classification_result {max_classification_result}")
        decoded_predictions = np.argmax(output_data, axis=1)
        classification_id = int(decoded_predictions[0])
        print(f"classification_id {classification_id} \n")

        # store the classification result for each image in a dictionry. 
        if classification_id in stored_classification_Results_map:
            stored_classification_Results_map[classification_id].append(max_classification_result)
        else:
            stored_classification_Results_map[classification_id] = [max_classification_result]

    max_value_count = 0

    #Calculate the final classification result
    for key, value in stored_classification_Results_map.items():
        if len(value) > max_value_count:
            max_value_count = len(value)

    max_valued_keys = [key for key in stored_classification_Results_map if len(stored_classification_Results_map[key]) >= max_value_count]

    new_dic_max_valued_key_map = {key: max(stored_classification_Results_map.get(key)) for key in max_valued_keys}

    max_key, max_value = max(new_dic_max_valued_key_map.items(), key=lambda x: x[1])

    accuracy = round(float(max_value)*100)
    final_classification_id = max_key

    # Set the threshold accuracy
    threshold_accuracy = 75
    
    if(accuracy < threshold_accuracy):
        #set the animal type as unidentified.
        final_classification_id = 6

    # Load labels
    labels_path = '/home/fyp/fyp-19/scripts/labels.txt' 
    with open(labels_path, 'r') as f:
        labels = f.read().splitlines()

    # Process the output to get predictions
    predicted_label = labels[final_classification_id]

    print("-----------------------------------")
    print(f"Animal Id - {final_classification_id}")
    print(f"Accuracy - {accuracy}")
    print(f"Predicted Animal Label - {predicted_label}")
    print("-----------------------------------")

    #Transmit Results
    send_results(final_classification_id, accuracy)

# Load results to the Transmitter
def send_results(animal_id, accuracy, cage_id=12 ):
    subprocess.run(["python", "Transmitter.py", str(cage_id), str(animal_id), str(accuracy)])

# Add event detection for the falling edge (switch press)
GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback=switch_callback, bouncetime=10000)

try:
    print("============ Waitng for switch trigger event ============")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
