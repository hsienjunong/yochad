from langchain_core.tools import tool
from openai import OpenAI

import time
import socket
import components.initializer as init

client = OpenAI()

host = init.HOST
port = int(init.PORT)

workspace_limits = {
    "reach_radius": 0.5,  # Maximum reach in meters
    "joint_limits": {
        "base": [-6.28, 6.28],       # J1 in radians
        "shoulder": [-3.14, 3.14],   # J2 in radians
        "elbow": [-3.14, 3.14],      # J3 in radians
        "wrist1": [-6.28, 6.28],     # J4 in radians
        "wrist2": [-6.28, 6.28],     # J5 in radians
        "wrist3": [-6.28, 6.28]      # J6 in radians
    }
}

home_position = [0.0, -1.5708, 0.0, -1.5708, 0.0, 0.0]

@tool
def send_command_to_robot(ur_script_command):
    """
    Sends a URScript command to the robot.

    Description:
        This tool sends a URScript command to the robot by establishing a socket
        connection directly within the function. The command is formatted and transmitted
        to the robot, ensuring it is executed as expected. Use this tool to control or 
        send instructions to the robot.

    Args:
        ur_script_command (str): The URScript command to be sent to the robot. 
                                 This should be a valid URScript command string.

    Returns:
        None
    """
    try:
        # Remove any code fences or extra whitespace
        ur_script_command = ur_script_command.strip('`').strip()

        # Print the command being sent
        print(f"Sending URScript command:\n{ur_script_command}")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            # Ensure the command ends with a newline character
            if not ur_script_command.endswith('\n'):
                ur_script_command += '\n'

            # Send the URScript command
            s.sendall(ur_script_command.encode('utf-8'))
        
            # Wait for the robot to process the command
            time.sleep(0.5)

    except Exception as e:
        print(f"Error sending command to robot: {e}")

@tool
def generate_urscript(user_command):
    """
    Generates URScript commands from a user's natural language input.

    Description:
        This tool uses the OpenAI API to convert natural language commands 
        into URScript commands for controlling a UR3e robot. The tool ensures 
        that generated commands adhere to predefined rules for safety and accuracy 
        within the robot's operational boundaries.

    Args:
        user_command (str): The natural language command to be interpreted 
                            into URScript code.

    Returns:
        str: The generated URScript command or a message indicating that the 
             movement is not possible due to workspace limitations.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are a robotic control assistant specialized in converting human language instructions into URScript commands for a UR3e robot.\n"
                "Follow these steps for every command:\n"
                "1. Retrieve the robot's current position using the URScript command `get_actual_joint_positions()`.\n"
                "   - Use the retrieved joint positions as the starting point for all calculations.\n"
                "2. Analyze the user's intent and break it down into specific joint movements relative to the current position.\n"
                "   - If the user specifies a movement direction (e.g., 'move up', 'move forward') without a distance, assume a default distance of 0.1 meters.\n"
                "3. Translate the intent into robot terms by calculating the necessary joint angle adjustments for the movement.\n"
                "   - For example, if the user asks to move left by 300 degrees (converted to radians), you must calculate the corresponding joint movement.\n"
                "4. Ensure that the URScript command is generated as a single line. The robot software only understands commands written in one line.\n"
                "   - For example, instead of:\n"
                "       `current_joint_positions = get_actual_joint_positions()`\n"
                "       `movej([current_joint_positions[0] + 300 * (3.14159 / 180), ...])`\n"
                "     You must generate:\n"
                "       `movej([get_actual_joint_positions()[0] + 300 * (3.14159 / 180), get_actual_joint_positions()[1], get_actual_joint_positions()[2], get_actual_joint_positions()[3], get_actual_joint_positions()[4], get_actual_joint_positions()[5]], a=1.0, v=0.5)`\n"
                "5. Always use `movej` for all movements. You must never use `movel` or any other motion commands.\n"
                "6. Ensure the movement respects the robot's workspace limits (joint limits, reach radius).\n"
                "7. If the requested movement is still not feasible after calculations, explain why.\n\n"
                "Examples of using `movej` as a single-line command:\n"
                "- Example 1: Rotate the base joint (J1) by 300 degrees (converted to radians) from its current position:\n"
                "  `movej([get_actual_joint_positions()[0] + 300 * (3.14159 / 180), get_actual_joint_positions()[1], get_actual_joint_positions()[2], get_actual_joint_positions()[3], get_actual_joint_positions()[4], get_actual_joint_positions()[5]], a=1.0, v=0.5)`\n"
                "- Example 2: Move up by 0.1 meters relative to the current position:\n"
                "  Assume this involves adjusting J2. You must calculate the adjustment and generate:\n"
                "  `movej([get_actual_joint_positions()[0], get_actual_joint_positions()[1] + calculated_offset, get_actual_joint_positions()[2], get_actual_joint_positions()[3], get_actual_joint_positions()[4], get_actual_joint_positions()[5]], a=1.2, v=0.8)`\n"
                "- Example 3: Return to the home position:\n"
                "  `movej([0.0, -1.5708, 0.0, -1.5708, 0.0, 0.0], a=1.0, v=0.5)`\n\n"
                "The home position of the robot is [0.0, -1.5708, 0.0, -1.5708, 0.0, 0.0].\n\n"
                "For multi-step trajectories, generate sequential single-line `movej` commands relative to the robot's position at each step. "
                "Retrieve the current position dynamically within each command to ensure accuracy.\n\n"
                "If the user provides an ambiguous command (e.g., 'move up'), always calculate the movement relative to the current position. "
                "Provide only the URScript code unless movement is not possible."
            )
        },
        {
            "role": "user",
            "content": f"Convert the following command into URScript:\n\n{user_command}"
        }
    ]

    try:
        completion = client.chat.completions.create(
            model=init.DEFAULT_CHAT_MODEL,
            messages=messages,
            max_tokens=150,
            temperature=0
        )

        ur_script_command = completion.choices[0].message.content.strip()
        # Remove any code fences or markdown syntax
        ur_script_command = ur_script_command.strip('').strip()
        return ur_script_command
    except Exception as e:
        print(f"Error interpreting command: {e}")
        return None
