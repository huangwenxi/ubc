# coding=utf-8
import struct
from enum import Enum
from tool import Tool
from database import *
from info import *
MESSAGE_HEADER_SIZE = 8
USER_NUMBER_QUERY_MESSAGE_INFO_LENGTH = 23
USER_NUMBER_QUERY_MESSAGE_LENGTH = MESSAGE_HEADER_SIZE + USER_NUMBER_QUERY_MESSAGE_INFO_LENGTH

class Second_Communication_Procotol(object):
    # message serial
    USER_NUMBER_QUERY = 8
    USER_NUMBER_REPORT = 20
    USER_DETECTION_NUMBER_REPORT = 24
    HEARTBEAT_REPORT = 31
    # class parameter
    address = ()



    @classmethod
    def unpack(cls, message):

        length, message_sequence, message_serial, carrier, message_param = struct.unpack('!I4B', message)
        if message_serial == cls.HEARTBEAT_REPORT:
            info = struct.unpack_from('!H4BH4B', message, MESSAGE_HEADER_SIZE)
            Heartbeat_Info.store_info(info)

        elif message_serial == cls.USER_DETECTION_NUMBER_REPORT:
            #假定2g如果翻译队列不空闲的话是不会上报imsi的
            imsi_num = (length - MESSAGE_HEADER_SIZE) / User_Detection_Nunber_Report.INFO_LENGTH
            imsi_list = []
            offest = MESSAGE_HEADER_SIZE
            for index  in range(imsi_num):
                imsi_info = struct.unpack_from('!BHI20s20sh')
                if imsi_info == None:
                    return -1
                imsi = imsi_info[3][:15]
                imsi_list.append(imsi)
            cls.process(message_sequence, message_serial, carrier, imsi)

        elif message_serial == cls.USER_NUMBER_REPORT:




    @classmethod
    def process(cls, message_sequence, message_serial, carrier, info_data):

        if message_serial == cls.USER_DETECTION_NUMBER_REPORT:
            try:
                for imsi in imsi:
                    table_name, msin = Tool.parse_imsi(imsi)
                    ret = MyDataBase.query_table(table_name, imsi)
                    if ret == None:
                        cls.pack(message_sequence, message_serial, carrier, '0', 0x0211, imsi)
                        continue

            except StopIteration:
                return 0

            data = iter(imsi)
            try:
                while True:
                    data.next()
            except StopIteration:


    @classmethod
    def pack(cls, message_sequence, message_serial, carrier, message_param, info_sequence, info_data):
        message_length = USER_NUMBER_QUERY_MESSAGE_LENGTH
        serial_number =

    @classmethod
    def response(cls):
