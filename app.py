import streamlit as st
import subprocess
import os

# Function to download video and save it to a public directory
def download_video(url, is_playlist, quality, subtitles):
    # Create a temporary directory to save the downloaded video
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)

    # Base command for yt-dlp
    cmd = ["yt-dlp", "-o", os.path.join(download_dir, "%(title)s.%(ext)s")]

    # Add format options for video and audio
    quality_formats = {
        "144p": "bv*[height<=144][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "240p": "bv*[height<=240][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "360p": "bv*[height<=360][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "480p": "bv*[height<=480][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "720p": "bv*[height<=720][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "1080p": "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "1440p": "bv*[height<=1440][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "2160p": "bv*[height<=2160][ext=mp4]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "Best Available": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
    }
    cmd += ["-f", quality_formats.get(quality, "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]")]

    # Subtitles options
    if subtitles:
        cmd += ["--write-sub", "--sub-lang", "en", "--embed-subs"]

    # Playlist or single video
    if is_playlist:
        cmd += ["-o", os.path.join(download_dir, "%(playlist_index)s. %(title)s.%(ext)s")]
    else:
        cmd += ["-o", os.path.join(download_dir, "%(title)s.%(ext)s")]

    # Add the URL
    cmd.append(url)

    # Execute the command
    subprocess.run(cmd, check=True)

    # Get the downloaded file path(s)
    downloaded_files = [
        os.path.join(download_dir, f)
        for f in os.listdir(download_dir)
        if f.endswith(".mp4") or f.endswith(".mkv") or f.endswith(".webm")
    ]
    return downloaded_files


# Streamlit UI
st.set_page_config(page_title="YouTube Downloader", layout="centered")
st.title("YouTube Video Downloader!")

# Initialize session state variable
if 'download_triggered' not in st.session_state:
    st.session_state.download_triggered = False
if 'download_files' not in st.session_state:
    st.session_state.download_files = []

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
        ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p", "Best Available"],
        index=4,
        key="quality_select",
    )
    subtitles = st.checkbox("Add Subtitles", key="subtitles_checkbox")


# Assuming the download_video function exists and is defined correctly
# from some_module import download_video 

# Check if the session state has been initialized for download
if "download_triggered" not in st.session_state:
    st.session_state.download_triggered = False
if "download_files" not in st.session_state:
    st.session_state.download_files = []

# Download button (initial step)
with st.container():
    download_button = st.button("Download", key="download_button")

# Handle download button logic
if download_button:
    if not url:
        st.error("Please provide a valid YouTube URL.")
    else:
        try:
            with st.spinner("Downloading..."):
                # Download video and get the file paths
                file_paths = download_video(url, is_playlist, quality, subtitles)
                
                # Store the downloaded files in session state
                st.session_state.download_files = file_paths
                st.session_state.download_triggered = True

            st.success("Download completed successfully!")
        except subprocess.CalledProcessError as e:
            st.error(f"An error occurred during the download: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# Handle the case where download is triggered and files are available
if st.session_state.download_triggered and st.session_state.download_files:
    for file_path in st.session_state.download_files:
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                download_button_placeholder = st.empty()
                download_button = download_button_placeholder.download_button(
                    label="Download Video",
                    data=file,
                    file_name=os.path.basename(file_path),
                    mime="video/mp4"
                )
                
                # Automatically trigger the "Download Video" button using JavaScript
                st.markdown(
                    """
                    <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        const downloadButton = document.querySelector('button[aria-label="Download Video"]');
                        if (downloadButton) {
                            downloadButton.click();
                        }
                    });
                    </script>
                    """,
                    unsafe_allow_html=True
                )

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
