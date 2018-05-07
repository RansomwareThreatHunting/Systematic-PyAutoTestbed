#The Server's IP Address
IP = "192.168.124.137"
# Server's Port
Port = 6666
# Path of Malware Resources
Malwares_Resources_Path = "C:\\Users\\HD\\Documents\\Malware\\Resources"
#Path of folders like: resoursec, logs, done, ...
Data_Base = "C:\\Users\\HD\\Documents\\Malware"
#Name of Vm
Vm_Path = "C:\\VMs\\Win10\\Win10.vmx"
#Snapshot Name
Snapshot_name = "S20"
#VmMange's Path
VmManage_Path = "C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe"

#===============================================================
# set true to be zipped log otherwise false
ziped_agent_log = True

# if test doesn't finish after this time , the test terminate and start new test
time_out = 12 #in minute
# the time that software is tested
test_time = 30 #in second
#list of files and folders that need to be uploaded by agent
AUPathes = {}
# AUPathes = {"C:\\Users\\robo\\Desktop\\A"
#             , "C:\\Users\\robo\\Desktop\\d.txt"}
# set ture to use pywinmonkey
use_monkey = False
# set true to use software shortcuts in Launcher
use_shortcut = False
# set true to convert test's result to CSV (Both PML and CSV will be uploaded)
convertPML2CSV = True
ftp_username4download = 'Malware'
ftp_password4download = '123456'
ftp_username4upload = 'Logs'
ftp_password4upload = '123456'