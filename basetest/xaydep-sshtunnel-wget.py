# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import paramiko
from sshtunnel import SSHTunnelForwarder
import time
import logging
now_time = time.strftime("%Y-%m-%d-%H-%M", time.localtime())


###remote forward host config Definition###
Remote_For_Host='XX'
Remote_For_User='root'
Remote_For_Pass='XXX'
Remote_For_Port=22

###remote host config Definition --- real server#####
Remote_Host='XX'
Remote_User='root'
Remote_Pass='XX'
Remote_Port=22

#####包名和服务名####
War_name = "admin.war"
Ser_name = "admin"

#Local_War=os.path.join(os.getenv("WORKSPACE"),War_name)
# Local_War=os.path.join(Local_path,War_name)

###包下载####
Wget_war_url='wget XXXXXXXXXXX '

###jenkins config
# Project_down_Parentpath="/var/www/download-war/admin-2"
# War_down_direc=os.path.join(Project_down_Parentpath,now_time)

######remote path####
Remote_upload_file="/home/data/upload/admin.war"
Remote_file_path='/home/data/tomcats/tomcat8080/webapps/admin'
Remote_file_war='/home/data/tomcats/tomcat8080/webapps/admin.war'
Remote_bak_path='/home/data/bak/'


###remote service #####
tomcat_bin_path = "/home/data/tomcats/tomcat8080/bin/startup.sh"
service_command = "ps -ef | grep tomcat | grep 8080| grep -v grep"
pid_command = "ps aux | grep tomcat | grep 8080 | grep -v grep | awk '{print $2}'"


def remoteforwordhost():
    global remoteserver
    remoteserver = SSHTunnelForwarder(
        ssh_address_or_host=(Remote_For_Host, Remote_For_Port),
        ssh_username=Remote_For_User,
        ssh_password=Remote_For_Pass,
        remote_bind_address=(Remote_Host, Remote_Port)
    )


###ssh 传输太慢。使用http的wget#####
def remoterealhost():
    remoteserver.start()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname='127.0.0.1',
        port=remoteserver.local_bind_port,
        username=Remote_User,
        password=Remote_Pass
    )
    #stdin, stdout, stderr = ssh.exec_command('ls ' + Remote_file_path)  #exec_command返回的为tunple，第二个为stdout
    if ssh.exec_command('ls ' + Remote_file_path)[1].read():
        if ssh.exec_command(service_command)[1].read():
            ssh.exec_command('cp -r ' + Remote_file_path + ' ' + Remote_bak_path +  Ser_name + '_' + now_time)
            ssh.exec_command('kill -9 ' + ssh.exec_command(pid_command)[1].read())
            ssh.exec_command('rm -rf ' + Remote_file_path + '*')
            ###此处必须捕捉输入，不然执行就是直接进行到下一行命令，会造成下载不完整，坑了2个小时
            stdin, stdout, stderr = ssh.exec_command(Wget_war_url + ' -O ' + Remote_upload_file)
            print("stdout: ",stdout.read())
            print("stderr: ",stderr.read())
            stdin, stdout, stderr =ssh.exec_command('mv ' + Remote_upload_file + ' ' + Remote_file_war )
        else:
            stdin, stdout, stderr = ssh.exec_command('cp -r ' + Remote_file_path + ' ' + Remote_bak_path +  Ser_name + '_' + now_time)
            ssh.exec_command('kill -9 ' + ssh.exec_command(pid_command)[1].read())
            ssh.exec_command('rm -rf ' + Remote_file_path + '*')
            stdin, stdout, stderr = ssh.exec_command(Wget_war_url + ' -O ' + Remote_upload_file)
            print("stdout: ",stdout.read())
            print("stderr: ",stderr.read())
            stdin, stdout, stderr = ssh.exec_command('mv ' + Remote_upload_file + ' ' + Remote_file_war)
            print(stdout.read())
    else:
        print('the war path not exist,please login server checkout')
    ##service check####
    if ssh.exec_command(service_command)[1].read():
        logging.warn("the tomcat8080 service is running, need to restart")
        ssh.exec_command('kill -9 ' + ssh.exec_command(pid_command)[1].read())
        stdin,stdout,stderr = ssh.exec_command('source /etc/profile && /bin/bash ' + tomcat_bin_path)
        print(stdout.read())
    else:
        logging.warn("the tomcat8080 service stop, to start tomcats")
        stdin, stdout, stderr = ssh.exec_command('source /etc/profile && /bin/bash ' + tomcat_bin_path)
        print(stdout.read())
    ssh.close()
    remoteserver.close()


if __name__ == '__main__':
    remoteforwordhost()
    remoterealhost()


