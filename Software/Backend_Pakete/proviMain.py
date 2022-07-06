from Software.Backend_Pakete.scan import *
from Software.Backend_Pakete.initialize_scan import *
from Software.Backend_Pakete.process_data import *
from Software.Backend_Pakete.export_scan import *
from Software.Backend_Pakete.arduino import *



ardObj = Arduino(1, 1, 1)


scanobj = Scan((1, 2, 30, 10, 0))

initScanObj = InitializeScan(scanobj.width,scanobj.height,scanobj.framerate, scanobj.autoexposureFrames)


initScanObj.startPipeline()
initScanObj.stopPipeline()

initScanObj.takeFoto()

processDataObj = ProcessData()

# angle kommt von startscan statt der 0
processDataObj.processFoto(0,initScanObj.depth_igm(),initScanObj.color_image(),initScanObj.intrinsic())

exportScanObj = ExportScan()

exportScanObj.makeSTL(1,1,1,1,processDataObj.main_pcd)













