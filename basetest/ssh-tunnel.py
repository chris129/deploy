# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from sshtunnel import SSHTunnelForwarder
import paramiko


###remote forward host config Definition###
Remote_For_Host='跳板机IP'
Remote_For_User='跳板机用户'
Remote_For_Pass='跳板机密码'
Remote_For_Port=22

###remote host config Definition --- real server#####
Remote_Host='内网机器IP'
Remote_User='内网机器用户'
Remote_Pass='内网机器密码'
Remote_Port=22


###方式一： 本地开启监听
# server = SSHTunnelForwarder(
#     ssh_address_or_host=('IP',22),#机器的配置--跳板机
#     ssh_username='USER',                     #机器的配置--跳板机账号
#     ssh_password='PASS',               #机器的配置--跳板机密码
#     local_bind_address=('127.0.0.1',2222),   #本地监听信息，可选
#     remote_bind_address=('内网IP',22)         #机器的配置-内网私有IP地址
# )
#
# server.start()   #然后使用工具或命令连接本地端口即可

##方式二：
# remoteserver = SSHTunnelForwarder(
#     ssh_address_or_host=(Remote_For_Host, Remote_For_Port),  # 机器的配置--跳板机
#     ssh_username=Remote_For_User,  # 机器的配置--跳板机账号
#     ssh_password=Remote_For_Pass,  # 机器的配置--跳板机密码
#     remote_bind_address=(Remote_Host, Remote_Port)  # 机器的配置-内网私有IP地址
# )
# remoteserver.start()
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(
#     hostname='127.0.0.1',
#     port=remoteserver.local_bind_port,
#     username=Remote_User,  # 内网私有服务器的用户
#     password=Remote_Pass  # 内网私有服务器的密码
# )
# stdin, stdout, stderr = ssh.exec_command('ifconfig')
# print(stdout.read())
# ssh.close()
# remoteserver.close()

###方式3"： 不知道本地监听，使用随机端口
with SSHTunnelForwarder(
    ssh_address_or_host=(Remote_For_Host,Remote_For_Port),#机器的配置--跳板机
    ssh_username=Remote_For_User,                     #机器的配置--跳板机账号
    ssh_password=Remote_For_Pass,               #机器的配置--跳板机密码
    remote_bind_address=(Remote_Host,Remote_Port)         #机器的配置-内网私有IP地址
    ) as server:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname='127.0.0.1',
        port=server.local_bind_port,
        username=Remote_User,                   #内网私有服务器的用户
        password=Remote_Pass              #内网私有服务器的密码
    )
    stdin,stdout,stderr = ssh.exec_command('ifconfig')
    print(stdout.read())
    ssh.close()
