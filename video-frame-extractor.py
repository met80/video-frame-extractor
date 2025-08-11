import cv2
import os
import argparse

def extract_frames_with_time(video_path, output_folder, every_n=1):
    """
    Extract frames from a video and save them with timestamp in the filename.

    Args:
        video_path (str): Path to the video file.
        output_folder (str): Directory to save the extracted frames.
        every_n (int): Save every Nth frame (default = 1).
    """
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"FPS: {fps}, Total frames: {total_frames}")

    frame_idx = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % every_n == 0:
            timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            seconds = timestamp_ms // 1000
            milliseconds = timestamp_ms % 1000
            filename = os.path.join(output_folder, f"frame_{seconds:02d}s{milliseconds:03d}ms.png")
            cv2.imwrite(filename, frame)
            saved_count += 1

        frame_idx += 1

    cap.release()
    print(f"Done. Saved {saved_count} frames.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from a video with timestamps.")
    parser.add_argument("video_path", help="Path to the input video file")
    parser.add_argument("output_folder", help="Folder to save extracted frames")
    parser.add_argument("--every_n", type=int, default=1, help="Save every Nth frame (default: 1)")

    args = parser.parse_args()
    extract_frames_with_time(args.video_path, args.output_folder, args.every_n)
