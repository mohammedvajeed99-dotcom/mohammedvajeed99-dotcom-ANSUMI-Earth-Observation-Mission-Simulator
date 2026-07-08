import math

# ============================================================
# ASC_074 Brisbane Earth Observation Camera
# ============================================================

CAMERA_NAME = "ASC074_BrisbaneCam"

# Sensor
SENSOR_TYPE = "CMOS"

# Spectral Bands
SPECTRAL_BANDS = [
    "Blue",
    "Green",
    "Red",
    "Near Infrared"
]

# Orbit
ALTITUDE_KM = 536

# Camera
FOCAL_LENGTH_MM = 350
SENSOR_WIDTH_MM = 45
SENSOR_HEIGHT_MM = 6

# Resolution
IMAGE_WIDTH = 8192
IMAGE_HEIGHT = 1092

# Pixel Size
PIXEL_SIZE_MICRON = 5.5

# ------------------------------------------------------------

HFOV = 2 * math.degrees(
    math.atan(SENSOR_WIDTH_MM / (2 * FOCAL_LENGTH_MM))
)

VFOV = 2 * math.degrees(
    math.atan(SENSOR_HEIGHT_MM / (2 * FOCAL_LENGTH_MM))
)

GROUND_SWATH = 2 * ALTITUDE_KM * math.tan(math.radians(HFOV/2))

GSD = (GROUND_SWATH * 1000) / IMAGE_WIDTH

print("="*60)
print("ASC074 CAMERA")
print("="*60)

print(f"Camera Name      : {CAMERA_NAME}")
print(f"Sensor Type      : {SENSOR_TYPE}")
print(f"Spectral Bands   : {', '.join(SPECTRAL_BANDS)}")

print()

print(f"Orbit Altitude   : {ALTITUDE_KM} km")

print()

print(f"Focal Length     : {FOCAL_LENGTH_MM} mm")
print(f"Sensor Width     : {SENSOR_WIDTH_MM} mm")
print(f"Sensor Height    : {SENSOR_HEIGHT_MM} mm")

print()

print(f"Horizontal FOV   : {HFOV:.2f} deg")
print(f"Vertical FOV     : {VFOV:.2f} deg")

print()

print(f"Ground Swath     : {GROUND_SWATH:.2f} km")

print(f"GSD              : {GSD:.2f} meters/pixel")