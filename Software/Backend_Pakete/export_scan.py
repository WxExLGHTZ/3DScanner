
import open3d as o3d #pip install open3d
import numpy as np #pip install numpy


class ExportScan():


#erstellt stl aus Punktwolke
    def stlErstellen(self, kpoints, stdRatio, depth, iterations, hauptPointcloud):

        self.stlPointclod = hauptPointcloud

        self.stlPointclod = self.stlPointclod.uniform_down_sample(every_k_points=kpoints)
        self.stlPointclod, self.ind = self.stlPointclod.remove_statistical_outlier(nb_neighbors=100, std_ratio=stdRatio)
        self.boundingbox_ = o3d.geometry.AxisAlignedBoundingBox((-0.13, -0.13, 0), (0.13, 0.13, 0.01))
        self.bot = self.stlPointclod.crop(self.boundingbox_)
        try:
            self.hull, self._ = self.bot.compute_convex_hull()
            self.bot = self.hull.sample_points_uniformly(number_of_points=10000)
            self.bot.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
            self.bot.orient_normals_towards_camera_location(camera_location=np.array([0., 0., -10.]))
            self.bot.paint_uniform_color([0, 0, 0])
            self._, self.pt_map = self.bot.hidden_point_removal([0, 0, -1], 1)
            self.bot = self.bot.select_by_index(self.pt_map)
            self.stlPointclod = self.stlPointclod + self.bot
        except:
            print("error while making stl")
            pass
        finally:
            self.mesh, self.densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(self.stlPointclod,
                                                                                                  depth=depth)
            self.mesh = self.mesh.filter_smooth_simple(number_of_iterations=iterations)
            self.mesh.scale(1000, center=(0, 0, 0))
            self.mesh.compute_vertex_normals()

        return self.mesh