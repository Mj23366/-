# carla ros bridge 安装（还没跑懂）

系统：ubuntu20.04.6 LTS

电脑：联想r9000p 2021H

carla版本：0.9.14

ROS版本：noetic

## 1. 参考链接：
(1) [官方文档：ROS bridge installation for ROS 1](https://carla.readthedocs.io/projects/ros-bridge/en/latest/ros_installation_ros1/#before-you-begin)

(2) [bilibili：自动驾驶开发与Carla模拟器 4：Carla ROS Bridge](https://www.bilibili.com/video/BV1m24y1D7wW/?spm_id_from=333.1007.top_right_bar_window_custom_collection.content.click&vd_source=d0a48daf2273360b076d3a266765dfd0)

(3) [知乎：carla-ros-bridge的安装](https://zhuanlan.zhihu.com/p/422744756)

## 2. carla-ros-bridge的源码安装（官方文档说只能是ubuntu18.04才能用）：
```
mkdir -p ~/carla-ros-bridge/catkin_ws/src
cd ~/carla-ros-bridge
git clone --recurse-submodules https://github.com/carla-simulator/ros-bridge.git catkin_ws/src/ros-bridge
source /opt/ros/noetic/setup.bash

cd catkin_ws
rosdep update
rosdep install --from-paths src --ignore-src -r

catkin_make     # 或者使用catkin build，但我用这个会报错，所以用catkin_make
```
(1) `rosdep update` 失败可参考[链接](https://blog.csdn.net/Iamsonice/article/details/123315787)

(2) `catkin_make`失败，可尝试：
```
catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3
```

(3) `catkin_build`报错，但运行`catkin_make`成功，删除`build`和`devel`文件重新执行`catkin_build`成功

chatGPT解释：可能是由于在 catkin_make 编译时，CMake 生成的缓存文件（CMakeCache）和构建信息文件（catkin_generated）在 build 文件夹中被保存。当你运行 catkin build 时，它会在 build 文件夹中寻找这些文件。如果这些文件存在，它会认为先前的构建已经存在，并跳过重新构建，从而导致构建错误。
所以删除 build 和 devel 文件夹后，再运行 catkin build，会重新生成这些文件夹以及构建所需的所有文件。这可能是你能够成功构建的原因。



## 3. gitclone

根据官方文档，克隆

在这一步出错：**6.** Install the required ros-dependencies:

```
cd catkin_ws
rosdep update
rosdep install --from-paths src --ignore-src -r
```

参考链接：https://blog.csdn.net/zbw1185/article/details/123807654第三种方法，改完之后把翻墙改成全局就可以运行（试过不改文件，直接全局翻墙不行，还是得改文件）

运行 rosdep install --from-paths src --ignore-src -r 报错：  pip: Failed to detect successful installation of [transforms3d]   然后 pip install transforms3d ，然后再运行就行了




## 3. 测试carla-ros-bridge
根据 [bilibili：自动驾驶开发与Carla模拟器 4：Carla ROS Bridge](https://www.bilibili.com/video/BV1m24y1D7wW/?spm_id_from=333.1007.top_right_bar_window_custom_collection.content.click&vd_source=d0a48daf2273360b076d3a266765dfd0) 运行以下命令：

终端1运行：
```
cd /home/mj/carla/CARLA_0.9.14
./CarlaUE4.sh -prefernvidia -quality-level=Low -benchmark -fps=15
```

测试1：

打开终端2进入上面创建的ros工作空间`catkin_ws`中，然后`source ./devel/setup.bash`执行：
``` 
roslaunch carla_ad_demo carla_ad_demo.launch
```
解决完异常后会生成一辆`Tesla model 3`，并且自动行驶即测试成功



添加环境变量（.bashrc）：

```
export PYTHONPATH=$PYTHONPATH:/home/mj/carla/CARLA_0.9.14/PythonAPI/carla/dist/carla-0.9.14-py3.7-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:/home/mj/carla/CARLA_0.9.14/PythonAPI/carla
```

有没有可能就是直接把carla的安装以来都给装进去（carla安装是在carla虚拟环境中，ros运行是在ros的虚拟环境中）

现在将carla需要安装的依赖都装进ros虚拟环境中，emm还是不行，依然报错。下次试试carla和ROS在同一个虚拟环境中

```
pip install rospkg
pip install transforms3d
pip install agents
pip install opencv-python  
pip install opencv-contrib-python 
pip install pycryptodomex
pip install gnupg
pip install contrib
pip install --upgrade tf_slim
pip install shutdown
```




------
------
### 报错的处理：
### 1. 运行`roslaunch carla_ad_demo carla_ad_demo.launch`报错：
#### (1) 包不支持当前python版本
如果python3的版本太新或太旧，则可能导致[报错](https://stackoverflow.com/questions/70610389/importerror-with-event-cpython-310-x86-64-linux-gnu-so-undefined-symbol-pyge)：`undefined symbol: _PyGen_Send`，执行以下命令将conda虚拟环境的python版本降至3.8（太新的版本有些包还未支持）即可
```
conda install python=3.8 
```

#### (2) 出现报错：
```
ModuleNotFoundError: No module named 'gnupg'
```
参考[链接](https://zhuanlan.zhihu.com/p/416872266)，在这里大概率就只有两个原因：module包没安装、需要将module添加至环境变量

#### ① module包没安装

例如：`ModuleNotFoundError: No module named 'gnupg'`

终端运行（需要激活conda虚拟环境）：`pip install gnupg`

安装完后就不报错了，如果还报错，再运行一次确定是否已经完全安装

注意：缺少`gnupg`不一定是下载`gnupg`，可能是另外一个需要安装的包（这个包里面包含`gnupg`，这种情况就百度/谷歌）


#### ② 将module添加至环境变量

例如：`ModuleNotFoundError: No module named 'carla'`

首先确定是否已经安装了carla包，终端运行（需要激活conda虚拟环境）：`pip install carla` ，返回：
```
Requirement already satisfied: carla in ./anaconda3/envs/carla/lib/python3.8/site-packages (0.9.14)
```
说明已经安装了carla包，需要将其添加至环境变量，参考[链接](https://blog.csdn.net/liangzc1124/article/details/107437026)。在本次安装中，添加的环境变量有：
```
export PYTHONPATH=$PYTHONPATH:/home/mj/carla/CARLA_0.9.14/PythonAPI/carla/dist/carla-0.9.14-py3.7-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:/home/mj/carla/CARLA_0.9.14/PythonAPI/carla
```

注意：如果已经安装包并且添加了环境变量也仍然报错，可以尝试重启电脑

#### (3) 报错：`CARLA python module version 0.9.13 required. Found: 0.9.14`

解决办法：参考[链接](https://blog.csdn.net/weixin_37669024/article/details/123322341)修改 ~/carla-ros-bridge/catkin_ws/src/ros-bridge/carla_ros_bridge/src/carla_ros_bridge目录下的 CARLA_VERSION 文件内容，修改为 0.9.14 


#### (4) 运行`roslaunch carla_ad_demo carla_ad_demo.launch`无报错但一直黑屏没有生成车辆

参考[bilibili：自动驾驶开发与Carla模拟器 4：Carla ROS Bridge](https://www.bilibili.com/video/BV1m24y1D7wW/?spm_id_from=333.1007.top_right_bar_window_custom_collection.content.click&vd_source=d0a48daf2273360b076d3a266765dfd0) 是有车辆生成的

将白字报错的：
```
Exception in thread Thread-7: Traceback (most recent call last)
......
```
后面部分复制给chatGPT，它让我运行一下命令后解决，有车辆出现了
```
sudo apt update
sudo apt install python3-dev libffi-dev
sudo apt upgrade libffi-dev
conda update -c conda-forge libffi
```



AttributeError: module 'tensorflow' has no attribute 'contrib'

这种下载了也找不到包的，可以尝试uninstall ，然后再装一个更低一点的版本

例如 agents.navigation 找不到，搜也搜不到，把agents降低版本就解决了



重新再下载一个包

pip install empy

