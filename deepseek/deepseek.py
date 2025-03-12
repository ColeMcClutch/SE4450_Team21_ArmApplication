import openai
import can_data
import struct
import re
import time
import speech_recognition as sr 

# Set up DeepSeek AI client
client = openai.OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:1234/v1"
)

# Predefined positions for special commands
PRESET_MOVEMENTS = {
    "home": [0, 0, 0, 0, 0, 0],  # Home position (All joints at 0°)
    "wave_hello": [
        [0, 45, 0, 90, 0, 0],  # Raise arm
        [0, 45, 0, -90, 0, 0],  # Move left
        [0, 45, 0, 90, 0, 0],  # Move right
        [0, 45, 0, -90, 0, 0],  # Move left
        [0, 0, 0, 0, 0, 0]  # Return to rest position
    ]
}

# Function to generate AI response
def generate_response(prompt):
    response = client.chat.completions.create(
        model="deepseek-r1",
        messages=[
            {"role": "system", "content": "You are a robotic control AI assistant. "
             "Always respond with six numerical joint values, separated by commas, including negative values where appropriate. "
             "Example: '-30, 45, 60, -20, 10, -5'. "
             "Recognize and respond correctly to high-level commands like 'Move to home position', 'Wave hello', or 'Stop movement'."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )
    return response.choices[0].message.content

# Function to process AI-generated commands
def process_ai_command(udp_client, command_text):
    command_text = command_text.lower().strip()  # Normalize input
    print(f"🔹 Received Command: {command_text}")

    # Handle special commands
    if "home" in command_text or "reset" in command_text:
        print("Moving to Home Position...")
        send_joint_positions(udp_client, PRESET_MOVEMENTS["home"])
        return "Robot moved to home position."

    elif "wave" in command_text:
        print("Performing Wave Hello...")
        for pose in PRESET_MOVEMENTS["wave_hello"]:
            send_joint_positions(udp_client, pose)
            time.sleep(1)  # Delay between movements
        return "Robot completed waving motion."

    elif "stop" in command_text or "halt" in command_text:
        print("Stopping all movement...")
        send_idle_mode(udp_client)  # Send IDLE mode command
        return "Robot stopped."

    # Extract numerical values for normal movement
    ai_response = generate_response(command_text)
    print(f"🔹 AI Response: {ai_response}")

    joint_values = re.findall(r'-?\d+\.\d+|-?\d+', ai_response)  
    joint_values = [float(x) for x in joint_values][:6]  

    print(f"🔹 Extracted joint values: {joint_values}")

    if len(joint_values) == 6:
        send_joint_positions(udp_client, joint_values)
        return f"Sent command to move joints: {joint_values}"
    else:
        return f"Error: AI response did not contain 6 valid joint positions. Extracted: {joint_values}"

# Function to send joint positions via UDP
def send_joint_positions(udp_client, joint_angles):
    for i, angle in enumerate(joint_angles):
        cid = i + 1  # Motor ID
        reduction_value = 50  
        motor_cnt = angle / 360.0 * reduction_value
        pos = struct.pack('<f', float(motor_cnt))
        cmd2 = struct.pack('<HH', 60, 10)
        # ...send to UDP client

# Function to set all motors to IDLE mode (stop movement)
def send_idle_mode(udp_client):
    for i in range(1, 7):
        udp_client.send_message(
            i,
            can_data.command_id['Set_Axis_State'],
            struct.pack('<I', can_data.AxisState['IDLE']),
            struct.pack('<I', 0),
            can_data.Message_type['short']
        )

# 🗣️ Voice Control Function
def voice_command(udp_client):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for voice command...")
        try:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            audio = recognizer.listen(source)  # Capture audio

            # Convert speech to text
            command_text = recognizer.recognize_google(audio)
            print(f"Recognized: {command_text}")  # Debugging output

            return process_ai_command(udp_client, command_text)

        except sr.UnknownValueError:
            return "Could not understand the voice command."
        except sr.RequestError:
            return "Speech Recognition service unavailable."
        
def smooth_movement(udp_client, start_position, end_position, steps=10):
    """Move smoothly from start to end position in multiple steps"""
    for i in range(steps + 1):
        t = i / steps  # Interpolation parameter (0 to 1)
        # Linear interpolation between positions
        current_position = [start + (end - start) * t for start, end in zip(start_position, end_position)]
        send_joint_positions(udp_client, current_position)
        time.sleep(0.05)  # Small delay between steps
