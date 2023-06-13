import onnx
import onnxruntime
import numpy as np
import random
from onvif import ONVIFCamera


# For model
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


def readInput():
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
    elif obs_1_data[0][0] + cameraMovementXAxis[X1] < 0:
        if obs_1_data[0][0] != -1:
            obs_1_data[0][0] = 0
    else:
        if obs_1_data[0][0] != -1:
            obs_1_data[0][0] = obs_1_data[0][0] + cameraMovementXAxis[X1]

    if obs_1_data[0][1] + cameraMovementYAxis[Y1] > 1:
        if obs_1_data[0][1] != -1:
            obs_1_data[0][1] = 1
    elif obs_1_data[0][1] + cameraMovementYAxis[Y1] < 0:
        if obs_1_data[0][1] != -1:
            obs_1_data[0][1] = 0
    else:
        if obs_1_data[0][1] != -1:
            obs_1_data[0][1] += cameraMovementYAxis[Y1]

    # Camera 02
    if obs_1_data[0][3] + cameraMovementXAxis[X2] > 1:
        if obs_1_data[0][3] != -1:
            obs_1_data[0][3] = 1
    elif obs_1_data[0][3] + cameraMovementXAxis[X2] < 0:
        if obs_1_data[0][3] != -1:
            obs_1_data[0][3] = 0
    else:
        if obs_1_data[0][3] != -1:
            obs_1_data[0][3] += cameraMovementXAxis[X2]

    if obs_1_data[0][4] + cameraMovementYAxis[Y2] > 1:
        if obs_1_data[0][4] != -1:
            obs_1_data[0][4] = 1
    elif obs_1_data[0][4] + cameraMovementYAxis[Y2] < 0:
        if obs_1_data[0][4] != -1:
            obs_1_data[0][4] = 0
    else:
        if obs_1_data[0][4] != -1:
            obs_1_data[0][4] += cameraMovementYAxis[Y2]

    if obs_0_data[0][0] == 1:
        obs_1_data[0][2] = random.choice([-1, 0, 1])

    if obs_0_data[0][1] == 1:
        obs_1_data[0][5] = random.choice([-1, 0, 1])

    return [X1 * 10 + Y1, X2 * 10 + Y2]


# For camera
IP = "192.168.101.21"  # Camera IP address
PORT = 8899  # Port
USER = "admin"  # Username
PASS = "Chame1eon"  # Password
WSDL_PATH = "/Users/JavierGonzales/Library/Python/3.9/lib/python3.9/site-packages/wsdl"


XMAX = 1
XMIN = -1
YMAX = 1
YMIN = -1
moverequest = None
ptz = None
active = False


def do_move(ptz, request):
    # Start continuous move
    global active
    if active:
        ptz.Stop({"ProfileToken": request.ProfileToken})
    active = True
    ptz.ContinuousMove(request)


def move_up(ptz, request):
    print(
        f"X1: {str(obs_1_data[0][0])[:4]},\t\tY1: {str(obs_1_data[0][1])[:4]} \t\tmove up..."
    )
    request.Velocity.PanTilt.x = 0
    request.Velocity.PanTilt.y = YMAX
    do_move(ptz, request)


def move_down(ptz, request):
    print(
        f"X1: {str(obs_1_data[0][0])[:4]},\t\tY1: {str(obs_1_data[0][1])[:4]} \t\tmove down..."
    )
    request.Velocity.PanTilt.x = 0
    request.Velocity.PanTilt.y = YMIN
    do_move(ptz, request)


def move_right(ptz, request):
    print(
        f"X1: {str(obs_1_data[0][0])[:4]},\t\tY1: {str(obs_1_data[0][1])[:4]} \t\tmove right..."
    )
    request.Velocity.PanTilt.x = XMAX
    request.Velocity.PanTilt.y = 0
    do_move(ptz, request)


def move_left(ptz, request):
    print(
        f"X1: {str(obs_1_data[0][0])[:4]},\t\tY1: {str(obs_1_data[0][1])[:4]} \t\tmove left..."
    )
    request.Velocity.PanTilt.x = XMIN
    request.Velocity.PanTilt.y = 0
    do_move(ptz, request)


def move_upleft(ptz, request):
    print(
        f"X1: {str(obs_1_data[0][0])[:4]},\t\tY1: {str(obs_1_data[0][1])[:4]} \t\tmove up left..."
    )
    request.Velocity.PanTilt.x = XMIN
    request.Velocity.PanTilt.y = YMAX
    do_move(ptz, request)


def move_upright(ptz, request):
    print(
        f"X1: {str(obs_1_data[0][0])[:4]},\t\tY1: {str(obs_1_data[0][1])[:4]} \t\tmove up left..."
    )
    request.Velocity.PanTilt.x = XMAX
    request.Velocity.PanTilt.y = YMAX
    do_move(ptz, request)


def move_downleft(ptz, request):
    print(
        f"X1: {str(obs_1_data[0][0])[:4]},\t\tY1: {str(obs_1_data[0][1])[:4]} \t\tmove down left..."
    )
    request.Velocity.PanTilt.x = XMIN
    request.Velocity.PanTilt.y = YMIN
    do_move(ptz, request)


def move_downright(ptz, request):
    print(
        f"X1: {str(obs_1_data[0][0])[:4]},\t\tY1: {str(obs_1_data[0][1])[:4]} \t\tmove down left..."
    )
    request.Velocity.PanTilt.x = XMAX
    request.Velocity.PanTilt.y = YMIN
    do_move(ptz, request)


def setup_move():
    mycam = ONVIFCamera(IP, PORT, USER, PASS, WSDL_PATH)
    # Create media service object
    media = mycam.create_media_service()

    # Create ptz service object
    global ptz
    ptz = mycam.create_ptz_service()

    # Get target profile
    media_profile = media.GetProfiles()[0]

    # Get PTZ configuration options for getting continuous move range
    request = ptz.create_type("GetConfigurationOptions")
    request.ConfigurationToken = media_profile.PTZConfiguration.token
    ptz_configuration_options = ptz.GetConfigurationOptions(request)

    global moverequest
    moverequest = ptz.create_type("ContinuousMove")
    moverequest.ProfileToken = media_profile.token
    if moverequest.Velocity is None:
        moverequest.Velocity = ptz.GetStatus(
            {"ProfileToken": media_profile.token}
        ).Position

    # Get range of pan and tilt
    # NOTE: X and Y are velocity vector
    global XMAX, XMIN, YMAX, YMIN
    XMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
    XMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
    YMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
    YMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min


def readin():
    """Reading from stdin and displaying menu"""
    global moverequest, ptz
    movements = readInput()

    if movements:
        if movements[0] == 10:
            move_up(ptz, moverequest)
        elif movements[0] == 12:
            move_down(ptz, moverequest)
        elif movements[0] == 1:
            move_left(ptz, moverequest)
        elif movements[0] == 21:
            move_right(ptz, moverequest)
        elif movements[0] == 0:
            move_upleft(ptz, moverequest)
        elif movements[0] == 20:
            move_upright(ptz, moverequest)
        elif movements[0] == 2:
            move_downleft(ptz, moverequest)
        elif movements[0] == 22:
            move_downright(ptz, moverequest)
        elif movements[0] == 11:
            ptz.Stop({"ProfileToken": moverequest.ProfileToken})
            active = False
        else:
            print(f"No values for movements: {movements}")


if __name__ == "__main__":
    setup_move()
    try:
        while True:
            readin()
    except KeyboardInterrupt:
        ptz.Stop({"ProfileToken": moverequest.ProfileToken})
        print()
        print("Stopping object detection...")
        pass
    # finally:
    #     loop.remove_reader(sys.stdin)
    #     loop.close()
