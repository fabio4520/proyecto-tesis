import cv2
import mediapipe as mp
import copy
from math import sqrt
# from pyfirmata import Arduino, util, SERVO
from functions import *

# port = 'COM4' # Cambiar el puerto COM por el que corresponda
# board = Arduino(port)
# board.digital[9].mode = SERVO

maximum_distances_to_wrist = {
    "thumb": {
        "max": 0.7,
        "min": 0.56
    },
    "index": {
        "max": 1.06,
        "min": 0.58
    },
    "middle": {
        "max": 1.17,
        "min": 0.82
    },
    "ring": {
        "max": 1.10,
        "min": 0.58
    },
    "pinky": {
        "max": 0.93,
        "min": 0.56
    }
}

def main():
    # rotateservo(9, 0, board)

    # Initialize MediaPipe Hands module
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
    )
    cap = cv2.VideoCapture(0)


    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
    
        frame = cv2.flip(frame, 1)  # Flip the image horizontally
        debug_image = copy.deepcopy(frame) # Create a copy of the image
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert the image to RGB

        # Process the image
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
                # for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                #                                   results.multi_handedness):
                    hand_landmarks = results.multi_hand_landmarks[0]
                    handedness = results.multi_handedness[0]

                    landmark_list = calculate_landmark_list(hand_landmarks)

                    wrist_x, wrist_y = landmark_list[0][0], landmark_list[0][1]
                    thumb_X, thumb_y = landmark_list[4][0], landmark_list[4][1]
                    thumb_ip_y = landmark_list[3][1] # auxiliar
                    index_x, index_y = landmark_list[8][0], landmark_list[8][1]
                    index_dip_y = landmark_list[7][1] # auxiliar
                    middle_x, middle_y = landmark_list[12][0], landmark_list[12][1]
                    middle_dip_y = landmark_list[11][1] # auxiliar
                    ring_x, ring_y = landmark_list[16][0], landmark_list[16][1]
                    ring_dip_y = landmark_list[15][1] # auxiliar
                    pinky_x, pinky_y = landmark_list[20][0], landmark_list[20][1]
                    pinky_dip_y = landmark_list[17][1] # auxiliar

                    # Calculate distances
                    distance_thumb_wrist = round(sqrt((thumb_X - wrist_x)**2 + (thumb_y - wrist_y)**2),4)
                    distance_index_wrist = round(sqrt((index_x - wrist_x)**2 + (index_y - wrist_y)**2),4)
                    distance_middle_wrist = round(sqrt((middle_x - wrist_x)**2 + (middle_y - wrist_y)**2),4)
                    distance_ring_wrist = round(sqrt((ring_x - wrist_x)**2 + (ring_y - wrist_y)**2),4)
                    distance_pinky_wrist = round(sqrt((pinky_x - wrist_x)**2 + (pinky_y - wrist_y)**2),4)

                    # print(f"[{distance_thumb_wrist}, {distance_index_wrist}, {distance_middle_wrist}, {distance_ring_wrist}, {distance_pinky_wrist}]")

                    # knowing that the hand is extended and coordenates starts at 0,0 at the top left corner
                    avg_distances = 0.0
                    distance_thumb_wrist_normalized = distance_thumb_wrist
                    distance_index_wrist_normalized = distance_index_wrist
                    distance_middle_wrist_normalized = distance_middle_wrist
                    distance_ring_wrist_normalized = distance_ring_wrist
                    distance_pinky_wrist_normalized = distance_pinky_wrist

                    if thumb_ip_y > thumb_y and index_dip_y > index_y and middle_dip_y > middle_y and ring_dip_y > ring_y and pinky_dip_y > pinky_y:
                        avg_distances = (distance_thumb_wrist + distance_index_wrist + distance_middle_wrist + distance_ring_wrist + distance_pinky_wrist) / 5
                        distance_thumb_wrist_normalized = round(distance_thumb_wrist / avg_distances, 4)
                        distance_index_wrist_normalized = round(distance_index_wrist / avg_distances, 4)
                        distance_middle_wrist_normalized = round(distance_middle_wrist / avg_distances, 4)
                        distance_ring_wrist_normalized = round(distance_ring_wrist / avg_distances, 4)
                        distance_pinky_wrist_normalized = round(distance_pinky_wrist / avg_distances, 4)

                    
                    # print(f"[{distance_thumb_wrist_normalized}, {distance_index_wrist_normalized}, {distance_middle_wrist_normalized}, {distance_ring_wrist_normalized}, {distance_pinky_wrist_normalized}]")

                    if maximum_distances_to_wrist["thumb"]["min"] < distance_thumb_wrist_normalized < maximum_distances_to_wrist["thumb"]["max"]:
                        # normalize values to 0-1 range
                        # when distance is maximum, value is 0 and servomotor is at 0 degrees
                        # when distance is minimum, value is 1 and servomotor is at 180 degrees
                        distance_thumb_wrist_servo = round((distance_thumb_wrist_normalized - maximum_distances_to_wrist["thumb"]["max"]) / (maximum_distances_to_wrist["thumb"]["min"] - maximum_distances_to_wrist["thumb"]["max"]), 4)
                        angle_thumb = round(distance_thumb_wrist_servo * 180)
                        # print(f"angle_thumb: {angle_thumb}")
                        # rotateservo(9, angle_thumb, board)

                    elif maximum_distances_to_wrist["index"]["min"] < distance_index_wrist_normalized < maximum_distances_to_wrist["index"]["max"]:
                        distance_index_wrist_servo = round((distance_index_wrist_normalized - maximum_distances_to_wrist["index"]["max"]) / (maximum_distances_to_wrist["index"]["min"] - maximum_distances_to_wrist["index"]["max"]), 4)
                        angle_index = round(distance_index_wrist_servo * 180)
                        # print(f"angle_index: {angle_index}")
                        # rotateservo(9, angle_index, board)
                    
                    elif maximum_distances_to_wrist["middle"]["min"] < distance_middle_wrist_normalized < maximum_distances_to_wrist["middle"]["max"]:
                        distance_middle_wrist_servo = round((distance_middle_wrist_normalized - maximum_distances_to_wrist["middle"]["max"]) / (maximum_distances_to_wrist["middle"]["min"] - maximum_distances_to_wrist["middle"]["max"]), 4)
                        angle_middle = round(distance_middle_wrist_servo * 180)
                        # print(f"angle_middle: {angle_middle}")
                        # rotateservo(9, angle_middle, board)

                    elif maximum_distances_to_wrist["ring"]["min"] < distance_ring_wrist_normalized < maximum_distances_to_wrist["ring"]["max"]:
                        distance_ring_wrist_servo = round((distance_ring_wrist_normalized - maximum_distances_to_wrist["ring"]["max"]) / (maximum_distances_to_wrist["ring"]["min"] - maximum_distances_to_wrist["ring"]["max"]), 4)
                        angle_ring = round(distance_ring_wrist_servo * 180)
                        # print(f"angle_ring: {angle_ring}")
                        # rotateservo(9, angle_ring, board)

                    elif maximum_distances_to_wrist["pinky"]["min"] < distance_pinky_wrist_normalized < maximum_distances_to_wrist["pinky"]["max"]:
                        distance_pinky_wrist_servo = round((distance_pinky_wrist_normalized - maximum_distances_to_wrist["pinky"]["max"]) / (maximum_distances_to_wrist["pinky"]["min"] - maximum_distances_to_wrist["pinky"]["max"]), 4)
                        angle_pinky = round(distance_pinky_wrist_servo * 180)
                        # print(f"angle_pinky: {angle_pinky}")
                        # rotateservo(9, angle_pinky, board)

                    # Drawing section
                    brect = calc_bounding_rect(debug_image, hand_landmarks)
                    debug_image = draw_bounding_rect(debug_image, brect)
                    debug_image = draw_info_text(
                        debug_image,
                        frame,
                        brect,
                        handedness,
                        hand_landmarks,
                        wrist_x,
                        wrist_y
                    )
                    

        cv2.imshow('Hand Tracking', debug_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
