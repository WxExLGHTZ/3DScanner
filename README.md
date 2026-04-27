# 3D Scanner

A desktop application that turns an Intel RealSense depth camera and an Arduino-driven stepper motor turntable into a 3D scanner — capturing RGBD frames from multiple angles, registering them into a unified point cloud via computed rotation-translation matrices, and reconstructing a watertight mesh exported as STL.

## Motivation

Building a 3D scanner from consumer hardware requires solving several non-trivial problems: synchronizing camera capture with turntable rotation, transforming each depth frame into world coordinates based on the current angle, and merging multiple partial point clouds into a single consistent model. This project handles the full pipeline — from raw RGBD frames captured by an Intel RealSense camera through multi-angle point cloud registration to Poisson surface reconstruction — controlled through a PyQt5 desktop interface that lets users configure scan resolution, mesh quality, and hardware settings.

## Features

- Scans physical objects by rotating them on an Arduino-controlled turntable while capturing RGBD frames from an Intel RealSense camera
- Registers point clouds from multiple viewing angles using computed rotation-translation matrices derived from the turntable geometry
- Crops, filters, and denoises point clouds with bounding box constraints and statistical outlier removal
- Reconstructs a watertight triangle mesh from the merged point cloud using Poisson surface reconstruction
- Exports the final model as an STL file, scaled to millimeters
- Displays the point cloud and mesh in an interactive 3D viewer (Open3D)
- Imports existing PLY point cloud files for viewing
- Provides configurable scan parameters: Arduino COM port, step size, frame resolution, and mesh quality settings

## Tech Stack

| Category | Technology |
|----------|-----------|
| Language | Python 3.8.x |
| 3D Processing | Open3D (point clouds, meshing, visualization) |
| Depth Camera | Intel RealSense SDK (pyrealsense2) |
| GUI | PyQt5 |
| Motor Control | Arduino via pyserial (9600 baud) |


## Architecture

The system follows a capture-process-export pipeline driven by the turntable's rotation cycle. The **Arduino** firmware accepts step commands over serial and drives a stepper motor through a 6:1 gear reduction. The **InitializeScan** module configures the RealSense pipeline for aligned color and depth streams and extracts the camera intrinsics. At each rotation step, an RGBD frame is captured and handed to the **ProcessData** module, which converts it to an Open3D point cloud, computes the camera's extrinsic position from the current turntable angle (using trigonometric transformation with known distance and tilt offsets), applies the rotation-translation matrix, crops to a bounding box, and removes outliers. The partial clouds are accumulated into a single registered point cloud. After a full 360° rotation, the **ExportScan** module generates a bottom surface via convex hull sampling, then runs Poisson surface reconstruction with configurable depth and smoothing iterations to produce the final STL mesh.

```
Arduino Turntable ──► RealSense RGBD Capture ──► Point Cloud Conversion
    ──► Extrinsic Transform (angle-based) ──► Registration ──► Poisson Reconstruction ──► STL Export
```

## Getting Started

### Prerequisites

- Windows 
- Python 3.8.x (tested with 3.8.0)
- PyCharm or Visual Studio Code (recommended)
- Intel RealSense D400 series camera
- Arduino with stepper motor (28BYJ-48 + ULN2003 driver, pins 8–11)

### Hardware Setup

Connect the stepper motor driver to Arduino pins 8, 9, 10, 11 and upload the firmware:

```
Upload 3D_scan_neu.ino (or arduino_platform.ino) via the Arduino IDE.
```

> [!NOTE]
> A wiring diagram is provided in `Arduino_Steckplan.jpeg`.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/3d-scanner.git
   cd 3d-scanner/Software
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Upgrade pip and install dependencies:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

> [!NOTE]
> macOS users need to install pyrealsense2 from a separate source:
> `pip install pyrealsense2 -f https://github.com/cansik/pyrealsense2-macosx/releases`

4. Open the project in PyCharm or VS Code and set the interpreter to `venv/Scripts/Python.exe`.

## Usage

1. Place the object on the turntable and connect both the Arduino and the RealSense camera.
2. Run the application:
   ```bash
   python main.py
   ```
3. Click **Settings** to configure the Arduino COM port (default: `COM5`) and scan parameters.
4. Click **Start Scan** — the turntable rotates in steps while the camera captures frames. The status bar shows the current angle. The scan takes less than 1 minute.
5. Click **Show Pointcloud** to inspect the registered point cloud in the 3D viewer.
6. Click **Save STL** to reconstruct the mesh and export it as an STL file.

Alternatively, use **Import** to load an existing `.ply` point cloud file for viewing.


## Authors

- William Eppel
- Mert Karadeniz
- Vinh Thong Trinh
- Habib Ben Khedher
