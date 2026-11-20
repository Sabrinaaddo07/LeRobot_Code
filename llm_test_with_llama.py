
from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
import time
import ollama

#asks llm right left up or down
# Asks LLM to choose a movement
#create a loop for the API key to see multiple times promtping and see trend 
def ask_llm():
    response = ollama.chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "system",
                "content": """
                You are controlling a robotic arm.

                Choose ONE movement:
                1 = UP
                2 = DOWN
                3 = RIGHT
                4 = LEFT

                Respond with ONLY the number corresponding to your choice.
                """
            }
        ]
    )

    answer = response.message.content.strip()

    # Extract the number from the response
    for character in answer:
        if character in ["1", "2", "3", "4"]:
            return int(character)

    raise ValueError(f"Invalid LLM response: {answer}")

#moves arm up
def move_up():

    up_positions = {
        "shoulder_pan": 1958,
        "shoulder_lift": 1395,
        "elbow_flex": 2170,
        "wrist_flex": 2070,
        "wrist_roll": 3237,
        "gripper": 2079
    }

    for motor, position in up_positions.items():

        robot.bus.write(
            "Goal_Position",
            motor,
            position,
            normalize=False
        )

    print("\nMoving robot to up position...")

# Moves robot arm down
def move_down():

    down_positions = {
        "shoulder_pan": 1957,
        "shoulder_lift": 1538,
        "elbow_flex": 2882,
        "wrist_flex": 2286,
        "wrist_roll": 3237,
        "gripper": 2074
    }

    for motor, position in down_positions.items():

        robot.bus.write(
            "Goal_Position",
            motor,
            position,
            normalize=False
        )

    print("\nMoving robot to down position...")

#Moves robot arm to the left position
def move_left():

    right_positions = {
        "shoulder_pan": 1340,
        "shoulder_lift": 1304,
        "elbow_flex": 2540,
        "wrist_flex": 2978,
        "wrist_roll": 3240,
        "gripper": 2073
    }

    for motor, position in right_positions.items():

        robot.bus.write(
            "Goal_Position",
            motor,
            position,
            normalize=False
        )

    print("\nMoving robot to right position...")

# Moves robot arm to the right position
def move_right():

    right_positions = {
        "shoulder_pan": 2582,
        "shoulder_lift": 1304,
        "elbow_flex": 2540,
        "wrist_flex": 2978,
        "wrist_roll": 3240,
        "gripper": 2073
    }

    for motor, position in right_positions.items():

        robot.bus.write(
            "Goal_Position",
            motor,
            position,
            normalize=False
        )

    print("\nMoving robot to right position...")

# a function to read and print all motor positions
def print_motor_positions():
    positions = robot.bus.sync_read(
        "Present_Position",
        motors=[
            "shoulder_pan",
            "shoulder_lift",
            "elbow_flex",
            "wrist_flex",
            "wrist_roll",
            "gripper"
        ],
        normalize=False
    )

    print("\nCurrent Motor Positions:")

    for motor, position in positions.items():
        print(f"{motor}: {position}")


def main():
    global robot

    config = SO101FollowerConfig(
        port="/dev/cu.usbmodem5B421378291",
        id="AlltheWayT",
    )

    robot = SO101Follower(config)

    try:
        robot.connect(calibrate=False)
        print("Follower connected!")

        for i in range(5):
            print(f"\nMovement {i + 1} of 5")

            decision = ask_llm()
            print("LLM decision:", decision)

            match decision:
                case 1:
                    move_up()
                case 2:
                    move_down()
                case 3:
                    move_right()
                case 4:
                    move_left()
                case _:
                    print("Invalid movement selection.")
                    continue

            time.sleep(2)
            print_motor_positions()

    finally:
        if robot.is_connected:
            robot.disconnect()
            print("\nFollower disconnected.")



if __name__ == "__main__":
    main()
