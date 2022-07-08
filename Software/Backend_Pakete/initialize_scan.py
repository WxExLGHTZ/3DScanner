import pyrealsense2 as rs
import open3d as o3d #pip install open3d
import numpy as np #pip install numpy


class InitializeScan():

    def __init__(self, width, height, framerate,autoexposureFrames):

        self.width = width
        self.height = height
        self.framerate = framerate
        self.autoexposureFrames = autoexposureFrames
        self.pipe = rs.pipeline()
        self.align = None
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.any, self.framerate)
        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.any, self.framerate)

        self.color_image = None
        self.depth_image = None
        self.color_frame = None
        self.depth_frame = None
        self.intrinsic = None

        self.w = None
        self.h = None
        self.fx = None
        self.fy = None
        self.px = None
        self.py = None

        #wird benutzt in process_data.py
        #self.depth_image
        #self.color_image


    def startPipeline(self):

        self.pipe.start(self.config)
        self.align = rs.align(rs.stream.color)


    def stopPipeline(self):

        self.pipe.stop()
        self.pipe = None
        self.config = None

        print("pipeline gestopt")



    def takeFoto(self):


        print("foto gemaakt!")
        for i in range(self.autoexposureFrames):
            self.frameset = self.pipe.wait_for_frames()


        self.frameset = self.pipe.wait_for_frames()
        self.frameset = self.align.process(self.frameset)
        self.profile = self.frameset.get_profile()
        self.depth_intrinsics = self.profile.as_video_stream_profile().get_intrinsics()
        self.w, self.h = self.depth_intrinsics.width, self.depth_intrinsics.height
        self.fx, self.fy = self.depth_intrinsics.fx, self.depth_intrinsics.fy
        self.px, self.py = self.depth_intrinsics.ppx, self.depth_intrinsics.ppy

        self.color_frame = self.frameset.get_color_frame()
        self.depth_frame = self.frameset.get_depth_frame()

        #werden jetzt als rückgabewerte von Funktionen übergeben

        #self.intrinsic = o3d.camera.PinholeCameraIntrinsic(self.w, self.h, self.fx, self.fy, self.px, self.py)
        #self.depth_image = np.asanyarray(self.depth_frame.get_data())
        #self.color_image = np.asanyarray(self.color_frame.get_data())




    def intrinsic(self):

        self.intrinsic = o3d.camera.PinholeCameraIntrinsic(self.w, self.h, self.fx, self.fy, self.px, self.py)

        return self.intrinsic



    def depth_igm(self):
        self.depth_image = np.asanyarray(self.depth_frame.get_data())

        return self.depth_image



    def color_igm(self):
        self.color_image = np.asanyarray(self.color_frame.get_data())

        return self.color_image


    def giveImageArray(self):
        return self.color_image
