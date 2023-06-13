import onnx
import onnxruntime
import numpy as np
import random

cameraMovementXAxis = [0.01, 0, -0.01]
cameraMovementYAxis = [-0.05, 0, 0.05]
x1Avg = 0
y1Avg = 1
x2Avg = 0.9
y2Avg = 0.9

model = onnx.load("./eyesModel.onnx")

session = onnxruntime.InferenceSession(model.SerializeToString())

input_name = session.get_inputs()[0].name
input_shape = session.get_inputs()[0].shape

batch_size = 1
obs_0_shape = (batch_size, 2)
obs_0_data = np.array([0, 1], dtype=np.float32)
obs_0_data = obs_0_data.reshape(obs_0_shape)

"""
X - Cam01                   X - Motor01
0 - right                   0 - left
1 - no movement             1 - no movement
2 - left                    2 - right

Y - Cam01                   Y - Motor01
0 - down                    0 - up
1 - no movement             1 - no movement
2 - up                      2 - down

X - Cam02                   X - Motor02
0 - right                   0 - left
1 - no movement             1 - no movement
2 - left                    2 - right

Y - Cam02                   Y - Motor02
0 - down                    0 - up
1 - no movement             1 - no movement
2 - up                      2 - down


top - right : 1,1,1,1 - X1,Y1,X2,Y2
movement : 0,2,0,2 - Y1,X1,Y2,X2

bottom - right : 1,0,1,0 - X1,Y1,X2,Y2
movement : 2,2,2,2 - Y1,X1,Y2,X2

bottom - left : 0,0,0,0 - X1,Y1,X2,Y2
movement : 2,0,2,0 - Y1,X1,Y2,X2

top - left : 0,1,0,1 - X1,Y1,X2,Y2
movement : 0,0,0,0 - Y1,X1,Y2,X2

"""

obs_1_shape = (batch_size, 6)
obs_1_data = np.array(
    [
        x1Avg,
        y1Avg,
        0,
        -1,
        -1,
        random.choice([-1, 0, 1]),
    ],
    dtype=np.float32,
)
obs_1_data = obs_1_data.reshape(obs_1_shape)


action_masks_shape = (batch_size, 12)
action_masks_data = np.array(
    [
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
    ],
    dtype=np.float32,
)
action_masks_data = action_masks_data.reshape(action_masks_shape)

loopNumber = 0

while True:
    loopNumber += 1

    input_data = {
        "obs_0": obs_0_data,
        "obs_1": obs_1_data,
        "action_masks": action_masks_data,
    }

    output = session.run(
        ["deterministic_discrete_actions"],
        input_data,
    )

    Y1, X1, Y2, X2 = output[0][0]

    # Camera parsing for movement
    # Camera01
    if obs_1_data[0][0] + cameraMovementXAxis[X1] > 1:
        if obs_1_data[0][0] != -1:
            obs_1_data[0][0] = 1
        x1Avg = (x1Avg * loopNumber + 1) / (loopNumber + 1)
    elif obs_1_data[0][0] + cameraMovementXAxis[X1] < 0:
        if obs_1_data[0][0] != -1:
            obs_1_data[0][0] = 0
        x1Avg = (x1Avg * loopNumber + 0) / (loopNumber + 1)
    else:
        if obs_1_data[0][0] != -1:
            obs_1_data[0][0] = obs_1_data[0][0] + cameraMovementXAxis[X1]
        x1Avg = (x1Avg * loopNumber + obs_1_data[0][0]) / (loopNumber + 1)

    if obs_1_data[0][1] + cameraMovementYAxis[Y1] > 1:
        if obs_1_data[0][1] != -1:
            obs_1_data[0][1] = 1
        y1Avg = (y1Avg * loopNumber + 1) / (loopNumber + 1)
    elif obs_1_data[0][1] + cameraMovementYAxis[Y1] < 0:
        if obs_1_data[0][1] != -1:
            obs_1_data[0][1] = 0
        y1Avg = (y1Avg * loopNumber + 0) / (loopNumber + 1)
    else:
        if obs_1_data[0][1] != -1:
            obs_1_data[0][1] += cameraMovementYAxis[Y1]
        y1Avg = (y1Avg * loopNumber + obs_1_data[0][1]) / (loopNumber + 1)

    # Camera 02
    if obs_1_data[0][3] + cameraMovementXAxis[X2] > 1:
        if obs_1_data[0][3] != -1:
            obs_1_data[0][3] = 1
        x2Avg = (x2Avg * loopNumber + 1) / (loopNumber + 1)
    elif obs_1_data[0][3] + cameraMovementXAxis[X2] < 0:
        if obs_1_data[0][3] != -1:
            obs_1_data[0][3] = 0
        x2Avg = (x2Avg * loopNumber + 0) / (loopNumber + 1)
    else:
        if obs_1_data[0][3] != -1:
            obs_1_data[0][3] += cameraMovementXAxis[X2]
        x2Avg = (x2Avg * loopNumber + obs_1_data[0][3]) / (loopNumber + 1)

    if obs_1_data[0][4] + cameraMovementYAxis[Y2] > 1:
        if obs_1_data[0][4] != -1:
            obs_1_data[0][4] = 1
        y2Avg = (y2Avg * loopNumber + 1) / (loopNumber + 1)
    elif obs_1_data[0][4] + cameraMovementYAxis[Y2] < 0:
        if obs_1_data[0][4] != -1:
            obs_1_data[0][4] = 0
        y2Avg = (y2Avg * loopNumber + 0) / (loopNumber + 1)
    else:
        if obs_1_data[0][4] != -1:
            obs_1_data[0][4] += cameraMovementYAxis[Y2]
        y2Avg = (y2Avg * loopNumber + obs_1_data[0][4]) / (loopNumber + 1)

    if obs_0_data[0][0] == 1:
        obs_1_data[0][2] = random.choice([-1, 0, 1])

    if obs_0_data[0][1] == 1:
        obs_1_data[0][5] = random.choice([-1, 0, 1])

    print(
        f"[{Y1} {X1} {Y2} {X2}]({X1}{Y1})\t\t[X1: {str(obs_1_data[0][0])[:4]} \tX1Avg: {str(x1Avg)[:4]}],\t\t[Y1: {str(obs_1_data[0][1])[:4]} \tY1Avg: {str(y1Avg)[:4]}],\t\t[X2: {str(obs_1_data[0][3])[:4]} \tX2Avg: {str(x2Avg)[:4]}],\t\t[Y2: {str(obs_1_data[0][4])[:4]} \tY2Avg: {str(y2Avg)[:4]}]"
    )

    if loopNumber >= 1:
        break
