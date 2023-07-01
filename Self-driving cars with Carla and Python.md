# Self-driving cars with Carla and Python

#### 1.  Controlling the Car and getting Camera Sensor Data  

参考链接：

[官方文档：Controlling the Car](https://carla.readthedocs.io/en/latest/core_actors/#vehicles)

[官方文档：Getting Camera Sensor Data](https://carla.readthedocs.io/en/latest/core_sensors/#sensors-step-by-step)

[Youtube: Controlling the Car and getting Camera Sensor Data - Self-driving cars with Carla and Python p.2](https://www.youtube.com/watch?v=2hM44nr7Wms&t=639s)

最终代码文件见：tutorial_video_2.py

##### 1.1  导入相关依赖：

```python
import glob				# 该模块用于在文件系统中搜索匹配的文件路径名
import os				# 提供了与操作系统交互的功能，如路径处理、创建文件夹等
import sys				# 提供了访问与 Python 解释器和其环境相关的变量和函数的功能
import random			# 该模块用于生成伪随机数
import time				# 提供了与时间相关的功能，如获取当前时间、计时等
import numpy as np		# 提供了高性能的多维数组对象和各种数学函数
import cv2				# opencv库的接口，提供了各种图像处理函数和工具
```



##### 1.2  将 Carla 路径添加到 Python编辑器的搜索路径中

```python
try: 
    # 这部分代码的作用是将 carla 模块所在的路径添加到 Python 解释器的搜索路径中。
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
   

except IndexError:	# 如果 sys.path.append() 中的 glob.glob() 返回的列表为空，即没有找到对应的 carla 模块路径，就会发生 IndexError 异常。
    pass

import carla    	# 找到carla的位置后，导入 carla 模块就可以使用其功能和类可用
```

这部分代码是在carla/CARLA_0.9.14/PythonAPI/examples/manual_control.py 文件中复制过来的，官方文档应该有说明

1.  `try` ：Python的一种异常处理机制。用于包裹可能引发异常的代码块，如果包裹的代码发生异常，程序会跳出try块并执行与异常类型匹配的except块中的代码，而不会终止程序的执行；
2.  `sys.path.append()`： 语句将指定的路径添加到 Python 解释器的搜索路径列表中；
3.  `glob.glob`：用于匹配文件路径模式的函数。接受一个字符串参数，该字符串可以包含通配符（如`*`和`?`）以及目录路径和文件名的模式。返回与模式匹配的文件路径列表；
4.   `../carla/dist/carla-*%d.%d-%s.egg `  是相对路径，所以 Python 文件可以放在任意位置，只要相对路径能正确找到 carla 模块的位置即可。
5.   ` except IndexError`：用于捕获并处理 IndexError 类型的异常；
6.   `IndexError`：一种常见的异常类型，在使用索引访问列表、元组或字符串时，如果索引超出范围，就会引发该异常；
7.   `pass`：是一个空语句（空操作）。它用作占位符，表示一个代码块中什么也不做；



##### 1.3  Spawn and Control the Car

1.3.1 actor_list  and  actor.destroy()

```python
# 在创建 actor 之前先定义一个 actor_list 列表
actor_list = []     # 创建一个空的演员列表，用于存储在 Carla 服务器上创建的Actors

# 在创建完 Actor 之后需要将这个 Actor 放进这个列表里面，例如：
# actor_list.append(vehicle)

# 在程序的结尾需要将 actor_list 列表里面的所有对象全部 destroy
finally:    # finally 关键字引导的是一个代码块，其中的代码将始终执行，无论是否发生异常
    for actor in actor_list:
        actor.destroy()
        # 遍历 actor_list 列表并调用每个演员对象的 destroy() 方法，以确保资源的正确释放
    print("All Cleaned up !!")
```

1. Actor 可以是Vehicles、Walkers、Sensors、The spectator、Traffic signs and traffic lights，还有其他carla的相关基本定义可参考：[World and client](https://carla.readthedocs.io/en/latest/core_concepts/#1st-world-and-client)、[Actors and blueprints](https://carla.readthedocs.io/en/latest/core_concepts/#2nd-actors-and-blueprints)、[Maps and navigation](https://carla.readthedocs.io/en/latest/core_concepts/#3rd-maps-and-navigation)、[Sensors and data](https://carla.readthedocs.io/en/latest/core_concepts/#4th-sensors-and-data)；
2.  `finally` 关键字引导的是一个代码块，其中的代码将始终执行，无论是否发生异常；
3.  遍历 `actor_list` 列表并调用每个演员对象的 `destroy()` 方法，以确保资源的正确释放；



1.3.2  一些关于carla的初始化

```python
try: 
    client = carla.Client("localhost", 2000)				# 设置client的IP和端口号
    client.set_timeout(2.0)									# 设置carla客户端的超时时间
    world = client.get_world()								# 获取当前运行的模拟环境的接口对象
    blueprint_library = world.get_blueprint_library()		# 获取当前环境的蓝图对象
```

1.   `client` 是用户请求模拟中的信息和更改的模块，相关可参考[官方文档：World and client](https://carla.readthedocs.io/en/latest/core_concepts/#1st-world-and-client)，client 需要一个IP和一个特定的端口号。
使用多个client的情况：多个独立的程序或系统需要与 Carla 服务器进行通信、并行训练多个智能代理、分布式计算或并行任务
            如果要在多台计算机上进行分布式并行训练，可以使用多个 Carla client 实例来实现。
		 每个计算机上的一个 client 实例将连接到 Carla 服务器，并与其通信。
        		使用多个 client 实例可以实现并行的数据收集和训练。每个 client 实例可以在独立的环境中采集数据，并将数据传输给主节点进行集中处理和训练。
		 多个 client 需要链接到同一个局域网中（例如：连接到同一个路由器或交换机）或者通过互联网远程连接，并且能够相互访问

2.   `"localhost"`: 这是指定 Carla 服务器所在的主机地址。在这里，使用 "localhost" 表示 Carla 服务器位于本地主机上，也就是当前运行代码的计算机上。如果 Carla 服务器位于其他主机上，则需要提供相应的主机地址（IP地址），例如：client = carla.Client("192.168.0.100", 2000)

3.   `2000`:  Carla 服务器监听的端口号。默认情况下，Carla 服务器使用 2000 端口进行通信。不同监听端口号在网络通信中用于标识不同的服务或应用程序。

4.   `client.set_timeout(2.0)` 是用于设置Carla客户端的超时时间。超时时间是指在网络通信中，当客户端发送请求或等待响应时所允许的最长等待时间，也是等待客户端相应的最长时间。
5.  `client.get_world()`  可以获取当前Carla服务器上正在运行的模拟环境的接口对象；
   这个接口对象可以用于访问和控制模拟环境中的各种元素和功能；
   获取到的world对象可以用于执行各种操作，比如添加车辆、设置天气条件、获取模拟环境中的车辆列表、执行模拟步长等；
   通过与world对象的交互，可以实现对模拟环境的控制和观测，从而进行强化学习训练或其他任务；
6. `world.get_blueprint_library()` 从当前的模拟世界对象 world 中获取蓝图库对象 blueprint_library。这个库包含了可用于创建车辆和传感器等实体的各种蓝图，可以使用blueprint_library提供的方法和属性来查找特定类型的蓝图、获取蓝图的属性、创建实体等操作。



1.3.3 Spawn and Control the Car

```python
    bp = blueprint_library.filter("model3")[0]      						# 获得 model3 相应给的实体和属性信息
    spawn_point = random.choice(world.get_map().get_spawn_points())			# 设置汽车生成坐标

    vehicle = world.spawn_actor(bp, spawn_point)							# 根据蓝图信息和坐标生成车辆，并将车辆对象将赋值给变量vehicle
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))	# 将车辆的控制设置为向前行驶
	    # 其中设置了油门 (throttle) 为 1.0，方向盘 (steer) 为 0.0
    
    actor_list.append(vehicle)			# 将生成的车辆对象 vehicle 添加到 actor_list 列表中。
```

1.  `blueprint_library.filter("model3")[0]` ：通过filter() 寻找  `"model3"`  ，然后通过索引[0] 选择列表中的第一个元素。这样变量 bp 就包含了名为 "model3" 的蓝图，可以在后续的代码中使用它来创建相应的实体（例如创建一个 "model3" 类型的车辆）或获取其属性信息
2.  `world.get_map()` 返回地图对象，然后通过调用 get_spawn_points() 方法获取所有可用的生成点
3.  `random.choice()`  函数从生成点列表中随机选择一个生成点，并将其赋值给 spawn_point 变量
4.  `apply_control()`  方法将 `carla.VehicleControl` 对象作为参数传递给 vehicle 对象



1.3.4  运行代码

在上面代码后加上下面代码，启动carla后运行python文件，即可在carla环境中找到一辆随机生成的model3在向前行驶

```python
time.sleep(30)      # 使程序暂停执行 30 秒钟
```



#####  1.4  spawn and get information Camera
```python
# 函数定义，python不要求函数定义需要放在函数调用前面，但为了代码可读性和良好的编程风格，建议函数定义放在函数调用前面
IM_WIDTH = 960
IM_HEIGHT = 680
def process_img(image):
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT,IM_WIDTH,4))
    i3 = i2[:,:,:3]
    cv2.imshow("123",i3)
    cv2.waitKey(2)
    return i3/255.0
```

```python
    # 设置蓝图信息
    cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')	# 选择相机
    cam_bp.set_attribute("image_size_x","IM_WIDTH")						# 相机横轴像素
    cam_bp.set_attribute("image_size_y","IM_HEIGHT")					# 相机纵轴像素
    cam_bp.set_attribute('sensor_tick', '1.0')							# 设置相机帧率
    cam_bp.set_attribute("fov","110")									# 相机角度

    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))			# 相机相对于车辆的位置
    sensor = world.spawn_actor(cam_bp, spawn_point, attach_to=vehicle)	# 生成相机
    listener = sensor.listen(lambda data: process_img(data))			# 读取并利用process_img(data)函数使用相机数据
    actor_list.append(sensor)											# 将生成的相机对象添加到 actor_list 列表中
```


​        这里运行出问题了，cv2.imshow() 就是没办法显示画面（打开的窗口是黑屏）。尝试使用matplotlib、Pygame、pyqtgraph等，有些可以显示第一章图片，有些则是直接将接收到的图片保存成文件，或用一张图片一个窗口这样打开。证明data数据的转换是没问题的，但就是没办法像教程视频一样输出成视频。

​        不深究，后面应该是用RVIZ来集成显示相关传感器的信息的。



2.  

sudo apt-get install libjasper-dev 

