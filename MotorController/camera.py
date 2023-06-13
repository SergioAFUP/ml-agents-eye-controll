import cv2
import requests
from requests.auth import HTTPBasicAuth
from onvif import ONVIFCamera

# PTZ : PAN, TILT, ZOOM camera type


def moveMotors():  # Not working, use movement.py to try the movement for motors
    cam = ONVIFCamera(
        "192.168.101.21",
        8899,
        "admin",
        "Chame1eon",
        "/Users/JavierGonzales/Library/Python/3.9/lib/python3.9/site-packages/wsdl",
    )  # [camera's IP, port, username, password, wsdl library if not detected by default]

    # Create media service object
    media_service = cam.create_media_service()

    # Create ptz service object
    ptz_service = cam.create_ptz_service()

    # Get target profile
    profiles = media_service.GetProfiles()
    target_profile = profiles[0]

    # Get PTZ configuration options for the target profile
    ptz_configuration_options = ptz_service.GetConfigurationOptions(
        {"ConfigurationToken": target_profile.PTZConfiguration.token}
    )

    # Get the range of pan and tilt
    pan_range = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[
        0
    ].XRange
    tilt_range = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[
        0
    ].YRange

    # Construct a request for absolute move
    request = ptz_service.create_type("AbsoluteMove")
    request.ProfileToken = target_profile.token

    # Perform the move
    request.Position = {
        "PanTilt": {
            "x": -1,
            "y": -1,
        }
    }

    ptz_service.AbsoluteMove(request)


def connectToCamera():  # Working
    url = "rtsp://admin:Chame1eon@192.168.101.21"

    cap = cv2.VideoCapture(url)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("IP Camera stream", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def httpRequest():  # Initial attempt get a request form camera
    url = "http://192.168.86.30"
    username = "admin"
    password = "Chame1eon"

    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    print(response.text)


if __name__ == "__main__":
    moveMotors()
