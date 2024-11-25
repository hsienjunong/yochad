import conversation_handler as convo
from components.connection import initialize_robot

import tools.commands as commands

if __name__ == "__main__":
    # initialize the robot
    robot, socket_connection = initialize_robot()
    if robot and socket_connection:
        print("Robot and socket connection are successfully initialized.")
    else:
        print("Failed to initialize robot or socket connection.")
    # start the agent chatbot 
    print("Welcome to the UR Agent Chatbot! Type 'exit' to quit.")
    while True:

        # commands.send_command_to_robot("current_joint_positions = get_actual_joint_positions()")
        # commands.send_command_to_robot("movej([get_actual_joint_positions()[0] + 300 * (3.14159 / 180), get_actual_joint_positions()[1], get_actual_joint_positions()[2], get_actual_joint_positions()[3], get_actual_joint_positions()[4], get_actual_joint_positions()[5]], a=1.0, v=0.5)")

        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = convo.handle_conversation(user_input)
        print(f"Agent: {response}")
