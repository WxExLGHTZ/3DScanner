
import open3d as o3d #pip install open3d
import numpy as np #pip install numpy


class ExportScan():

    def makeSTL(self, kpoints, stdRatio, depth, iterations, main_pcd):
        # print(self.main_pcd)

        #umgeschrieben
        #self.stl_pcd = self.main_pcd
        self.stl_pcd = main_pcd

        self.stl_pcd = self.stl_pcd.uniform_down_sample(every_k_points=kpoints)
        self.stl_pcd, self.ind = self.stl_pcd.remove_statistical_outlier(nb_neighbors=100, std_ratio=stdRatio)
        self.bbox1 = o3d.geometry.AxisAlignedBoundingBox((-0.13, -0.13, 0), (0.13, 0.13, 0.01))
        self.bottom = self.stl_pcd.crop(self.bbox1)
        try:
            self.hull, self._ = self.bottom.compute_convex_hull()
            self.bottom = self.hull.sample_points_uniformly(number_of_points=10000)
            self.bottom.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
            self.bottom.orient_normals_towards_camera_location(camera_location=np.array([0., 0., -10.]))
            self.bottom.paint_uniform_color([0, 0, 0])
            self._, self.pt_map = self.bottom.hidden_point_removal([0, 0, -1], 1)
            self.bottom = self.bottom.select_by_index(self.pt_map)
            self.stl_pcd = self.stl_pcd + self.bottom
        except:
            print("No bottom could be made")
            pass
        finally:
            self.mesh, self.densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(self.stl_pcd,
                                                                                                  depth=depth)
            self.mesh = self.mesh.filter_smooth_simple(number_of_iterations=iterations)
            self.mesh.scale(1000, center=(0, 0, 0))
            self.mesh.compute_vertex_normals()

        return self.mesh