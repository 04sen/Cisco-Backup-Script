# Cisco Device Configuration Backup Script

## Overview

This Python script automates the backup of running configurations for Cisco network devices using SSH and TFTP. It provides scheduled configuration retrieval and dynamically deletes old backup files. 

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [TFTP Server Setup](#tftp-server-setup)
  - [Option 1: TFTPD64 (Recommended for Windows)](#option-1-tftpd64-recommended-for-windows)
  - [Option 2: Linux TFTP Server](#option-2-linux-tftp-server)
- [Configuration](#configuration)
  - [Device Credentials](#device-credentials)
  - [Backup Location](#backup-location)
  - [Hosts](#hosts)
  - [TFTP Configuration](#tftp-configuration)
  - [Backup Retention](#backup-retention)
- [Usage](#usage)
  - [Running the Script](#running-the-script)
   - [Scheduling Options](#scheduling-options)
   - [Testing the Script](#testing-the-script)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

- [License](#license)
- [Contact](#contact)

## Features

- Automated SSH connection to Cisco devices
- Periodic configuration backup
- TFTP-based configuration transfer
- Automatic old backup file deletion
- Configurable backup and deletion intervals

## Prerequisites

### Hardware
- Cisco network device(s) with SSH access
- TFTP server

### Software
- Python 3.x
- Required Python packages:
  - paramiko
  - schedule
  - datetime


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cisco-backup-script.git
   ```

2. Install required dependencies:
   ```bash
   pip install paramiko schedule datetime os time
   ```

   Full list of dependencies:
   - `paramiko`: SSH connection library
   - `schedule`: Task scheduling library
   - `datetime`: Date and time manipulation
   - `os`: Operating system interactions
   - `time`: Time-related functions

## TFTP Server Setup

### Option 1: TFTPD64 (Recommended for Windows)
1. Download TFTPD64 from the official website:
   [TFTPD64 Website.](https://pjo2.github.io/tftpd64/)

2. Installation steps:
   - Download the latest release
   - Extract the zip file
   - Run `tftpd64.exe` as an administrator
   - Configure the TFTP server directory
   - Ensure the directory is accessible and has appropriate permissions

### Option 2: Linux TFTP Server
For Linux systems, use the standard tftp-hpa server:
```bash
sudo apt-get update
sudo apt-get install tftpd-hpa
sudo systemctl enable tftpd-hpa
sudo systemctl start tftpd-hpa
```

## Configuration

### Device Credentials
1. Open the script and modify the `cisco_device` dictionary:
   ```python
   cisco_device = {
       "host": "",  # Leave blank, will be populated from hosts.txt
       "port": 22,
       "username": "your_username", #@TODO Enter the hostname of the Cisco Device
       "password": "your_password" #@TODO Enter the password of the Cisco Device
   }
   ```

### Backup Location
1. Modify the `folder` variable to the location / name of the folder where all the backups will be saved:
   ```
   folder = "backups"
   ```

### Hosts
1. Modify the `hosts.txt` file with one Cisco device IP per line:
   ```
   192.168.1.1
   192.168.1.2
   10.0.0.1
   ```

### TFTP Configuration
1. Update the TFTP server IP in the script:
   ```python
   remote_connection.send("127.0.0.1\n")  # @TODO change this IP to reflect TFTP Server IP
   ```

### Backup Retention
1. Modify the `N` variable in `check_and_delete()` to set backup retention time:
   ```python
   N = 0.5  # @TODO Change this to the number of minutes/ days /seconds as per your requirement
   ```

## Usage

### Running the Script
```bash
python backup_script.py
```

### Scheduling Options
The script supports multiple scheduling configurations:
- Current default: Runs every 0.5 minutes
- Commented examples include:
  - Running every Monday at 08:00
  - Customizable time-based schedules

Please vist the [Scheduling Documentation](https://schedule.readthedocs.io/en/stable/) for more Infomation.

### Please Note: 

The Idea is to have this script running indefinitely on a lightweight device and/or Server connected to the network.
You will need to restart the Script if the device reboots. 

## Testing The Script

It is recommened to use a physical Cisco-ios device however you can also access the [Cisco Sandbox](https://developer.cisco.com/site/sandbox/) and use one of the Always-on devices to test the script. 

I recommened using the **IOS XE on Cat8kv AlwaysOn** device as it has given me the most consistency. 

### Please Note:
If using the Cisco Sandbox, the IP, username and password must reflect whats provided by Cisco. 

## Troubleshooting

- Ensure SSH and TFTP ports are open
- Verify network connectivity
- Check device credentials
- Confirm TFTP server is running and accessible
- Verify Python dependencies are correctly installed

## Contributing

### Future Development

**Seeking Contributions!** The project is currently exploring migration from TFTP to SFTP for more secure file transfers. Community contributions are highly welcome to help implement this feature.

We especially welcome contributions related to:
- SFTP implementation
- Security enhancements
- Cross-platform compatibility

#### Current Limitations
- Uses TFTP for file transfer
- Potential security risks with current transfer method
- Limited error handling for network issues

#### Contribution Process:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Additional Notes for Contributors
- Prioritize security in all modifications
- Maintain backward compatibility where possible
- Add comprehensive error handling


## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Contact

Sachinandan Das Sen - s.sen04@icloud.com
