import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Function to open and display images based on a given prompt
def open_images(prompt):
    folder_path = r"Data"  # Folder where the images are stored
    prompt = prompt.replace(" ", "_")  # Replace spaces in prompt with underscores
    
    # Generate the filenames for the images
    files = [f"{prompt}[{i}].jpg" for i in range(1, 5)]
    
    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            # Try to open and display the image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)  # Pause for 1 second before showing the next image
        except IOError:
            print(f"Unable to open {image_path}")

# API details for the Hugging Face Stable Diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# Async function to send a query to the Hugging Face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []
    print(f"Generating images for prompt: {prompt}")
    
    # Create 4 image generation tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(9, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)
    
    # Wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks)
    print("Received image bytes")
    
    # Save the generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        file_path = fr"Data\{prompt.replace(' ', '_')}[{i + 1}].jpg"
        with open(file_path, "wb") as f:
            f.write(image_bytes)
            print(f"Saved {file_path}")

# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))  # Run the async image generation
    open_images(prompt)  # Open the generated images

# MAIN LOOP
print("Image generation service started. Waiting for requests...")

try:
    while True:
        try:
            with open(r"Frontend/Files/ImageGeneration.data", "r") as f:
                data: str = f.read().strip()
                print(f"Read data: '{data}'")
            
            if not data or "," not in data:
                print("Invalid data format. Waiting...")
                sleep(1)
                continue
            
            Prompt, status = data.split(",")
            Prompt = Prompt.strip()
            status = status.strip()
            
            print(f"Prompt: {Prompt}, Status: {status}")
            
            if status == "True":    
                print("Generating Images...")
                GenerateImages(prompt=Prompt)
                
                # Reset the status after processing the request
                with open(r"Frontend/Files/ImageGeneration.data", "w") as f:
                    f.write("False,False")
                print("Status reset. Waiting for next input.")
            elif status == "False" and Prompt == "False":
                # Exit the loop if the file contains "False,False" and the prompt is "False"
                print("Got termination signal. Exiting...")
                break
            else:
                print("No request. Sleeping.")
                sleep(1)

        except Exception as e:
            print(f"Error in loop: {e}")
            sleep(1)

except KeyboardInterrupt:
    print("\n🔴 Program terminated by user.")
