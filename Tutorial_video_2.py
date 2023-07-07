import glob
import os
import random
import sys
import time

import cv2

import numpy as np

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])

except IndexError:  # 用于捕获并处理 IndexError 类型的异常
    pass
import carla

actor_list = []  # 创建一个空的演员列表，用于存储在 Carla 服务器上创建的演员对象

IM_WIDTH = 960
IM_HEIGHT = 680


def process_img(image):
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    time.sleep(0.01)
    cv2.imshow("123", i3)       # 这里看看官方文档，doc.pygame for vehicle control.py
                                # 那里面是通过pygame来打开窗口的，我也模仿一下就行。
                                # https://carla.readthedocs.io/en/latest/tuto_G_pygame/#rendering-camera-output-and-controlling-vehicles-with-pygame
    cv2.waitKey(0)
    print("123")
    return i3 / 255.0


try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(2.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    bp = blueprint_library.filter("model3")[0]  # filter： 筛选
    spawn_point = random.choice(world.get_map().get_spawn_points())
    vehicle = world.spawn_actor(bp, spawn_point)
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    actor_list.append(vehicle)

    cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')
    cam_bp.set_attribute("image_size_x", f"{IM_WIDTH}")
    cam_bp.set_attribute("image_size_y", f"{IM_HEIGHT}")
    cam_bp.set_attribute("fov", "110")
    cam_bp.set_attribute('sensor_tick', '25.0')

    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    camera = world.spawn_actor(cam_bp, spawn_point, attach_to=vehicle)
    # listener = sensor.listen(lambda data: process_img(data))
    # listener = camera.listen(lambda data: image.save_todisk('output/%06d.png' % image.frame))

    actor_list.append(camera)


    time.sleep(30)  # 使程序暂停执行 30 秒钟

finally:  # finally 关键字引导的是一个代码块，其中的代码将始终执行，无论是否发生异常
    for actor in actor_list:
        actor.destroy()
    # cv2.destroyAllWindows()
    print("All Cleaned up !!")
