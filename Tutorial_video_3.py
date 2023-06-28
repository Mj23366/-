import glob
import os
import sys
import random
import time
import numpy as np
import cv2

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])

except IndexError:  # 用于捕获并处理 IndexError 类型的异常
    pass

import carla
actor_list = []  # 创建一个空的演员列表，用于存储在 Carla 服务器上创建的演员对象

SHOW_PREVIEW = False
IM_WIDTH = 960
IM_HEIGHT = 680

class CarEnv:
    SHOW_CAM = SHOW_PREVIEW
    STEER_AMT = 1.0
    im_width = IM_WIDTH
    im_height = IM_HEIGHT

    def __int__(self):
        self.client = carla.Client("localhost", 2000)
        self.client.set_timeout(2.0)
        self.world = self.client.get_world()
        blueprint_library = self.world.get_blueprint_library()
        self.model_3 = blueprint_library.filter("model3")[0]

    def reset(self):
        self.collision_list = []
        self.actor_list = []

        self.transform = random.choice(self.world.get_map().get_spawn_points())
        self.vehicle = self.world.spawn_actor(self.model_3, self.transform)

        self.actor_list.append(self.vehicle)

def process_img(image):
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    cv2.imshow("123", i3)
    cv2.waitKey(2)
    return i3 / 255.0

