import sys
import time
import carla
import cv2
import pygame

import numpy as np

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



def pygame_callback(data, obj):
    img = np.reshape(np.copy(data.raw_data), (data.height, data.width, 4))
    img = img[:,:,:3]
    img = img[:, :, ::-1]
    obj.surface = pygame.surfarray.make_surface(img.swapaxes(0,1))

class RenderObject(object):
    def __init__(self, width, height):
        init_image = np.random.randint(0,255,(height,width,3),dtype='uint8')
        self.surface = pygame.surfarray.make_surface(init_image.swapaxes(0,1))
try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(2.0)

    camera = world.spawn_actor(cam_bp, spawn_point, attach_to=vehicle)
    # listener = sensor.listen(lambda data: process_img(data))
    # listener = camera.listen(lambda data: image.save_todisk('output/%06d.png' % image.frame))
    renderObject = RenderObject(IM_WIDTH, IM_HEIGHT)
    camera.listen(lambda image: pygame_callback(image, renderObject))

    actor_list.append(camera)


    time.sleep(30)  # 使程序暂停执行 30 秒钟

finally:  # finally 关键字引导的是一个代码块，其中的代码将始终执行，无论是否发生异常
    for actor in actor_list:
        actor.destroy()
    # cv2.destroyAllWindows()
    print("All Cleaned up !!")
