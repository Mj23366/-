# carla安装

系统：ubuntu20.04 LTS

电脑：联想r9000p 2021H  AMD5800H  3060

硬盘要求：300G+

参考链接：
(1) [ CARLA  官方文档](https://carla.readthedocs.io/en/latest/build_linux/)

(2) [知乎：Ubuntu 20.04 安装CARLA](https://zhuanlan.zhihu.com/p/595785458)

(3) [CSDN：Carla 安装详细教程 —— Ubuntu 20.04 安装 Carla](https://blog.csdn.net/m0_59161987/article/details/128928855)

## 1. 启动carla

```
conda activate carla 
cd /home/mj/carla/CARLA_0.9.13
./CarlaUE4.sh -prefernvidia 
```



```
conda activate carla 
cd /home/mj/carla/CARLA_0.9.13
./CarlaUE4.sh -prefernvidia -quality-level=Low -benchmark -fps=15
```



## 2. anaconda创建虚拟环境

```
conda create --name carla python=3.8
conda activate carla 
```

## 3. 环境配置

#### (1) 安装python3.8
如果在创建虚拟环境的时候没有指定：python=3.7，则运行以下命令

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
python3 --version
```
注意：不建议使用最新(或较新)的python版本，因为有些包可能还未适配最新版本的python

#### (2) 升级pip3
```bash
sudo apt-get install python3-pip            # 安装pip3
sudo pip3 install --upgrade pip             # 升级pip3
sudo gedit ~/.bashrc                        # 修改 .bashrc 文件
export PATH=/home/cxx/.local/bin/:$PATH     # 在文件末尾添加如下字段(cxx是用户名)
source ~/.bashrc                            # 保存文件后执行刷新调用
```
注意：这里升级pip3后，pip3的可执行文件位置可能发生变化，因此需要将新的可执行文件路径添加到环境变量中


#### (3) 一些python的依赖
```
pip3 install --user testresources           # 这个是安装报错后自己加的
pip3 install --upgrade numpy
pip3 install launchpadlib
pip3 install --user pygame numpy
pip install --user setuptools &&
pip3 install --user -Iv setuptools==47.3.1 &&
pip install --user distro &&
pip3 install --user distro &&
pip install --user wheel &&
pip3 install --user wheel auditwheel
```

#### (4) 一些需要提前安装的包
```
sudo apt-get update &&
sudo apt-get install wget software-properties-common &&
sudo add-apt-repository ppa:ubuntu-toolchain-r/test &&
wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add - &&
sudo apt-add-repository "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-8 main" &&
sudo apt-get update
```
以下指令不同ubuntu版本有所不同，具体细节查看[CARLA官方文档](https://carla.readthedocs.io/en/latest/build_linux/)
```bash
# ubuntu20.04
sudo apt-add-repository "deb http://apt.llvm.org/focal/ llvm-toolchain-focal main"
sudo apt-get install build-essential clang-10 lld-10 g++-7 cmake ninja-build libvulkan1 python python-dev python3-dev python3-pip libpng-dev libtiff5-dev libjpeg-dev tzdata sed curl unzip autoconf libtool rsync libxml2-dev git
sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/lib/llvm-10/bin/clang++ 180 &&
sudo update-alternatives --install /usr/bin/clang clang /usr/lib/llvm-10/bin/clang 180
```
anzhttp://blog.deskangel.com/2020/05/13/install-clang-on-ubuntu/

## 4. 安装UE4

#### (1) 将 github账号 与 Unreal Engine 账号 连接
安装虚幻引擎前需要将 github账号 与 Unreal Engine 账号 连接，具体方法参考：[Unreal Engine官方教程](https://www.unrealengine.com/en-US/ue-on-github)

#### (2) 去github的[epic games主页](https://github.com/EpicGames)，点击fallow

#### (3) 创建一个github 的 personal access token (classic)

创建流程参考[github文档](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

#### (4) 开始安装UE4：

运行以下链接会要求输入github的账户名和密码，刚刚创建的 personal access token (classic) 就是密码
```
git clone --depth 1 -b carla https://github.com/CarlaUnreal/UnrealEngine.git ~/UnrealEngine_4.26
```

#### (5) 编译UE4：
需要较长时间
```
cd ~/UnrealEngine_4.26./Setup.sh && 
./GenerateProjectFiles.sh && 
make
```

#### (6) 安装完成

## 5. 安装carla

carla有两种安装方法：Debian软件包安装、源码编译安装

### (1) Debian软件包安装：

####  ① 下载链接：
[从官方在github的发布中下载](https://github.com/carla-simulator/carla/releases) 或 [从carla中文站中下载](https://bbs.carla.org.cn/)

#### ②. 需要下载的文件（大概20G）：
```
[Ubuntu] CARLA_0.9.14.tar.gz
[Ubuntu] AdditionalMaps_0.9.14.tar.gz
[Ubuntu] CARLA_0.9.14_RSS.tar.gz
```
#### ③ 安装carla

将刚刚下载的安装包解压到安装目录，然后在终端中打开，运行：

```
pip install carla
pip3 install carla
```
注意：

 i. 这一步没有在[官方文档](https://carla.readthedocs.io/en/latest/build_linux/)中找到，是参照[博客](https://blog.csdn.net/m0_59161987/article/details/128928855)执行的，该博客说这个是官方给出的命令；

ii. 一瞬间就运行完，可以正常启动carla，但后续跑官方提供的example提示缺少的东西较多，不知道是否跟这个有关；

#### ④ 启动carla
启动命令相关可参考[CSDN：Carla 安装详细教程 —— Ubuntu 20.04 安装 Carla](https://blog.csdn.net/m0_59161987/article/details/128928855)
```
cd /home/mj/carla/CARLA_0.9.14
./CarlaUE4.sh -prefernvidia 
```

```
cd /home/mj/carla/CARLA_0.9.14
./CarlaUE4.sh -prefernvidia -quality-level=Low -benchmark -fps=15
```

注意：如果只执行 `./CarlaUE4.sh`可能无法启动carla，因为ubuntu默认使用核显，而carla需要独立显卡才能启动


### 6. 源码编译安装：

#### (1) 运行命令：
```
cd ~
git clone https://github.com/carla-simulator/carla
cd ~/carla
git checkout -b tags/0.9.14
./Update.sh
pip install --upgrade setuptools    # 报错后自己加的
make PythonAPI
make launch
```

#### (2) 如果网络好，安装过程中不会有什么问题，但如果网络不好，问题可能就比较多了

##### ① `git clone`失败，删掉clone的文件重新开始
##### ② `make PythonAPI`报错：

```
tar: Error is not recoverable: exiting now   
Util/BuildTools/Linux.mk:143: recipe for target 'setup' failed
```

原因是：网路波动导致文件下载失败，第二次运行检测到有这个文件就直接“编译”，然后“编译”失败了
    
[解决办法](https://github.com/carla-simulator/carla/issues/3428)：将`/carla/build`中损坏的文件或全部文件删除再重新运行`make PythonAPI`

#### (3) 运行一些例子
```
# Terminal A 
cd PythonAPI/examples
python3 -m pip install -r requirements.txt
python3 generate_traffic.py  

# Terminal B
cd PythonAPI/examples
python3 dynamic_weather.py 
```
注意：`python3 -m pip install -r requirements.txt`是安装 requirements.txt 文件中的一些包或依赖，如果报错，打开这个文件修改里面的版本即可
