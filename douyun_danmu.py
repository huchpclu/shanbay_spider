# -*- coding: utf-8 -*-

import socket
import re
import datetime

HOST = '124.95.174.146'
PORT = 8601
roomid = 101342


def align_left_str(raw_str, max_length, filled_chr):
    my_length = 0
    for i in range(0, len(raw_str)):
        if ord(raw_str[i]) > 127 or ord(raw_str[i]) <= 0:
            my_length += 1

        my_length += 1

    if (max_length - my_length) > 0:
        return raw_str + filled_chr * (max_length - my_length)
    else:
        return raw_str


def parse_content(msg):
    # print(msg)
    content = msg[12:-1].decode('utf-8', 'ignore')
    return content


def danmu_recv():
    return parse_content(s.recv(4000))


class DouyuMsg(object):
    """Docstring for DouyuTcpMessage. """

    def __init__(self, content):
        self.length = bytearray([len(content) + 9, 0x00, 0x00, 0x00])
        self.code = self.length
        self.magic = bytearray([0xb1, 0x02, 0x00, 0x00])
        self.content = bytes(content.encode("utf-8"))
        self.end = bytearray([0x00])

    def get_bytes(self):
        return bytes(self.length + self.code + self.magic + self.content + self.end)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
cmd = "type@=loginreq/roomid@=%s/" % roomid
msg = DouyuMsg(cmd).get_bytes()
s.send(msg)
data = s.recv(4000)
cmd = "type@=joingroup/rid@=%s/gid@=-9999/" % roomid
msg = DouyuMsg(cmd).get_bytes()
s.send(msg)
while True:
    recv_msg = danmu_recv()
    if "type@=" not in recv_msg:
        print(recv_msg)
        print("无效信息")
    else:
        msg_content = recv_msg.replace("@S", "/").replace("@A=", ":").replace("@=", ":")
        try:
            msg_type = re.search('type:(.+?)\/', msg_content).group(1)
            if msg_type == "chatmsg":
                msg_type_zh = "弹幕消息"
                sender_id = re.search('\/uid:(.+?)\/', msg_content).group(1)
                nickname = re.search('\/nn:(.+?)\/', msg_content).group(1)
                content = re.search('\/txt:(.+?)\/', msg_content).group(1)
                level = re.search('\/level:(.+?)\/', msg_content).group(1)
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("|" + msg_type_zh + "| " + align_left_str(nickname, 20, " ") +
                      align_left_str("<Lv:" + level + ">", 8, " ") +
                      align_left_str("(" + sender_id + ")", 13, " ") +
                      "@ "+time+": " + content + " ")

        except Exception as e:
            print(e)
            print("解析错误")
