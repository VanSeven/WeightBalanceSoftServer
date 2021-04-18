# -*- coding: utf-8 -*-

import sqlite3
import xlrd
import os


class UserInfoDataBaseManage(object):
    def __init__(self):
        self.con = None
        self.cur = None

    # 从excel中增加数据，method表示是追加还是覆盖
    def add_user_info_from_excel(self, excel_path, method='append'):
        self.connect_database()
        if method == 'new':
            self.cur.execute('DROP TABLE IF EXISTS USERINFO')
        self.cur.execute("CREATE TABLE IF NOT EXISTS USERINFO(id TEXT PRIMARY KEY,password TEXT,authority TEXT,"
                         "logincount INTEGER)")
        self.con.commit()

        if os.path.isfile(excel_path):
            try:
                # 打开文件
                xl_data = xlrd.open_workbook(excel_path)
                # 选择第一个sheet
                table = xl_data.sheet_by_index(0)
                for i in range(table.nrows):
                    if i > 0:
                        data = '\'%s\', \'%s\', \'%s\', %d' % (table.cell_value(i, 0), table.cell_value(i, 1),
                                                               table.cell_value(i, 2), table.cell_value(i, 3))
                        self.cur.execute('INSERT INTO USERINFO VALUES (%s)' % data)
                        self.con.commit()
            except:
                print('写入失败！')

        self.disconnect_database()

    # 查询用户登录信息
    def confirm_user_info(self, user_info):
        self.connect_database()
        info = user_info.split(' ')
        username = info[0]
        password = info[1]
        self.cur.execute(
            'SELECT authority FROM USERINFO WHERE id = \'%s\' AND password = \'%s\'' % (username, password))
        self.con.commit()
        result_rows = self.cur.fetchall()

        if result_rows and len(result_rows) == 1:
            self.cur.execute(
                'UPDATE USERINFO SET logincount = logincount + 1 WHERE id = \'%s\'' % username)
            self.con.commit()
            self.disconnect_database()
            # 返回结果，结果+权限等级，结果：1表示查询成功，权限：以高到低，分A、B、C三个等级
            return '1 ' + result_rows[0][0]
        else:
            self.disconnect_database()
            return '0 A'

    # 连接数据库
    def connect_database(self):
        self.con = sqlite3.connect('.\\data\\userinfo.db')
        self.cur = self.con.cursor()

    # 断开数据库
    def disconnect_database(self):
        if self.cur and self.con:
            self.cur.close()
            self.con.close()


if __name__ == '__main__':
    user_info_dbm = UserInfoDataBaseManage()
    user_info_dbm.add_user_info_from_excel(excel_path='.\\data\\用户信息.xlsx', method='new')
