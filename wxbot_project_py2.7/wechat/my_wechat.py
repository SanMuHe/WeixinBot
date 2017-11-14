#!/usr/bin/env python
# coding: utf-8

#===================================================
from utils import *
from wechat_apis import WXAPI
from config import Constant
#---------------------------------------------------
import time
from datetime import timedelta
#===================================================

class MyWeChat(WXAPI):
    def __str__(self):
        description = \
            "=========================\n" + \
            "[#] Web WeChat\n" + \
            "[#] UUID: " + self.uuid + "\n" + \
            "[#] Uin: " + str(self.uin) + "\n" + \
            "[#] Sid: " + self.sid + "\n" + \
            "[#] Skey: " + self.skey + "\n" + \
            "[#] DeviceId: " + self.device_id + "\n" + \
            "[#] PassTicket: " + self.pass_ticket + "\n" + \
            "[#] Run Time: " + self.get_run_time() + '\n' + \
            "========================="
        return description

    def __init__(self, host='wx.qq.com'):

        super(MyWeChat, self).__init__(host)

        self.last_login = 0  # 上次退出的时间
        self.start_time = time.time()
        self.exit_code = 0

    def start(self):
        echo(Constant.LOG_MSG_START)

        timeOut = time.time() - self.last_login
        echo(Constant.LOG_MSG_TRY_INIT)
        if self.webwxinit():
            echo(Constant.LOG_MSG_SUCCESS)
        else:
            echo(Constant.LOG_MSG_FAIL)

            while True:
                # first try to login by uin without qrcode
                echo(Constant.LOG_MSG_ASSOCIATION_LOGIN)
                if self.association_login():
                    echo(Constant.LOG_MSG_SUCCESS)
                else:
                    echo(Constant.LOG_MSG_FAIL)
                    # scan qrcode to login
                    run(Constant.LOG_MSG_GET_UUID, self.getuuid)
                    echo(Constant.LOG_MSG_GET_QRCODE)
                    self.genqrcode()
                    echo(Constant.LOG_MSG_SCAN_QRCODE)

                if not self.waitforlogin():
                    continue
                echo(Constant.LOG_MSG_CONFIRM_LOGIN)
                if not self.waitforlogin(0):
                    continue
                break

            run(Constant.LOG_MSG_LOGIN, self.login)
            run(Constant.LOG_MSG_INIT, self.webwxinit)
            run(Constant.LOG_MSG_STATUS_NOTIFY, self.webwxstatusnotify)
            run(Constant.LOG_MSG_GET_CONTACT, self.webwxgetcontact)
            echo(Constant.LOG_MSG_CONTACT_COUNT % (
                    self.MemberCount, len(self.MemberList)
                ))
            echo(Constant.LOG_MSG_OTHER_CONTACT_COUNT % (
                    len(self.GroupList), len(self.ContactList),
                    len(self.SpecialUsersList), len(self.PublicUsersList)
                ))

    def get_run_time(self):
        """
        @brief      get how long this run
        @return     String
        """
        total_time = int(time.time() - self.start_time)
        t = timedelta(seconds=total_time)
        return '%s Day %s' % (t.days, t)

    def stop(self):
        """
        @brief      Save some data and use shell to kill this process
        """
        echo(Constant.LOG_MSG_RUNTIME % self.get_run_time())
