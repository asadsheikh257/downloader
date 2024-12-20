import streamlit as st
import subprocess
import os
import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip

# Function to merge audio and video using moviepy
def merge_audio_video(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    video_clip.close()
    audio_clip.close()

# Function to download video and audio separately and merge them
def download_video(url, is_playlist, quality, subtitles):
    # Create a temporary directory to save the downloaded files
    temp_dir = tempfile.mkdtemp()

    # Base paths for video and audio
    video_path = os.path.join(temp_dir, "video.mp4")
    audio_path = os.path.join(temp_dir, "audio.m4a")
    output_path = os.path.join(temp_dir, "output.mp4")

    # Download video
    video_cmd = [
        "yt-dlp", "-f", f"bv*[height<={quality}][ext=mp4]", "-o", video_path, url
    ]

    # Download audio
    audio_cmd = [
        "yt-dlp", "-f", "ba[ext=m4a]", "-o", audio_path, url
    ]

    # Execute the commands
    subprocess.run(video_cmd, check=True)
    subprocess.run(audio_cmd, check=True)

    # Merge video and audio
    merge_audio_video(video_path, audio_path, output_path)

    # Return the path to the merged file
    return output_path

# Streamlit UI
st.set_page_config(page_title="YouTube Downloader", layout="centered")
st.title("YouTube Video Downloader")

# Input fields
with st.container():
    st.markdown("### Input Video Details")
    url = st.text_input("Enter YouTube URL", key="url_input")
    option = st.selectbox("Download Type", ("Single Video", "Playlist"), key="download_type")
    is_playlist = option == "Playlist"

# Options for quality and subtitles
with st.container():
    st.markdown("### Options")
    quality = st.selectbox(
        "Select Video Quality",
        ["144", "240", "360", "480", "720", "1080", "1440", "2160"],
        index=4,
        key="quality_select"
    )
    subtitles = st.checkbox("Add Subtitles", key="subtitles_checkbox")

# Download button
with st.container():
    download_button = st.button("Download", key="download_button")

if download_button:
    if not url:
        st.error("Please provide a valid YouTube URL.")
    else:
        try:
            with st.spinner("Downloading and processing..."):
                # Download video and get the file path
                file_path = download_video(url, is_playlist, quality, subtitles)

                # Provide a download link/button for the user to download the video
                with open(file_path, "rb") as file:
                    st.download_button(
                        label="Download Video",
                        data=file,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4"
                    )

            st.success("Download completed successfully!")
        except subprocess.CalledProcessError:
            st.error("An error occurred during the download. Please check the URL and try again.")



# JavaScript to detect the theme
st.markdown("""
    <script>
    window.onload = function() {
        const theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        document.body.setAttribute('data-streamlit-theme', theme);
    }
    </script>
""", unsafe_allow_html=True)

# Footer - dynamically styled
footer_style = """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            padding: 1px 0;
            font-size: 14px;
        }
        .footer[data-streamlit-theme='dark'] {
            background-color: #0E1117;  /* Dark background */
            color: #FAFAFA;  /* White text */
        }
        .footer[data-streamlit-theme='light'] {
            background-color: #f1f1f1;  /* Light background */
            color: #333;  /* Dark text */
        }
        .footer a {
            text-decoration: none;
        }
        /* Email and phone number link color */
        .footer a.email, .footer a.phone {
            color: inherit;  /* Inherit the color from footer (white in dark, dark in light) */
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
"""

# Insert the footer styles
st.markdown(footer_style, unsafe_allow_html=True)

# Footer content
st.markdown("""
    <div class="footer">
        <p>Contact: <a href="mailto:asadsheikh257@gmail.com" class="email">asadsheikh257@gmail.com</a> | Phone: <a href="tel:+923017481916" class="phone">+923017481916</a></p>
    </div>
""", unsafe_allow_html=True)
