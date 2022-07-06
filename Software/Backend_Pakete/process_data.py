
import open3d as o3d #pip install open3d
import numpy as np #pip install numpy


class ProcessData():
   
   


    def __init__(self):

        # umgeschrieben
        self.bbox = o3d.geometry.AxisAlignedBoundingBox((-0.13, -0.13, 0), (0.13, 0.13, 0.2))
        self.main_pcd = None

        self.dtr = np.pi / 180
        self.distance = 0.258 - 0.0
        #self.distance = 0.258 - self.backDistance



    #muss dann als erstes gemacht werden nach der Erstellung des process_data Objekts
    def main_pcdCreation(self):
        self.main_pcd = o3d.geometry.PointCloud()

        


    def processFoto(self, angle,depth_image,color_image,intrinsic):
        print(angle)

        self.angle = angle

        #self.depth_frame_open3d = o3d.geometry.Image(self.depth_image)
        #self.color_frame_open3d = o3d.geometry.Image(self.color_image)

        self.depth_frame_open3d = o3d.geometry.Image(depth_image)
        self.color_frame_open3d = o3d.geometry.Image(color_image)

        self.rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(self.color_frame_open3d,
                                                                             self.depth_frame_open3d,
                                                                             convert_rgb_to_intensity=False)

        #self.pcd = o3d.geometry.PointCloud.create_from_rgbd_image(self.rgbd_image, self.intrinsic)

        self.pcd = o3d.geometry.PointCloud.create_from_rgbd_image(self.rgbd_image, intrinsic)


        self.pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
        self.pcd.orient_normals_towards_camera_location(camera_location=np.array([0., 0., 0.]))
        self.getcameraLocation()
        self.rMatrix()
        self.pcd.rotate(self.R, (0, 0, 0))
        self.pcd.translate((self.x, self.y, self.z))
        self.pcd = self.pcd.crop(self.bbox)
        self.pcd, self.ind = self.pcd.remove_statistical_outlier(nb_neighbors=100, std_ratio=2)
        self.main_pcd = self.main_pcd + self.pcd

    def getPointcloud(self):
        return self.main_pcd



    def getcameraLocation(self):
        self.x = np.sin(self.angle * self.dtr) * self.distance - np.cos(self.angle * self.dtr) * 0.035
        self.y = -np.cos(self.angle * self.dtr) * self.distance - np.sin(self.angle * self.dtr) * 0.035
        self.z = 0.165
        self.o = self.angle
        self.a = 112.5
        self.t = 0

    def rMatrix(self):
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