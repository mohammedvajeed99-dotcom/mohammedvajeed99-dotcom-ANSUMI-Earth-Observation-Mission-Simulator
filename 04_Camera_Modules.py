camera_modules = {}

for i in range(1, 49):

    satellite = f"ASC_074_{i:02d}"

    camera_modules[satellite] = {
        "CameraName": "ASC074_BrisbaneCam",
        "SensorType": "CMOS",
        "CameraType": "Pushbroom",
        "FocalLength_mm": 350,
        "SensorWidth_mm": 45,
        "SensorHeight_mm": 6,
        "HFOV_deg": 7.36,
        "VFOV_deg": 0.98,
        "Swath_km": 68.91,
        "GSD_m": 8.41,
        "Pointing": "Nadir"
    }

print("=====================================")
print("Camera Modules Created")
print("=====================================")
print("Total Cameras:", len(camera_modules))

print()

for sat in list(camera_modules.keys())[:5]:
    print(sat, "->", camera_modules[sat]["CameraName"])