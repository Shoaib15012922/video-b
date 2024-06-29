import cv2
import firebase_admin
from firebase_admin import credentials, storage

# Replace with your Firebase project credentials (get from project settings)
cred = credentials.Certificate('fir-838b9-firebase-adminsdk-i868v-958ea70e32.json')
firebase_app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'fir-838b9.appspot.com'
})

def video_to_wireframe(input_video, output_video):
    """
    This function takes a video as input and generates a wireframed video as output.

    Args:
        input_video: Path to the input video file.
        output_video: Path to the output video file where the wireframed video will be saved.
    """
    # Read the input video
    cap = cv2.VideoCapture(input_video)

    # Check if video capture is successful
    if not cap.isOpened():
        print("Error opening video stream or file")
        return

    # Get video frame width and height
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec for the output video
    fourcc = cv2.VideoWriter_fourcc(*'avc1')

    # Create the output video writer object
    out = cv2.VideoWriter(output_video, fourcc, 20.0, (width, height), False)

    # Process video frames one by one
    while True:
        ret, frame = cap.read()

        # Check if frame is read correctly
        if not ret:
            print("Can't receive frame (stream end?). Exiting...")
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection to detect edges in the frame
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Outlines the edges with white color
        out.write(edges)

    # Release all resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Upload the generated video to Firebase Storage
    bucket = storage.bucket()  # Use firebase_admin.storage.bucket() to get the bucket instance
    blob = bucket.blob(output_video)  # Replace with desired storage path in Firebase
    blob.upload_from_filename(output_video)
    print(f"Wireframed video uploaded to Firebase Storage: {blob.public_url}")

# Example usage
input_video = "input1.mp4"  # Replace with your video path
output_video = "output5.mp4"  # Define output path

video_to_wireframe(input_video, output_video)

print("Wireframed video generation complete!")
