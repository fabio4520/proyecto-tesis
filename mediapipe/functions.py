from time import sleep
import numpy as np
import cv2

def rotateservo(pin, angle, board):
    board.digital[pin].write(angle)
    sleep(0.02)

def calculate_landmark_list(hand_landmarks):
        return [[round(landmark.x, 4), round(landmark.y, 4)] for landmark in hand_landmarks.landmark]

### Drawing section
def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv2.boundingRect(landmark_array)

    return [x, y, x + w, y + h]

def draw_bounding_rect(image, brect):
    # Outer rectangle
    cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                  (0, 0, 0), 1)

    return image

def draw_info_text(image, frame, brect, handedness, hand_landmarks,wrist_x,wrist_y):
    
    cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                 (0, 0, 0), -1)

    info_text = handedness.classification[0].label[0:]
    cv2.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    for i, landmark in enumerate(hand_landmarks.landmark):
      # Draw a circle in the points of interest
      if i in [0, 4, 8, 12, 16, 20]:
          # Draw a circle in the points of interest
          cv2.circle(image, (round(landmark.x * frame.shape[1]), round(landmark.y * frame.shape[0])), 5, (0, 0, 255), -1)
          # Draw the index of the point of interest
          cv2.putText(image, f'{i}: ({round(landmark.x * frame.shape[1])},{round(landmark.y * frame.shape[0])})', (round(landmark.x * frame.shape[1]), round(landmark.y * frame.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
          # Draw a line between the points and the wrist
          cv2.line(image, (round(landmark.x * frame.shape[1]), round(landmark.y * frame.shape[0])), (round(wrist_x * frame.shape[1]), round(wrist_y * frame.shape[0])), (0, 255, 0), 2)
          # Draw if hand is left or right
    return image