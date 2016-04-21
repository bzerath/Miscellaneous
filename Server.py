# -*- coding: utf-8 -*-
from __future__ import unicode_literals     # Everything is UTF-8

import logging
import socket
import time
import struct

logger = logging.getLogger(__name__)


def CONVERT_HexStr2Bin(HexStrValue):
    str1 = b""
    str2 = b""
    while HexStrValue:
        str1 = HexStrValue[0:2]
        s = int(str1, 16)
        str2 += struct.pack(b'B', s)
        HexStrValue = HexStrValue[2:]
    return str2


def dec2hex(number, length):
    hexavalue = str("%X" % number)
    while len(hexavalue) < length:
        hexavalue = '0'+hexavalue
    return hexavalue


class Server(object):
    def __init__(self, server_name, type_server):
        """
        Only an ersatz of algorithm.
        """
        self.Message_part = ""
        self.Server_Name = server_name
        self.Type_server = type_server
        self.Message2Send_Header = ""
        self.Message2Send_Control = ""
        # read information in the Variables.LiteATS_Servers_General_Information dic
        self.UDP_IP_Server = "255.255.255.255"
        self.UDP_PORT_Server = 20000
        self.UDP_IP_ATS = "255.255.255.255"
        self.UDP_PORT_ATS = 20000
        self.ATS_ID = "255.255.255.255"
        self.Server_ID = "id_serv"
        self.Log_ID = "id_log"

        # Prepares the socket
        try:
            self.socket_Server = socket.socket(socket.AF_INET,     # Internet
                                               socket.SOCK_DGRAM)  # UDP
            self.socket_Server.setsockopt(socket.SOL_SOCKET,
                                          socket.SO_REUSEADDR,
                                          1)
            self.socket_Server.bind((self.UDP_IP_ATS, self.UDP_PORT_ATS))
            self.socketOK = True
        except Exception as e:
            logger.error("Error connexion to {} ({}) !!".format(self.Type_server, self.Server_Name))

    def sendMessage(self):
        self.socket_Server.sendto(CONVERT_HexStr2Bin(self.Message2Send_Header+self.Message2Send_Control),
                                      (self.UDP_IP_Server,
                                       self.UDP_PORT_Server))

    def Server_Run(self):
        """
        Just an example.
        >>> serveur = Server(...)
        >>> thread = threading.Thread(target=serveur.Server_Run)
        >>> thread.daemon = True
        >>> thread.start()
        :return:
        """
        while Trigger:
            if Status:
                # Get data from queues
                if not queue.empty():   # import Queue
                    self.tmp, self.command_type = queue.get()
                    queue.task_done()

                # Do someting with self.tmp and self.command_type
                # write a message to send
                logger.info(message)
                self.sendMessage()

            time.sleep(0.5)

    def Reception_Run(self):
        """
        Another example in a reception purpose
        """
        while Trigger:
            if Status:
                try:
                    data, addr = self.socket_Server.recvfrom(4096)  # buffer size is 4096 bytes
                except Exception as e:
                    logger.error("No data received. Reception socket may be misconfigured.")
                    break
                # Converts the binary received into some hexa string
                for item in data:
                    self.Message_part += dec2hex(struct.unpack('B', item)[0], 2)
                if self.Message_part != '':
                    # do something with it
                self.Message_part = ''
            time.sleep(0.5)


