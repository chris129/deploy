# -*- coding: utf-8 -*-
import paramiko
import time
import os
import logging
now_time = time.strftime("%Y-%m-%d-%H-%M", time.localtime())



###主机集群配置#####
Remote_host1 = {'Remote_Host':'XXX','Remote_User':'root','Remote_Pass':'XXX','Remote_Port':2222}
Remote_host2 = {'Remote_Host':'XXX','Remote_User':'root','Remote_Pass':'XXX','Remote_Port':2222}



####local file Definition####
##WORKSPACE是直接到代码目录下的，例如/var/lib/jenkins/workspace_test/hardware-app#####
##/var/lib/jenkins/workspace/xahl/admin/target/admin.war
#Local_path = os.getenv("WORKSPACE")
#Local_path = "/var/lib/jenkins/workspace/xahl"


###发布包存放位置
Local_path="../sources/pre-pc/"
##定义war包的名称
#War_name = os.getenv('service_name')
Zip_name = "dist.zip"
Ser_name = "dist"



#Local_War=os.path.join(os.getenv("WORKSPACE"),War_name)
Local_zip=os.path.join(Local_path,Zip_name)


###jenkins config
# Project_down_Parentpath="/var/www/download-war/admin-2"
# War_down_direc=os.path.join(Project_down_Parentpath,now_time)

######remote path 相关上级目录需要提前建好####
Remote_upload_file="/usr/local/nginx/uploadpath/dist.zip"
Remote_file_parentpath='/usr/local/nginx/html/zufangguanli-pc/'
Remote_file_path='/usr/local/nginx/html/zufangguanli-pc/dist'
Remote_file_zip='/usr/local/nginx/html/zufangguanli-pc/dist.zip'
Remote_bak_path='/usr/local/nginx/html/zufangguanli-pc/bak/'




def remotedeploy(remotehostconfig):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=remotehostconfig['Remote_Host'],
        port=remotehostconfig['Remote_Port'],
        username=remotehostconfig['Remote_User'],
        password=remotehostconfig['Remote_Pass']
    )

    #stdin, stdout, stderr = ssh.exec_command('ls ' + Remote_file_path)  #exec_command返回的为tunple，第二个为stdout
    if ssh.exec_command('ls ' + Remote_file_path)[1].read():
        stdin, stdout, stderr = ssh.exec_command('cp -r ' + Remote_file_path + ' ' + Remote_bak_path + Ser_name + '_' + now_time)
        print(stdout.read())
        scp = paramiko.Transport((remotehostconfig['Remote_Host'], remotehostconfig['Remote_Port']))
        scp.connect(username=remotehostconfig['Remote_User'], password=remotehostconfig['Remote_Pass'])
        sftp = paramiko.SFTPClient.from_transport(scp)
        sftp.put(Local_zip, Remote_upload_file)
        sftp.close()
        stdin, stdout, stderr = ssh.exec_command('rm -rf ' + Remote_file_path + '*')
        stdin, stdout, stderr = ssh.exec_command('mv ' + Remote_upload_file + ' ' + Remote_file_zip)
        print(stdout.read())
        stdin, stdout, stderr = ssh.exec_command('unzip ' + Remote_file_zip + ' -d ' + Remote_file_parentpath)
        print(stdout.read())
        stdin, stdout, stderr = ssh.exec_command('rm -rf ' + Remote_file_parentpath)
    else:
        print('the pre-pc path:/usr/local/nginx/html/zufangguanli-pc/dist  not exist,please login server checkout')
    ssh.close()



###单台服务器传输
# #remote host config Definition --- real server#####
# Remote_Host='47.100.113.123'
# Remote_User='root'
# Remote_Pass='C5]werkh4zbpoGb'
# Remote_Port=2222
# def remoterealhost():
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(
#         hostname=Remote_Host,
#         port=Remote_Port,
#         username=Remote_User,
#         password=Remote_Pass
#     )
#
#     #stdin, stdout, stderr = ssh.exec_command('ls ' + Remote_file_path)  #exec_command返回的为tunple，第二个为stdout
#     if ssh.exec_command('ls ' + Remote_file_path)[1].read():
#         stdin, stdout, stderr = ssh.exec_command('cp -r ' + Remote_file_path + ' ' + Remote_bak_path + Ser_name + '_' + now_time)
#         print(stdout.read())
#         scp = paramiko.Transport((Remote_Host, Remote_Port))
#         scp.connect(username=Remote_User, password=Remote_Pass)
#         sftp = paramiko.SFTPClient.from_transport(scp)
#         sftp.put(Local_zip, Remote_upload_file)
#         sftp.close()
#         stdin, stdout, stderr = ssh.exec_command('rm -rf ' + Remote_file_path + '*')
#         stdin, stdout, stderr = ssh.exec_command('mv ' + Remote_upload_file + ' ' + Remote_file_zip)
#         print(stdout.read())
#         stdin, stdout, stderr = ssh.exec_command('unzip ' + Remote_file_zip + ' -d ' + Remote_file_parentpath)
#         print(stdout.read())
#     else:
#         print('the pre-pc path:/usr/local/nginx/html/zufangguanli-pc/dist  not exist,please login server checkout')
#     ssh.close()


if __name__ == '__main__':
    remotedeploy(Remote_host1)
    print("deploy host1 commplate")
    remotedeploy(Remote_host2)
    print("deploy host2 commplate")