import cv2
from ffpyplayer.player import MediaPlayer
import os

class VideoPlayer:
    def __init__(self, folder):
        self.video_folder = folder
        # Gets a list of video files in the specified folder
        self.video_files = self.get_video_files()
        # Assigning index to which video in the folder we want to play
        self.current_video_index = 0
        
    # Returns a list of video files (ending with ".mp4") in the specified folder
    def get_video_files(self):
        return [f for f in os.listdir(self.video_folder) if f.endswith(".mp4")]

    def play_selected_video(self):
        # Gets the full path of the selected video
        video_path = os.path.join(self.video_folder, self.video_files[self.current_video_index])
        # Opens the video file using OpenCV for video display
        video = cv2.VideoCapture(video_path)
        # Creates a MediaPlayer object for handling audio synch
        player= MediaPlayer(video_path)

        self.setup_video_window()

        #A loop to read video frames & display them
        while True:
            # Reads a frame from the video
            grabbed, frame = video.read()
            # Gets the audio frame and status from the MediaPlayer
            audio_frame, val = player.get_frame()

            # Checks if the video has reached the end
            if not grabbed:
                print("End of video")
                break
            
            # Checks if you pressed the quit button (Esc in this case)
            if self.check_quit_key():
                break
            # Displays the video frame
            self.show_frame(frame)

        # Cleans up resources after playing the video
        self.cleanup(video)

    def setup_video_window(self):
        cv2.namedWindow("VideoStarter", cv2.WINDOW_NORMAL)
        # Sets the window to full-screen mode
        cv2.setWindowProperty("VideoStarter", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def show_frame(self, frame):
        cv2.imshow("VideoStarter", frame)

    def cleanup(self, video):
        # Releases the video capture object and closes all OpenCV windows
        video.release()
        cv2.destroyAllWindows()

    # Use Esc to stop the video & close the window (can be changed to any button)
    def check_quit_key(self):
        # Adjust the number in cv2.waitKey() to sync video and sound
        return cv2.waitKey(29) & 0xFF == 27

# Creates a VideoPlayer instance with the folder containing video files
if __name__ == "__main__":
    video_player = VideoPlayer("videos")
    video_player.play_selected_video()
