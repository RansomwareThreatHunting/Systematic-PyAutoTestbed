import LauncherConf
import socket
import FtpAgent
import subprocess
import time
import shutil
import win32gui, win32con
import win32com.client
# libs for monkey
import PyWinMonkeyLib, threading, pyautogui, win32api


pid = 0

def ServerConnection(State):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = LauncherConf.IP
    port = LauncherConf.Port
    while True:
        try:
            s.connect((host, port))
            break
        except:
            continue

    s.send(State.encode('ascii'))
    msg = s.recv(1024)
    ServerMessage = msg.decode('ascii')
    s.close()
    return ServerMessage


def Start_State():
    return ServerConnection("Start")

def Download_from_ftp(Malware):
    ServerConnection("Start Downloading")
    return FtpAgent.grabFile(Malware)

def Upload_to_ftp_LogZip(Malware):
    ServerConnection("Start Uploading Log Zip")
    return FtpAgent.placeFile_LogZip(Malware)

def MsgSpliter(msg):
    List_msg = []
    List_msg = msg.split("**")
    return List_msg

def get_shortcut_target(shortcutpath,shortcutname):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut('%s/%s' % (shortcutpath, shortcutname))
    return shortcut.Targetpath

def Test_Start(Malware):
    global pid
    Sleep_time = LauncherConf.test_time
    open_proc = subprocess.Popen(
        '%s /BackingFile %s/%s.PML' % (LauncherConf.Procmon_Path, LauncherConf.LogFile_Path, Malware[0:len(Malware) - 4]))
    time.sleep(5)
    # minimize procmon---------------------------------------------------------------------
    time.sleep(2)
    minimize = win32gui.GetForegroundWindow()
    print("should be procmon: " + win32gui.GetWindowText(minimize))
    win32gui.ShowWindow(minimize, win32con.SW_MINIMIZE)
    # -------------------------------------------------------------------------------------
    ServerConnection("ProcMon Launched")

    try:
        malware_path = '%s/%s' % (LauncherConf.Malwares_Resources_Path, Malware)
        if LauncherConf.use_shortcut:
            malware_path = '%s' %(get_shortcut_target(LauncherConf.Malwares_Resources_Path, Malware))
            write2LogFile("shortcut path: " + malware_path)

        process = subprocess.Popen(malware_path)
        time.sleep(5)
        ServerConnection("Malware Launched")
    except:
        time.sleep(30)
        ServerConnection("Malware Launched FAILED")
        ServerConnection("END")
        exit()
    pid = process.pid
    #monkey================================
    if LauncherConf.use_monkey:
        write2LogFile("come into monkey")
        pyautogui.click(win32api.GetSystemMetrics(0) / 2, win32api.GetSystemMetrics(1) / 2)
        window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        write2LogFile("should be window title: " + window_title)
        t = threading.Thread(target=PyWinMonkeyLib.GoSimulate, args=(window_title, int(Sleep_time/2), 5, False))
        t.start()
        threading._shutdown()
    #======================================
    time.sleep(Sleep_time)
    ServerConnection("Process finished")
    terminate_proc = subprocess.Popen('%s /Terminate' % (LauncherConf.Procmon_Path))
    terminate_proc.wait()

    if LauncherConf.convertPML2CSV:
        convert2csv = subprocess.Popen('%s /OpenLog %s\\%s.PML /SaveAs %s\\%s.csv' % (
            LauncherConf.Procmon_Path, LauncherConf.LogFile_Path, Malware[0:len(Malware) - 4], LauncherConf.LogFile_Path,
        Malware[0:len(Malware) - 4]))
        convert2csv.wait()
        ServerConnection("PML Converted to csv")

    return True


def exactname():
    global pid
    out = subprocess.check_output("C:\\Windows\\System32\\wbem\\WMIC.exe process where processID=%d get name" % (pid))
    return (''.join(out.decode('ascii').split()))[1]

def move2other_dir(src,dst):
    shutil.move(src , dst)

def write2LogFile( message):

    log_file = open("%s\\%s" % (LauncherConf.LogFile_Path, "debug.txt"), "a")
    try:
        log_file.write(message + "\n")
    except:
        print("aaa")
    try:
        log_file.close()
    except:
        print("bbb")

def get_conf_from_server():

    write2LogFile("before get conf msg")
    conf_msg = ServerConnection("a")
    write2LogFile("conf_msg: " + conf_msg)

    if conf_msg == "agent_conf_sending":
        write2LogFile("is if conf_msg")

        while conf_msg != "agent_conf_ended":
            conf_msg = ServerConnection("a")
            write2LogFile("conf_msg: " + conf_msg)

            if conf_msg[0:11] == "adds_upload":
                LauncherConf.dir4uplaod = conf_msg[11:].split("*")
                write2LogFile("adds upload: %s" % LauncherConf.dir4uplaod)

            elif conf_msg[0:14] == "convert_upload":
                if conf_msg[14:] == "False":
                    LauncherConf.convertPML2CSV = False
                else:
                    LauncherConf.convertPML2CSV = True

            elif conf_msg[0:15] == "shortcut_upload":
                if conf_msg[15:] == "True":
                    LauncherConf.use_shortcut = True
                else:
                    LauncherConf.use_shortcut = False

            elif conf_msg[0:13] == "monkey_upload":
                if conf_msg[13:] == "True":
                    LauncherConf.use_monkey = True
                else:
                    LauncherConf.use_monkey = False
            elif conf_msg[0:10] == "ftp_user4D":
                LauncherConf.ftp_username4download = conf_msg[10:]

            elif conf_msg[0:10] == "ftp_pass4D":
                LauncherConf.ftp_password4download = conf_msg[10:]

            elif conf_msg[0:10] == "ftp_user4U":
                LauncherConf.ftp_username4upload = conf_msg[10:]

            elif conf_msg[0:10] == "ftp_pass4U":
                LauncherConf.ftp_password4upload = conf_msg[10:]

            elif conf_msg[0:9] == "test_time":
                LauncherConf.test_time = int(conf_msg[9:])


FirstStateMessage = Start_State()
MessageList = MsgSpliter(FirstStateMessage)
isDownloaded = False

get_conf_from_server()

if MessageList[1] == "ReadyCopy":
    isDownloaded = Download_from_ftp(MessageList[0])

if (isDownloaded):
    ServerConnection("CopyDone")
    if (Test_Start(MessageList[0])):

        for i in LauncherConf.dir4uplaod:
            move2other_dir(i, LauncherConf.LogFile_Path)
        if (Upload_to_ftp_LogZip(MessageList[0])):
            ServerConnection("END")
            exit()
else:
    ServerConnection("Cant download file")
    exit()
