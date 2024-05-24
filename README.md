This is project is an AI assistant satelite, that can access any OpenAI API compliant language model both remotely and locally thanks to NordVPN's Meshnet, Ollama and Vosk.

##Requirements
### Ollama
Consider running Ollama in a Docker container with GPU support. Ollama containers works very well through WSL.
Install the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation)

> Note: You can skip to the Container section if you will not be running Ollama with a Nvidia GPU.
1. Configure the repository
```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
    | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
    | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
    | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
```
2. Install the NVIDIA Container Toolkit packages
```
sudo apt-get install -y nvidia-container-toolkit
```
3. Configure Docker to use the Nvidia driver
```
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### Container
1. Start the container

With GPU support:
```
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```
CPU only:
```
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

2. Download and interact with the model
```
docker exec -it ollama ollama run llama3
```
There are other models available. See the official Ollama repository - [Ollama/Ollama](https://github.com/ollama/ollama?tab=readme-ov-file#model-library)

3. Exit the interactive shell
```
/bye
```

### NordVPN Meshnet

#### Satelite - Linux
1. Install NordVPN on the satellite device - Raspberry Pi 4B in my case
[Installing NordVPN on Linux distributions](https://support.nordvpn.com/hc/en-us/articles/20196094470929-Installing-NordVPN-on-Linux-distributions)
2. Log in
[How to log in to NordVPN on Linux devices without a GUI](https://support.nordvpn.com/hc/en-us/articles/20226600447633-How-to-log-in-to-NordVPN-on-Linux-devices-without-a-GUI)
4. Enable Meshnet
[Using Meshnet on Linux](https://meshnet.nordvpn.com/getting-started/how-to-start-using-meshnet/using-meshnet-on-linux)

#### Host - Windows
1. Installing NordVPN on the host device - Windows 10 in my case
[Installing and using NordVPN on Windows 10 and 11](https://support.nordvpn.com/hc/en-us/articles/19472023025169-Installing-and-using-NordVPN-on-Windows-10-and-11)
2. Log in
3. Enable Meshnet
[Using Meshnet on Windows](https://meshnet.nordvpn.com/getting-started/how-to-start-using-meshnet/using-meshnet-on-windows)

### Python
1. Install Miniconda
[Latest Miniconda installer links](https://docs.anaconda.com/free/miniconda/index.html)
2. Create a new Conda environment that has Python3.9 installed
```
conda create --name vosk python=3.9
```
3. Activate vosk environment
```
conda activate vosk
```

### Repository
1. Clone the repository
```
git clone 