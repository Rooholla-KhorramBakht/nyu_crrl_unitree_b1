#!/usr/bin/env python3
import rospy
from std_msgs.msg import Header
from audio_common_msgs.msg import AudioData, AudioDataStamped
import sounddevice as sd
import numpy as np

# Constants
SAMPLE_RATE = 44100  # Sample rate (44100 Hz is a common value)
DURATION = 20  # Duration of audio capture in seconds
BUFFER_SIZE = 512  # Buffer size for audio playback

# ROS node initialization
rospy.init_node('audio_capture_node')

# Get input device from ROS parameter
input_device = rospy.get_param('~input_device', default='default')
print(f'Opening input device: {input_device}')
input_device='hw:2,0'
# ROS publisher initialization
audio_pub_1 = rospy.Publisher('audio_ch1', AudioDataStamped, queue_size=1)
audio_pub_2 = rospy.Publisher('audio_ch2', AudioDataStamped, queue_size=1)

# Callback function for audio capture
def audio_callback(indata, frames, time, status):
    # Create AudioDataStamped message
    audio_msg_ch1 = AudioDataStamped()
    audio_msg_ch1.header = Header()
    audio_msg_ch1.header.stamp = rospy.Time.now()
    audio_msg_ch1.audio = AudioData()
    
    audio_msg_ch2 = AudioDataStamped()
    audio_msg_ch2.header = Header()
    audio_msg_ch2.header.stamp = audio_msg_ch1.header.stamp
    audio_msg_ch2.audio = AudioData()
    data = (indata*128+128).astype(np.uint8)
    ch1 = data[:,0].squeeze().tolist()
    ch2 = data[:,1].squeeze().tolist()
    audio_msg_ch1.audio.data = ch1
    audio_msg_ch2.audio.data = ch2
    audio_pub_1.publish(audio_msg_ch1)
    audio_pub_2.publish(audio_msg_ch2)

# Start audio capture
with sd.InputStream(
    callback=audio_callback,
    channels=2,
    samplerate=SAMPLE_RATE,
    blocksize=BUFFER_SIZE,
    device=input_device):
    while not rospy.is_shutdown():
        sd.sleep(int(DURATION * 1000))  # Sleep in milliseconds to allow audio capture
