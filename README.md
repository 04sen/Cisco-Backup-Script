# Cisco Device Configuration Backup Script

## Overview

This Python script automates the backup of running configurations for Cisco network devices using SSH and TFTP. It provides scheduled configuration retrieval and old backup file management.

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



## Project Structure

```
cisco-backup-script/
│
├── backups/                  # Directory for storing 
│   └── (backup files will be stored here)
│
├── hosts.txt                 # List of Cisco device IP addresses
│
├── backup_script.py          # Main Python script for device backup
│
├── README.md                 # Project documentation
|
└── LICENSE                   # MIT License file
```

### Directory and File Descriptions

- `backups/`: 
  - Default directory for storing configuration backups
  - Automatically created by the script
  - Configuration files are saved here with timestamps

- `hosts.txt`:
  - Plain text file containing IP addresses of Cisco devices
  - One IP address per line
  - Used by the script to iterate through devices for backup

- `backup_script.py`:
  - Main Python script
  - Handles SSH connections
  - Manages backup process
  - Implements scheduling and file cleanup


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cisco-backup-script.git
   cd cisco-backup-script
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

I used TFTP because it was very easy to start a Server on my Laptop using TFTPD64. I have added a setup guide for Windows and Linux below.

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

### Please Note: 

The Idea is to have this script running indefinitely on a lightweight device and/or Server connected to the network.

You will need to restart the Script if the device reboots. 

## Scheduling Options
The script supports multiple scheduling configurations:
- Current default: Runs every 0.5 minutes
- Commented examples include:
  - Running every Monday at 08:00
  - Customizable time-based schedules

Please vist the [Scheduling Documentation](https://schedule.readthedocs.io/en/stable/) for more Infomation.

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

Distributed under the MIT License. See [LICENSE](LICENSE.md) for more information.

## Contact

Sachinandan Das Sen - s.sen04@icloud.com
