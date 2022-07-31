
import open3d as o3d #pip install open3d
import numpy as np #pip install numpy


class ProcessData():
   


    def __init__(self):

        self.boundingBox = o3d.geometry.AxisAlignedBoundingBox((-0.13, -0.13, 0), (0.13, 0.13, 0.2))

        self.hauptPointCloud = o3d.geometry.PointCloud()

        self.dtr = np.pi / 180
        self.distance = 0.258


#konvertieren der aufgenommenen Daten in Punktwolken

    def konvertieren(self, angle, depth_image, color_image, intrinsic):

        print(angle)

        self.winkel = angle

        self.depth_frame_open3d = o3d.geometry.Image(depth_image)
        self.color_frame_open3d = o3d.geometry.Image(color_image)

        self.rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(self.color_frame_open3d,
                                                                             self.depth_frame_open3d,
                                                                             convert_rgb_to_intensity=False)


        self.pointCloud = o3d.geometry.PointCloud.create_from_rgbd_image(self.rgbd_image, intrinsic)


        self.pointCloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
        self.pointCloud.orient_normals_towards_camera_location(camera_location=np.array([0., 0., 0.]))
        self.getKameraPos()
        self.rtMatrix()
        self.pointCloud.rotate(self.R, (0, 0, 0))
        self.pointCloud.translate((self.x, self.y, self.z))
        self.pointCloud = self.pointCloud.crop(self.boundingBox)
        self.pointCloud, self.ind = self.pointCloud.remove_statistical_outlier(nb_neighbors=100, std_ratio=2)
        self.hauptPointCloud = self.hauptPointCloud + self.pointCloud


#Punktwolke zurückgeben
    def getPointcloud(self):
        return self.hauptPointCloud



    def getKameraPos(self):
        self.x = np.sin(self.winkel * self.dtr) * self.distance - np.cos(self.winkel * self.dtr) * 0.035
        self.y = -np.cos(self.winkel * self.dtr) * self.distance - np.sin(self.winkel * self.dtr) * 0.035
        self.z = 0.165
        self.o = self.winkel
        self.a = 112.5
        self.t = 0

    def rtMatrix(self):
        self.o = self.o * self.dtr
        self.a = (-self.a) * self.dtr
        self.t = self.t * self.dtr
        self.R = [[np.cos(self.o) * np.cos(self.t) - np.cos(self.a) * np.sin(self.o) * np.sin(self.t),
                   -np.cos(self.o) * np.sin(self.t) - np.cos(self.a) * np.cos(self.t) * np.sin(self.o),
                   np.sin(self.o) * np.sin(self.a)],
                  [np.cos(self.t) * np.sin(self.o) + np.cos(self.o) * np.cos(self.a) * np.sin(self.t),
                   np.cos(self.o) * np.cos(self.a) * np.cos(self.t) - np.sin(self.o) * np.sin(self.t),
                   -np.cos(self.o) * np.sin(self.a)],
                  [np.sin(self.a) * np.sin(self.t), np.cos(self.t) * np.sin(self.a), np.cos(self.a)]]