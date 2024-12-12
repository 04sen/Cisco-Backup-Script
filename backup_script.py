# Copyright (c) [2024] Sachinandan Das Sen
# This file is part of Cisco-Backup-Script and released under the MIT license.
# See LICENSE.md for details or visit https://opensource.org/licenses/MIT.

import paramiko
import time
import datetime
import schedule
import os

# Cisco device information
cisco_device = {
    "host": " ", #Leave this blank cause Device IP/IPs will be in a .txt file
    "port": 22,
    "username": "your_username", #@TODO Enter the hostname of the Cisco Device
    "password": "your_password", #@TODO Enter the password of the Cisco Device
}

# Var to hold the name of the folder where backups are stored
# Must be same directory as the script.
folder = "backups" 

#Function to get the running configuration
def get_cisco_running_config(cisco_device):
    """
    Connect to the Cisco device and retrieve the running configuration.
    
    This function will establish an SSH connection to the Cisco device, open an
    interactive shell session, send a command to display the running
    configuration, receive the output, and then close the SSH connection.
    
    :param cisco_device: A dictionary containing the Cisco device's IP address,
        port number, username, and password.
    :return: The running configuration of the Cisco device as a string, or None
        if an error occurs.
    """
    try:
        # Establish an SSH connection to the Cisco device
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=cisco_device["host"],
            port=cisco_device["port"],
            username=cisco_device["username"],
            password=cisco_device["password"]
        )
        
        print("Connected to " + cisco_device["host"])
        
        # Generate a timestamp for the filename
        now = datetime.datetime.now().replace(microsecond=0).strftime("%Y-%m-%d_%H.%M.%S")
        
        # Generate the filename
        file_path = (now +  "_cisco_backup_" + cisco_device["host"] + ".cfg")
        print("File Path: " + file_path + "\n")
        
        # Open an interactive shell session
        remote_connection = ssh_client.invoke_shell()
        time.sleep(1)
        
        # Send the command to display the running configuration
        remote_connection.send("terminal length 0\n")
        time.sleep(1)
        
        # Send the command to copy the running configuration to a TFTP server
        remote_connection.send("copy run tftp\n")
        time.sleep(2)
        
        # Send the IP address of the TFTP server
        remote_connection.send("127.0.0.1\n") # @TODO change this IP to reflect TFTP Server IP
        time.sleep(2)
        
        # Send the filename
        remote_connection.send(file_path + "\n")
        time.sleep(2)
        
        # Receive the output
        output = remote_connection.recv(65535).decode("utf-8")
        
        # Close the SSH connection
        ssh_client.close()
        
        return output
    
    except Exception as e:
        print(f"Error fetching running config: {e}")
        return None
    


# function to perform delete operation based on condition 
def check_and_delete(folder): 
   """
   Check all files in the given folder and delete those that are older than N minutes/days/seconds.

   This function takes a folder path as an argument and iterates over all files in the folder.
   For each file, it calculates the difference between the current time and the time when the file
   was last modified. If this difference is greater than N minutes/days/seconds, the file is deleted.

   :param folder: The path to the folder to check
   """
   
   N = 0.5 # @TODO Change this to the number of minutes/ days /seconds as per your requirement

   print("...checking old files...\n")

   # loop to check all files one by one  
   # os.walk returns 3 things: current path, files in the current path, and folders in the current path  
   for (root,dirs,files) in os.walk(folder, topdown=True): 
        for f in files:   
            file_path = os.path.join(root,f)
            print(f"Checking file {file_path}")
            
            
            # get the timestamp, when the file was modified  
            timestamp_of_file_modified = os.path.getmtime(file_path) 
            
            # convert timestamp to datetime 
            modification_date = datetime.datetime.fromtimestamp(timestamp_of_file_modified) 
            
            #find the number of minutes/days/seconds when the file was modified 
            number_from_last_modified = (datetime.datetime.now() - modification_date).total_seconds() // 60
           
            """ Another option, look at the schedule documentation for more infomation """
            #number_from_last_modified = (datetime.datetime.now() - modification_date).days 
            
            # print the number of minutes/days/seconds when the file was modified
            print(f"File was modified {number_from_last_modified:.2f} minutes ago") # @TODO Change this message to Reflect your solution
         


            if number_from_last_modified > N:
               # remove the file  
               os.remove(file_path) 
               print(f" Deleted : {file_path}")

        print("...done...\n")  

def repeatable(cisco_device):
    """
    This function is designed to be run periodically to retrieve the running
    configuration from a list of Cisco devices.

    It opens a file named "hosts.txt" and reads the contents, which should be a
    list of IP addresses of Cisco devices. It then iterates over the list and
    calls the get_cisco_running_config function to retrieve the running
    configuration of each device.

    :param cisco_device: A dictionary containing the IP address, port number,
        username, and password of a Cisco device.
    """

    print("Starting backup")
    with open("hosts.txt","r") as hosts:
        IPs = hosts.readlines()

    for IP in IPs: 
        # Strip any whitespace from the IP address
        IP = IP.strip()
        print("Get Running Config from " + IP)

        # Update the cisco_device dictionary with the current IP address
        cisco_device["host"] = IP

        # Call the get_cisco_running_config function to retrieve the running
        # configuration of the current device
        get_cisco_running_config(cisco_device)

        # Pause for 2 seconds before retrieving the next device's configuration
        time.sleep(2)


# Main function
if __name__ == "__main__":
    schedule.every(0.5).minutes.do(repeatable, cisco_device=cisco_device)
    schedule.every(0.5).minutes.do(check_and_delete, folder=folder)
    
    """ Other Options for Scheduling, Look at the schedule documentation for more infomation"""
    #schedule.every().monday.at("08:00").do(repeatable, cisco_device=cisco_device)
    #schedule.every().monday.at("08:00").do(check_and_delete, folder=folder)
    

    while True:
        # Checks whether a scheduled task 
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)
