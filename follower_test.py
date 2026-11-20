
from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
import time

# a function to read and print all motor positions
#GIT CHANGE
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


#moves robot to home position

def move_to_home():

    home_positions = {
        "shoulder_pan": 1960,
        "shoulder_lift": 856,
        "elbow_flex": 3088,
        "wrist_flex": 2879,
        "wrist_roll": 3231,
        "gripper": 2068
    }

    for motor, position in home_positions.items():

        robot.bus.write(
            "Goal_Position",
            motor,
            position,
            normalize=False
        )

    print("\nMoving robot to home position...")



def main():
    global robot
    # Configure the robot
    config = SO101FollowerConfig(
        port="/dev/cu.usbmodem5B421378291",
        id="AlltheWayT",
    )

    robot = SO101Follower(config)

    # Connect and run
    try:
        robot.connect(calibrate=False)
        print("Follower connected!")

        print_motor_positions()
        time.sleep(3)



    finally:
        if robot.is_connected:
            robot.disconnect()
            print("\nFollower disconnected.")


if __name__ == "__main__":
    main()




