# Python script

This python script is here so simulate 3 sensors (temperature, humidity and pressure) and send them to linux server.

## Process

The script will generate random data for the 3 sensors every 5 seconds. The data are store in a csv. When its good, it hash the csv for the integrity, store it in a txt file, compress the csv and the txt file and send them to the server via sftp.

## Packages

- hashlib: to hash
- paramiko: to connect to the server via ssh
- csv: to write the data in a csv file
- time: to wait between each data
- datetime: to get the date and time
- random: to generate random data
- os: Operating System interface
- shutil: to do file operations

## Installation

To install the packages, you need to use pip:

```bash
pip install paramiko
```

All other packages are already installed with python.


After that, you can create your RSA key used to encrypt the csv file:

```bash
 ssh-keygen -t rsa -b 2048 -m PEM  -f key/id_rsa
```

### Warning
To work with the server you need to give your ssh public key to the server admin.
If you already do that, you can go in weather.py and at line `73` change the path of the private key used for the ssh connection.

## Usage

To run the script, you need to use python:

```bash
python3 weather.py
```
