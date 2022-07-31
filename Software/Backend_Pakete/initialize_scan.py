import pyrealsense2 as rs
import open3d as o3d #pip install open3d
import numpy as np #pip install numpy


class InitializeScan():



    def __init__(self, width, height, framerate,autoexposureFrames):

        self.width = width
        self.height = height
        self.framerate = framerate
        self.autoexposureFrames = autoexposureFrames
        self.thePipeline = rs.pipeline()

        self.align = None
        self.theConfig = rs.config()

        self.theConfig.enable_stream(rs.stream.color, self.width, self.height, rs.format.any, self.framerate)
        self.theConfig.enable_stream(rs.stream.depth, self.width, self.height, rs.format.any, self.framerate)

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


#pipeline zur kamera starten
    def pipelineStarten(self):

        self.thePipeline.start(self.theConfig)
        self.align = rs.align(rs.stream.color)

        print("Pipeline gestartet")

# pipeline zur kamera beenden
    def pipelineStoppen(self):

        self.thePipeline.stop()
        self.thePipeline = None
        self.theConfig = None

        print("Pipeline gestopt")


#aufnahme der Daten durch kamera
    def aufnahme(self):


        print("Foto aufgenommen")
        for i in range(self.autoexposureFrames):
            self.cadrageSet = self.thePipeline.wait_for_frames()


        self.cadrageSet = self.thePipeline.wait_for_frames()
        self.cadrageSet = self.align.process(self.cadrageSet)
        self.profile = self.cadrageSet.get_profile()
        self.intrinsicsDepth = self.profile.as_video_stream_profile().get_intrinsics()
        self.w, self.h = self.intrinsicsDepth.width, self.intrinsicsDepth.height
        self.fx, self.fy = self.intrinsicsDepth.fx, self.intrinsicsDepth.fy
        self.px, self.py = self.intrinsicsDepth.ppx, self.intrinsicsDepth.ppy

        self.color_frame = self.cadrageSet.get_color_frame()
        self.depth_frame = self.cadrageSet.get_depth_frame()


#intrinsische matrix
    def intrinsics(self):

        self.intrinsic = o3d.camera.PinholeCameraIntrinsic(self.w, self.h, self.fx, self.fy, self.px, self.py)

        return self.intrinsic

#tiefendaten
    def depth_img(self):
        self.depth_image = np.asanyarray(self.depth_frame.get_data())

        return self.depth_image

#rgb daten
    def color_img(self):
        self.color_image = np.asanyarray(self.color_frame.get_data())

        return self.color_image
#gibt bilddaten zurück
    def bildArray(self):
        return self.color_image
