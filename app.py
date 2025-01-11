# import requests
# import streamlit as st
# from streamlit_lottie import st_lottie
# from PIL import Image

# st.set_page_config(page_title="Nepal Plate Vision", page_icon=":tada:", layout="wide")



# def load_lottieurl(url):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# lottie_coding = load_lottieurl("https://lottie.host/5b88b38c-59e2-4423-bad9-59c6373f4f04/k8HYqmoMAy.json")

# with st.container():
#     st.subheader("NEPAL PLATE VISION  :wave:")
#     st.title("Automating vehicle detection and license plate recognition ")
    
    
# with st.container():
#     st.write("---")
#     left_column, right_column = st.columns(2)
#     with left_column:
#         st.header("What I do")
#         st.write("##")
       
# with right_column:
#     st_lottie(lottie_coding, height=300, key="coding")       

import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import cv2
import tempfile
from streamlit_webrtc import webrtc_streamer

# Set page configuration
st.set_page_config(page_title="Nepal Plate Vision", page_icon=":tada:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animation
lottie_coding = load_lottieurl("https://lottie.host/5b88b38c-59e2-4423-bad9-59c6373f4f04/k8HYqmoMAy.json")

# Header section
with st.container():
    st.subheader("NEPAL PLATE VISION  :wave:")
    st.title("Automating vehicle detection and license plate recognition ")

# Main content section
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What I do")
        st.write("##")

    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")

# Add buttons
st.write("---")
st.header("Choose an action")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Real-Time Video")
    if st.button("Start Camera", key="start_camera"):
        st.write("Opening camera...")
        st.write("Press 'Stop' in the pop-up to finish capturing.")
        webrtc_streamer(key="realtime_video", 
                        video_transformer_factory=None, 
                        async_transform=False)

with col2:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader("Choose an image of the vehicle number plate", type=["jpg", "png", "jpeg"], key="upload_image")
    if uploaded_file is not None:
        st.subheader("Uploaded Image:")
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Vehicle Number Plate", use_column_width=True)
