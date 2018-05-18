from enum import Enum
from tool import *

class Heartbeat_Info(object):

    info = {'length':0 ,'info_serial':0, 'wArfcn1':0, 'b2GUENum1':0, 'b4GUENum1':0, 'b2GIMSINum1':0, 'b4GIMSINum1':0, 'wArfcn2':0, 'b2GUENum2':0, 'b4GUENum2':0, 'b2GIMSINum2':0, 'b4GIMSINum2':0}
    @classmethod
    def store_info(cls, info_tuple):
        Tool.transfer_tuple_2_dic(info_tuple, cls.info)



class User_Detection_Nunber_Report(object):
    INFO_LENGTH = 49
