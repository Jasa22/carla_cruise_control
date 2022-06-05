import glob
import os
import sys
import time
import math

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla


def _Radar_callback(radar_data, vehicle, world):

    radar_current_rotation = radar_data.transform.rotation
    radar_velocity_range = 7.5
    debug = world.debug

    distance_name_data = {}
    for detection in radar_data:
        distance_name_data["distance"] = detection.depth

        if distance_name_data["distance"] > 6 and distance_name_data['distance'] < 7:
            print("Slowing down car speed")
            dropped_vehicle.apply_control(carla.VehicleControl(throttle=0))
            dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))

        elif distance_name_data["distance"] > 7 and distance_name_data['distance'] < 7.5:
                print("Speeding up")
                dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=False))
                dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.3))

        break

    for detect in radar_data:
        radar_azimuth = math.degrees(detect.azimuth)
        radar_altitude = math.degrees(detect.altitude)

        forward_view = carla.Vector3D(x=detect.depth - 0.25)
        new_pitch = radar_current_rotation.pitch + radar_altitude
        new_yaw = radar_current_rotation.yaw + radar_azimuth
        new_roll = radar_current_rotation.roll
        carla.Transform(carla.Location(), carla.Rotation(
            pitch=new_pitch,
            yaw=new_yaw,
            roll=new_roll)).transform(forward_view)

        debug.draw_point(
            radar_data.transform.location + forward_view,
            size=0.075,
            life_time=0.06,
            color=carla.Color(255, 0, 0))
