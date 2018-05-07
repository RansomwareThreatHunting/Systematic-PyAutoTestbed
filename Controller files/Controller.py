import ControllerConf
import socket
import subprocess
import time
import shutil
import datetime
import os, errno
import zipfile

mal_log_dir = ""

def VM_Revert():

    write2LogFile("Pre Revert ")
    revert2snapshot = subprocess.Popen("%s -T ws revertToSnapshot %s %s" % (ControllerConf.VmManage_Path, ControllerConf.Vm_Path, ControllerConf.Snapshot_name))
    revert2snapshot.wait()
    write2LogFile("Revert Done ")
    time.sleep(2)

    write2LogFile("Pre Resume ")
    startVM = subprocess.Popen("%s -T ws start %s" % (ControllerConf.VmManage_Path, ControllerConf.Vm_Path))
    startVM.wait()
    write2LogFile("Resume new VM Done ")
    time.sleep(2)
    return True

def PrintLog(msg):
    datetime.datetime.now()
    print(str(datetime.datetime.now())+" | "+msg)

def Content_of_folder(path):
    "This Method Return Contents of a Folder as a List"
    Files = []
    Files=os.listdir(path)
    return  Files

def write2LogFile(message):

    log_file = open("%s\\%s" % (mal_log_dir, "controler_log.txt"), "a")
    try:
        log_file.write(message + " -time: " + log_time() + "\n")
    except:
        PrintLog("cant write to text file")
    try:
        log_file.close()
    except:
        PrintLog("cant close the text file")

def log_time():
    t = ""
    for i in range(3):
        t += str(time.localtime()[i]) + "/"
    t = t[0:len(t) - 1]
    t += " "
    for i in range(3, 7):
        t += str(time.localtime()[i]) + ":"
    t = t[0:len(t) - 1]
    return t

def dif_time_in_second(first_time , second_time):

    day = (second_time[2] - first_time[2]) * 24 * 60 * 60
    hour = (second_time[3] - first_time[3]) * 60 * 60
    minute = (second_time[4] - first_time[4]) * 60
    second = (second_time[5] - first_time[5])
    return (day+hour+minute+second)

def move2other_dir(src,dst):
    shutil.move(src , dst)

def renew_other_malware(Malware , malware_dst_name):
    if VM_Revert():
        move2other_dir(ControllerConf.Malwares_Resources_Path + "\\%s" % (Malware),
                        "%s\\%s\\%s" % (ControllerConf.Data_Base , malware_dst_name , Malware))

def make_directory(dir_path, dir_name):

    directory = dir_path + "\\" + dir_name
    if os.path.exists(directory):
        return True, directory
    try:
        os.makedirs(directory)
        return True, directory
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    return False, ""

def unzip(zip_file_path, zip_file_name):

    dir_maked, dir_path = make_directory(zip_file_path, "agent_log")
    zip_ref = zipfile.ZipFile("%s\\%s" %(zip_file_path, zip_file_name) , 'r')
    zip_ref.extractall(dir_path)
    zip_ref.close()
    os.remove("%s\\%s" %(zip_file_path, zip_file_name))

def List2Str(list, StrHeader):
    StrHeader += '*'.join(list)
    return StrHeader

def send_msg2agent(serversocket, msg):

    while True:
        try:
            serversocket.settimeout(60)
            Asocket, ad = serversocket.accept()
            break
        except:
            continue
    mssg = Asocket.recv(1024)
    St = mssg.decode('ascii')

    Asocket.send(msg.encode('ascii'))
    Asocket.close()

def send_conf2agent(serversocket):

    send_msg2agent(serversocket, "agent_conf_sending")
    PrintLog("agent conf sendig")

    if ControllerConf.AUPathes != {}:
        send_msg2agent(serversocket, List2Str(ControllerConf.AUPathes, "adds_upload"))

    send_msg2agent(serversocket, "convert_upload%s" % (ControllerConf.convertPML2CSV))
    send_msg2agent(serversocket, "shortcut_upload%s" % (ControllerConf.use_shortcut))
    send_msg2agent(serversocket, "monkey_upload%s" % (ControllerConf.use_monkey))
    send_msg2agent(serversocket, "ftp_user4D%s" % (ControllerConf.ftp_username4download))
    send_msg2agent(serversocket, "ftp_pass4D%s" % (ControllerConf.ftp_password4download))
    send_msg2agent(serversocket, "ftp_user4U%s" % (ControllerConf.ftp_username4upload))
    send_msg2agent(serversocket, "ftp_pass4U%s" % (ControllerConf.ftp_password4upload))
    send_msg2agent(serversocket, "test_time%s" % (ControllerConf.test_time))

    send_msg2agent(serversocket, "agent_conf_ended")
    PrintLog("agent conf ended")

def agent_Connection():

    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    # get local machine name
    host = ControllerConf.IP
    port = ControllerConf.Port

    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    # bind to the port
    serversocket.bind((host, port))
    # queue up to 5 requests
    serversocket.listen(5)

    newMalawre = 0
    oldMalware = 0
    start_time = time.localtime()

    print("====================================================================================")
    print("|                                                                                  |")
    print("|    This project is designed & developed in security laboratory at                |")
    print("|    Shiraz Univercity of Technology                                               |")
    print("|                                                                                  |")
    print("|    Team members: Sajad Homayoun, Hadi Mowla, Armin Aminian, Ali Dehghantanha     |")
    print("|                                                                                  |")
    print("====================================================================================\n")


    while True:
        if (len(Content_of_folder(ControllerConf.Malwares_Resources_Path)) == 0):
            PrintLog("END TEST")
            break

        if dif_time_in_second(start_time, time.localtime()) > (ControllerConf.time_out*60):
            renew_other_malware(Malware, "time_out")
            oldMalware += 1
            start_time = time.localtime()
            write2LogFile("time out")

        if oldMalware == newMalawre:
            Malware = Content_of_folder(ControllerConf.Malwares_Resources_Path).pop()
            newMalawre += 1
            PrintLog("\nRemained Samples: " + str(len(Content_of_folder(ControllerConf.Malwares_Resources_Path))))

        try:
            serversocket.settimeout(60)
            agent_socket, addr = serversocket.accept()
        except:
            continue

        msg = agent_socket.recv(1024)
        State = msg.decode('ascii')

        global mal_log_dir
        dir_maked = False
        if State == "Start":
            PrintLog(str(addr))
            PrintLog("Agent Is Alive")
            dir_maked , mal_log_dir = make_directory(ControllerConf.Data_Base + "\\Log", Malware[0:len(Malware) - 4])

        if State == "Start" or State == "END":
            PrintLog(State + " : " + Malware[0:len(Malware) - 4])
        else:
            PrintLog(State)

        message = State
        if State == "Start" or State == "END":
            message += " : " + Malware[0:len(Malware) - 4]

        write2LogFile(message)

        if(State=="Start"):
            Ml_State = Malware+"**"+"ReadyCopy"
            agent_socket.send(Ml_State.encode('ascii'))
            agent_socket.close()

            send_conf2agent(serversocket)

            start_time = time.localtime()
            continue

        elif(State=="CopyDone"):
            Msg="StartProcMon"
            agent_socket.send(Msg.encode('ascii'))

        elif(State == "Cant download file"):
            renew_other_malware(Malware , "connection_failed")
            oldMalware += 1

        elif (State == "Malware Launched FAILED"):
            renew_other_malware(Malware , "luanched_failed")
            oldMalware += 1

        elif(State=="END"):
            renew_other_malware(Malware , "done")
            if not ControllerConf.ziped_agent_log:
                unzip(mal_log_dir, "agent_log.zip")
            oldMalware += 1

        agent_socket.close()

agent_Connection()