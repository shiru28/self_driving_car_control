# Installing CARLA Simulator
## Prerequisites
Following you can find the download links for CARLA Simulator:
[Ubuntu 16.04 or later]()
[Windows 7 or higher]()

### Hardware
Recommended hardware specifications (from the [Unreal Engine 4 Wiki](https://wiki.unrealengine.com/Recommended_Hardware#Recommended))
- Quad-core Intel or AMD processor, 2.5 GHz or faster
- NVIDIA GeForce 470 GTX or AMD Radeon 6870 HD series card or higher
- 8 GB RAM
- ~10GB of hard drive space for the simulator setup

## Setup for Ubuntu
### Firewall

CARLA requires networking enabled with the firewall allowing access to the CARLAloader, and by default [​port 2000, 2001 and 2002​](https://carla.readthedocs.io/en/stable/connecting_the_client/) (TCP and UDP) available on thenetwork. Generally [​Ubuntu's built-in firewall is disabled by default​](https://help.ubuntu.com/community/UFW), so you shouldn't need to worry about the firewall access for the CARLA Simulator.

You can also check this by running the command in a terminal:
```
$ sudo ufw status
```
, and confirm that the response is `Status: inactive`

If your network does not provide access to port 2000, you may change which portsare used at a later stage of the setup, just make note of the option ​here​ in the FAQsection when trying to run CARLA in server-client mode

### Python Ubuntu

The CARLA python client runs on ​[Python 3.5.x or Python 3.6.x](https://www.python.org/downloads/) (x is any number).Python 3.7 is not compatible with CARLA​. Note that it is assumed that ​pip​ is installed along with the installation of Python.

The setup guide uses the command ​python3​ to load all of its python clients. Make sure that the commands ​`python3`​ and ​`pip​` exists in `​/usr/bin`​, so they are readily accessible via terminal.

To check that ​python3​ points to the correct version, run the following bash commandin terminal:
```
$ python3 --version
```
It should return `​Python 3.5.x`​ or `​Python 3.6.x`​, as these are the versions supported by this version of CARLA.

Check whether pip is installed for Python 3.5 or Python 3.6
```
$ python 3 -m pip -- version
```
It should return with the pip version, as well as the Python version that it points to (inthe brackets). For example: ​pip 8.1.1 from ... (python 3.5)​, or somethingsimilar. Make sure that it points to the correct Python version: ​(python 3.5)​ or(python 3.6)

### Preparing the CARLA Simulator
#### Download and Extract CARLA Simulator
1. Download the CARLA simulator ([​CarlaUE4Ubuntu.tar.gz​](#Prerequisites)) found in the link mentioned above. Note that this may take a while as the simulator file is several gigabytes in size.

2. Extract the contents of `​CarlaUE4Ubuntu.tar.gz`​ to any working directory. The extraction will create a folder named ​CarlaSimulator​ in the working directory, which hosts the CARLA server and client files required for the project.

    The guide assumes the simulator is extracted to `​$HOME​/opt/CarlaSimulator​`.

    Continue with this step for extraction instructions, otherwise skip to the next step.

    **Ubuntu GUI method**
    
    Copy the ​`CarlaUbuntuUE4.tar.gz` ​file to the ​`opt​ `directory found under the homefolder. Create the `​opt` ​directory if it does not exist.

    Right click and extract the file contents into the current (​`opt`​) directory by clicking `Extract Here...​.`

    **Terminal method (alternative to using the Ubuntu GUI)**

    Run the following commands in a terminal to extract the simulator to `$HOME/opt`:
    ```
    $ cd <path/to/CarlaUE4Ubuntu.tar.gz>
    $ mkdir -p $HOME/opt # Ensures the opt directory exists
    $ tar -xzf CarlaUE4Ubuntu.tar.gz --directory $HOME/opt
    ```
#### Install Python Dependencies for Client
The CARLA Simulator client files requires additional dependencies to be installed, which are detailed inside the ​`$HOME​/opt/CarlaSimulator/requirements.txt`​ file.

To install these dependencies for your current user, run the following commands in terminal (you will need to be connected to the internet for this to work). ​Make sure that the version that `python3`​ points to is the correct [version](#python-ubuntu)​.
```
$ python3 -m pip install -r ​$HOME​/opt/CarlaSimulator/requirements.txt --user
```
There should be a `​Successfully installed ...`​ or ​`Requirement already satisfied` message at the end of the installation process when all of the requirements are successfully installed.

## Setup for Windows
### Firewall
CARLA requires networking enabled with the firewall allowing access to the CARLAloader, and by default [​port 2000, 2001 and 2002​](https://carla.readthedocs.io/en/stable/connecting_the_client/) (TCP and UDP) available on thenetwork. When you first run CARLA in server mode, Windows will prompt you to allow the application to access these ports if they are not ​already accessible​ on your system.

### Python Windows
The CARLA python client runs on [​Python 3.5.x or Python 3.6.x​](https://www.python.org/downloads/) (x is any number).Python 3.7 is not currently compatible with CARLA​. Note that it is assumed that pip​ is installed along with the installation of Python.

The setup guide uses the command ​`python​` to load all of its Python clients.

To check that `​python​` points to the correct version, run the following bash command in terminal:
```
\> python --version
```
It should return `​Python 3.5.x​` or `​Python 3.6.x`​, as these are the versions supported by this version of CARLA.

Check whether pip is installed for Python 3.5 or Python 3.6:
```
\> python -m pip --version
```
It should return with the pip version, as well as the Python version that it points to (in the brackets). For example: ​`pip 18.1 from ... (python 3.6)​`, or something similar.

### Preparing the CARLA Simulator
#### Download and Extract CARLA Simulator
1. Download the CARLA simulator (​CarlaUE4Windows.zip​) found in the reading page. Note that this may take a while as the simulator file is several gigabytes in size.

2. Extract the contents of ​[CarlaUE4Windows.zip](#Prerequisites)​ to any working directory. The extraction will create a folder named ​CarlaSimulator​ in the working directory, which hosts the CARLA server and client files required for the project.

    The guide assumes the simulator is extracted to ​`C:\CarlaSimulator​`.​ If `C:`​ is unavailable, you may replace ​`C:`​ with any other drive (for example ​`D:`​)

#### Install Python Dependencies for Client
The CARLA Simulator client files requires additional dependencies to be installed, which are detailed inside the ​`C:\CarlaSimulator\requirements.txt`​ file.

To install these dependencies for your current user, run the following commands in terminal (you will need to be connected to the internet for this to work). ​Make sure that the versionthat ​python​ points to is the correct [version](#python-windows).
```
\> python -m pip install -r C:\CarlaSimulator\requirements.txt --user
```
There should be a ​`Successfully installed ...`​ or ​`Requirement already satisfied` message at the end of the installation process when all of the requirements are successfully installed.

# Self-Driving Car Controller
Download the project by running the following commands:

**Ubuntu**
Navigate to the folder `$HOME/opt/CarlaSimulator/PythonClient` in the terminal and run the following command:
```
$ git clone https://github.com/shiru28/self_driving_car_control.git
```

**Windows**
```
\> cd C:\CarlaSimulator\PythonClient
\> git clone https://github.com/shiru28/self_driving_car_control.git
```

## Run CARLA Simulator
**Ubuntu:**
Navigate to the folder `$HOME/opt/CarlaSimulator` in the terminal and run the following command:
```
$ ./CarlaUE4.sh /Game/Maps/RaceTrack -windowed -carla-server -benchmark -fps=30
```

**Windows:**
```
\> cd C:\CarlaSimulator
\> CarlaUE4.exe /Game/Maps/RaceTrack -windowed -carla-server -benchmark -fps=30
```

## Run Controller
In anoher terminal, change the directory to go to "self_driving_car_control" folder, under the "PythoClient" folder and run the following command:

**Ubuntu:**
```
python3 carla_client.py
```

**Windows**
```
python carla_client.py
```