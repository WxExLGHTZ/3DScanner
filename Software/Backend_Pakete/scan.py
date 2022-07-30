import pyrealsense2 as rs
import open3d as o3d #pip install open3d
import numpy as np #pip install numpy


class Scan():


    def __init__(self, width, height, framerate, autoexposureFrames):

        self.width = width
        self.height = height
        self.framerate = framerate
        self.autoexposureFrames = autoexposureFrames