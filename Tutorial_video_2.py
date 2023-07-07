import glob
import os
import random
import sys
import time
import pygame
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


def pygame_callback(data, obj):
    img = np.reshape(np.copy(data.raw_data), (data.height, data.width, 4))
    img = img[:, :, :3]
    img = img[:, :, ::-1]
    obj.surface = pygame.surfarray.make_surface(img.swapaxes(0, 1))


class RenderObject(object):
    def __init__(self, width, height):
        init_image = np.random.randint(0, 255, (height, width, 3), dtype='uint8')
        self.surface = pygame.surfarray.make_surface(init_image.swapaxes(0, 1))


try:
    '''some initialises'''
    # Connect to the client and retrieve the world object
    client = carla.Client('localhost', 2000)
    world = client.get_world()

    # Set up the simulator in synchronous mode  同步模式
    settings = world.get_settings()
    settings.synchronous_mode = True  # Enables synchronous mode
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    # Set up the TM in synchronous mode
    traffic_manager = client.get_trafficmanager()
    traffic_manager.set_synchronous_mode(True)

    # Set a seed so behaviour can be repeated if necessary
    traffic_manager.set_random_device_seed(0)
    random.seed(0)

    # We will aslo set up the spectator so we can see what we do
    spectator = world.get_spectator()


    '''spawning vehicles'''
    # Retrieve the map's spawn points
    spawn_points = world.get_map().get_spawn_points()

    # Select some models from the blueprint library
    models = ['dodge', 'audi', 'model3', 'mini', 'mustang', 'lincoln', 'prius', 'nissan', 'crown', 'impala']
    blueprints = []
    for vehicle in world.get_blueprint_library().filter('*vehicle*'):
        # get_blueprint_library()函数获取蓝图库，然后使用filter('*vehicle*')方法筛选出所有包含关键词"vehicle"的蓝图。
        # 返回的结果是一个可迭代对象，可以遍历其中的元素
        if any(model in vehicle.id for model in models):
            # any()函数来检查是否有任何一个models列表中的车辆模型名称出现在vehicle.id中的蓝图ID中
            blueprints.append(vehicle)
            # 这两行代码的作用是遍历蓝图库中的每个蓝图，检查蓝图ID是否包含models列表中任何一个模型名称，
            # 如果包含，则将该蓝图添加到blueprints列表中

    # Set a max number of vehicles and prepare a list for those we spawn
    max_vehicles = 50
    max_vehicles = min([max_vehicles, len(spawn_points)])   # 生成车辆的数量不能多于可生成车辆点的数量
    vehicles = []

    # Take a random sample of the spawn points and spawn some vehicles
    for i, spawn_point in enumerate(random.sample(spawn_points, max_vehicles)):
        # random.sample(spawn_points, max_vehicles)  在spawn_points中随机选择max_vahicles个元素
        # enumerate() 函数用来遍历可迭代对象，并返回索引和对应的元素
        # for i, spawn_point 中，i 是索引，spawn_point 是元素
        temp = world.try_spawn_actor(random.choice(blueprints), spawn_point)
        if temp is not None:
            vehicles.append(temp)

    # Parse the list of spawned vehicles and give control to the TM through set_autopilot()
    for vehicle in vehicles:
        vehicle.set_autopilot(True)
        # Randomly set the probability that a vehicle will ignore traffic lights
        traffic_manager.ignore_lights_percentage(vehicle, random.randint(0, 50))


    # Render object to keep and pass the PyGame surface
    class RenderObject(object):
        def __init__(self, width, height):
            init_image = np.random.randint(0, 255, (height, width, 3), dtype='uint8')
            self.surface = pygame.surfarray.make_surface(init_image.swapaxes(0, 1))





























#     client = carla.Client("localhost", 2000)
#     client.set_timeout(2.0)
#
#     world = client.get_world()
#     blueprint_library = world.get_blueprint_library()
#     bp = blueprint_library.filter("model3")[0]  # filter： 筛选
#     spawn_point = random.choice(world.get_map().get_spawn_points())
#     vehicle = world.spawn_actor(bp, spawn_point)
#     vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
#     actor_list.append(vehicle)
#
#     cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')
#     cam_bp.set_attribute("image_size_x", f"{IM_WIDTH}")
#     cam_bp.set_attribute("image_size_y", f"{IM_HEIGHT}")
#     cam_bp.set_attribute("fov", "110")
#     cam_bp.set_attribute('sensor_tick', '25.0')
#
#     # Initialise the display
#     renderObject = RenderObject(IM_WIDTH, IM_HEIGHT)
#     pygame.init()
#     gameDisplay = pygame.display.set_mode((IM_WIDTH, IM_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
#     # Draw black to the display
#     gameDisplay.fill((0, 0, 0))
#     gameDisplay.blit(renderObject.surface, (0, 0))
#     pygame.display.flip()
#
#     spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
#     camera = world.spawn_actor(cam_bp, spawn_point, attach_to=vehicle)
#     # listener = sensor.listen(lambda data: process_img(data))
#     # listener = camera.listen(lambda data: image.save_todisk('output/%06d.png' % image.frame))
#
#     camera.listen(lambda image: pygame_callback(image, renderObject))
#
#     actor_list.append(camera)
#
#     time.sleep(30)  # 使程序暂停执行 30 秒钟
#
finally:  # finally 关键字引导的是一个代码块，其中的代码将始终执行，无论是否发生异常
    pass
#     for actor in actor_list:
#         actor.destroy()
#     camera.stop()
#     pygame.quit()
#     print("All Cleaned up !!")
