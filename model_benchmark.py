import tflite_runtime.interpreter as tflite
import numpy as np
from PIL import Image
import time
import subprocess
from datetime import datetime
from collections import Counter
import resource

model = 'TF8_MobilenetV2_Stripped_Pruned_TFLITE.tflite'
model_path = '/home/fyp/fyp-19/models/'+ model
# model_path = '/home/fyp/fyp-19/models/MobilenetV2_QAT_FUll.tflite'

interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

inference_times = []
memory_usages = []
sample_count = 599
# Load and preprocess the image
for i in range(sample_count):
    image_path = f"/home/fyp/fyp-19/images/all_test/test_image_{i+1}.jpg"

    # New code for preprocessing
    original_image = Image.open(image_path)
    new_size = (224, 224)
    resized_image = original_image.resize(new_size)
    input_data = np.array(resized_image, dtype=np.float32)
    input_data = np.expand_dims(input_data, axis=0)
    # End of preprocessing code
    
    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Get memory usage before inference
    memory_usage_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
   
    startTime = time.time()
    # Run inference
    interpreter.invoke()
    endTime = time.time()

    inference_time = endTime - startTime
    inference_times.append(inference_time)

    # Get memory usage after inference
    memory_usage_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    memory_usage = memory_usage_after - memory_usage_before
    memory_usages.append(memory_usage)

    print(f"Sample {i} Classified -inf_time: {inference_time}  -mem_usage: {memory_usage}")

# Calculate average memory usage
average_memory_usage = np.mean(memory_usages)


print(f"========== Number of samples {sample_count} ==========")
average_inference_time = np.mean(inference_times)
print(model)
print("Average Inference Time:", average_inference_time)
print("Average Memory Usage:", average_memory_usage, "KB")
