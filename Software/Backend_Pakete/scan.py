import pyrealsense2 as rs
import open3d as o3d #pip install open3d
import numpy as np #pip install numpy


class Scan():


    def __init__(self, width, height, framerate, autoexposureFrames, #backDistance
                 ):

        self.width = width
        self.height = height
        self.framerate = framerate
        self.autoexposureFrames = autoexposureFrames

        # brauchen wir nicht weil ist ja 0 im aufruf von Scan() aus StartScan
        #self.backDistance = backDistance





        # Das befindet sich jetzt in initialize_scan.py
        """
        self.pipe = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.any, self.framerate)
        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.any, self.framerate)
        """
        # Das wird anscheinend nicht gebraucht
        """
        # post-processing filters
        self.depth_to_disparity = rs.disparity_transform(True)
        self.disparity_to_depth = rs.disparity_transform(False)
        self.dec_filter = rs.decimation_filter()
        self.temp_filter = rs.temporal_filter()
        self.spat_filter = rs.spatial_filter()
        self.hole_filter = rs.hole_filling_filter()
        self.threshold = rs.threshold_filter(0.17, 0.4)

        self.dtr = np.pi / 180
        self.distance = 0.258 - self.backDistance
        self.bbox = o3d.geometry.AxisAlignedBoundingBox((-0.13, -0.13, 0), (0.13, 0.13, 0.2))
        """






