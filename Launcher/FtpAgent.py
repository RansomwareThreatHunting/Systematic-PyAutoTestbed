from ftplib import FTP
import LauncherConf
import time
import os
import shutil

def grabFile(filename):
    for i in range(5):
        try:
            ftp = FTP(LauncherConf.IP)
            ftp.login(user=LauncherConf.ftp_username4download, passwd=LauncherConf.ftp_password4download)
            localfile = open(LauncherConf.Malwares_Resources_Path + "\\" + filename, 'wb')
            ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
            break
        except:
            if i == 4:
                return False
            time.sleep(5)
            continue
    time.sleep(2)
    ftp.quit()
    localfile.close()
    return True;
# ------------------------------------------------------------#

def placeFile_LogZip(Malware):
    os.chdir(LauncherConf.LogFile_Path)
    os.chdir('..')
    shutil.make_archive("%s\\agent_log" % (os.getcwd()), 'zip', LauncherConf.LogFile_Path)
    ftp = FTP(LauncherConf.IP)
    ftp.login(user=LauncherConf.ftp_username4upload, passwd=LauncherConf.ftp_password4upload)
    ftp.cwd(Malware[0:len(Malware) - 4])
    filename = os.getcwd() + "\\agent_log.zip"
    ftp.storbinary('STOR ' + "agent_log.zip" , open(filename, 'rb'))
    ftp.cwd('..')
    ftp.quit()
    return True
