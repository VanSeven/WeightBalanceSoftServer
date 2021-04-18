# -*- coding: utf-8 -*-

from socket import *

from UserInfoDataBase import UserInfoDataBaseManage


user_info_dbm = UserInfoDataBaseManage()


if __name__ == '__main__':
    HOST = ''
    PORT = 21567
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)

    try:
        while True:
            print('waiting for connection...')
            tcpCliSock, addr = tcpSerSock.accept()
            print('...connected from:', addr)

            try:
                while True:
                    data = tcpCliSock.recv(BUFSIZ)
                    if not data:
                        break
                    # 进入验证用户登录信息对话
                    if data.decode('utf-8') == 'confirm user info':
                        tcpCliSock.send(bytes('get confirm user info', encoding='utf-8'))
                        data = tcpCliSock.recv(BUFSIZ)
                        # 将用户登录信息与数据库记录进行查询
                        search_result = user_info_dbm.confirm_user_info(data.decode('utf-8'))
                        # 返回查询结果
                        data = tcpCliSock.send(bytes(search_result, encoding='utf-8'))
                        break
            except ConnectionResetError:
                print('客户端：%s 强制断开连接！' % str(addr))
            finally:
                tcpCliSock.close()
    except (EOFError, KeyboardInterrupt):
        tcpSerSock.close()
