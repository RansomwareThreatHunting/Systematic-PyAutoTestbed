<h1>
    Systematic-PyAutoTestbed
</h1>
<p>
    &emsp; In this project, we introduce Systematic-PyAutoTestbed as an automatic
    system to launch any executable application in an isolated environment. The
    system has the capability of launching and predetermined software such as
    “Process Monitor” to record all activities performed by the target
    application. It worth noting that our system also has the ability of
    working with other logger software while it also can be used to automate
    any task for generating logs in the same environment.
	<br/>&emsp; The first time, this project is used to record behavioral logs of more than
    4000 Ransomware in “
    <a href="http://ieeexplore.ieee.org/document/8051108/">
        Know Abnormal, Find Evil: Frequent Pattern Mining for Ransomware Threat
        Hunting and Intelligence
    </a>
    ”.
	<br/>&emsp; In cases of applying Systematic-PyAutoTestbed for detecting malicious
    behaviors of applications, the output can be used for sequential pattern
    mining algorithms to find useful patterns/signatures for malware detection.
	<br/>&emsp; Our system speeds up the analyzing procedure to achieve a more accurate
    pattern by performing more experiments. Moreover, Systematic-PyAutoTestbed
    provides the possibility of performing several experiments in the same
    environment with similar configuration.
	<br/>&emsp; This is a Server-Client (Controller-Launcher) system in which clients are
    controlled in an isolated environment Client, and download the application
    from the shared file server or database. The client launches the downloaded
    application to capture its behavior for a predetermined time. It finally
    uploads recorded logs to the server (Controller) for storing in logs
    repository. After finishing an experiment, Controller reverts the virtual
    machine environment to its original state (snapshot).
</p>

<p>
    <h3>&ensp;1. How to implement Systematic-PyAutoTestbed (Simple Architecture)</h3>
    &emsp; In this simple architecture, it needs a Windows Host to be Server and
    Client.
	<br/>The client is a Virtual Machine on Host and Host is Server
</p>

<p>
    <h4>&ensp;1.1. Server (Host)</h4>
    <strong>Step1.</strong>
    Install Python 3.6 and an IDE
	<br/><strong>Step2.</strong>
    Install VMware Workstation
	<br/>&emsp; • Deploy a Virtual Machine and Install a Windows OS on it as Client
	<br/><strong>Step3. </strong>
    Install a FTP Server (Recommend Xlight FTP Server)
	<br/><strong>Step4.</strong>
    Create these folders in the desired Path
	<br/>&emsp; • Resources: the repository of “Samples” that will be tested
	<br/>&emsp; • Done: the repository of “Samples” that be successfully tested
	<br/>&emsp; • Log: the repository of tests’ results
	<br/>&emsp; • Launched_fail: the repository of “Samples” that can’t run on the Client
	<br/>&emsp; • Connection_fail: the repository of “Samples” can’t be transferred from
    Server to Client
	<br/>&emsp; • Time_out : the repository of “Samples” that can’t run on determinate time
	<br/><strong>Step5.</strong>
    Put the “Samples” that you want to be tested in “Resources” Folder
</p>

<p>
    <h4>&ensp;1.2. Client</h4>
    <strong>Step1.</strong>
    Install Python 3.6
    <br/><strong>Step2.</strong>
    Create these folders in the desired Path (Optional but Recommended)
	<br/>&emsp; • Log: the repository of test result
	<br/>&emsp; • Procmon: the location of “Process Monitor”
	<br/>&emsp; • Launcher: the location of “Launcher Code”
</p>

<p>
  <h3>2. Configurations</h3>
    <h4>&ensp;2.1. Server Configuration</h4>
    <strong>Step1. </strong>
    Create a Virtual Server in FTP Server
	<br/>&emsp; • Create two Users in FTP Server:
	<br/>&emsp; &ensp; - The Home Folder of a User is “Log Folder” that is mentioned above
	<br/>&emsp; &ensp; - The Home Folder of another User is “Resources Folder” that is mentioned
    above
	<br/><strong>Step2. </strong>
    We recommend that a Static IP used for Server (This IP be used in Launcher
    and Controller Code)
	<br/><strong>Step3. </strong>
    Configuration of ControllerConf:
	<br/>&emsp; • Configure this file base on your needs and configurations
	<br/>In addition, for decreasing the time of software transfer between FTP
    Server and Launcher and testing the software that needs to install, this
    project can use shortcut of software (this ability will be introduced
    later)
</p>

<p>
    <h4>&ensp;2.2. Client Configuration</h4>
    <strong>Step1.</strong>
    The Client’s IP Address must be set
	<br/><strong>Step2.</strong>
    LauncherConf Configuration:
	<br/>&emsp; • Configure this file base on your needs and configurations
	<br/><strong>Step3.</strong>
    Close the Folders and then run “Launcher.py” in CMD
	<br/><strong>Step4.</strong>
    Take a Snapshot
</p>

<p>
    <h3>&ensp;3. How to Run Project</h3>
	<strong>Step1.</strong>
    Run the FTP Server
	<br/><strong>Step2.</strong>
    Turn on Client’s Virtual machine from Snapshot that was taken
	<br/><strong>Step3.</strong>
    Run the Controller.py
</p>

<p>
    <strong>Notes:</strong>
	<br/>&ensp;If you are going to use “Pywinmonkey”, you can download the latest version
    from github. You must copy it to the Launcher Code Folder and install its
    required Libs.
	<br/>&ensp;This project is designed and developed in SutechLab at Shiraz University of
    Technology.
</p>

<h5>Supervisor:</h5>
<ul>
  <li><a href="https://ir.linkedin.com/in/sajad-homayoun-0a286354">Dr. Sajad Homayoun</a>, (sajadhomayoun@gmail.com, s.homayoun@sutech.ac.ir) </li>
</ul>
<h5>Design and develop:</h5>
<ul>
  <li><a href="https://www.linkedin.com/in/hadi-mowla-667695144">Hadi Mowla</a>, (hadi.mowla@outlook.com)</li>
  <li><a href="https://www.linkedin.com/in/armin-aminian-242607bb/">Armin Aminian</a>, (armin.shadow.sdw@outlook.com)</li>
  <li><a href="https://ir.linkedin.com/in/sajad-homayoun-0a286354">Dr. Sajad Homayoun</a>, (sajadhomayoun@gmail.com, s.homayoun@sutech.ac.ir)</li>
</ul>
<h5>Advisors:</h5>
<ul>
  <li><a href="https://www.linkedin.com/in/alide/">Dr. Ali Dehghantanha</a>, (dehqan@gmail.com)</li>
  <li><a href="https://www.linkedin.com/in/marzieh-ahmadzadeh-22574428/">Dr. Marzieh Ahmadzadeh</a>, (ahmadzadeh@sutech.ac.ir)</li>
  <li><a href="http://sess.shirazu.ac.ir/sess/fresearch/FacultyCV.aspx?OP=Code=149770;">Dr. Sattar Hashemi</a>, (s_hashemi@shirazu.ac.ir)</li>
  <li><a href="https://www.linkedin.com/in/raouf-khayami-017281147">Dr. Raouf Khayami</a>, (khayami@sutech.ac.ir)</li>
  <li><a href="https://ir.linkedin.com/in/reza-akbari-a2237b126">Dr. Reza Akbari</a>, (akbari@sutech.ac.ir)</li>
</ul>
