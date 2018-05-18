#coding=utf-8
import  socket
import json
from tool import Tool
from database import MyDataBase
from logconfig import logger
from timer import Timer
mobile_table_name = 'mobilecomm'
union_table_name = 'unioncomm'
tele_table_name = 'telecomm'
OTHER = 'other'
VERSION = '1.0'
class MsgKey():
    id = 'id'
    ubc = 'ubc'
    imsi = 'imsi'
    info = 'info'
    type = 'type'
    module = 'module'
    ubc_info = 'ubc_info'
    imsi_list = 'imsilist'

#receive message id
class RcvMsgId_value():

    ubc_chg_tac = 'MSG_CHG_TAC'
    ntc_heartbeat = 'NTC_HEARTBEAT'
    ubc_get_imsi = 'MSG_UBC_GET_IMSI'
    ntc_query_imsi = 'NTC_QUERY_IMSI'
    ntc_insert_imsi = 'NTC_INSERT_IMSI'
    ubc_heartbeat = 'MSG_UBC_HEARTBEAT'
#response message id
class RspMsgId_value():

    ntc_set_imsi = 'NTC_SET_IMSI'
    ubc_set_imsi = 'MSG_SET_IMSI_UBC'
    ubc_heartbeat_ack = 'MSG_UBC_HEARTBEAT_ACK'
    ntc_insert_imsi_ack = 'NTC_INSERT_IMSI_ACK'
    ntc_query_imsi_ack = 'NTC_QUERY_IMSI_ACK'
    ntc_query_imsi_rep = 'NTC_QUERY_IMSI_REP'

db_info = {
    'mcc_of_china':'460',
    '00': mobile_table_name,
    '02': mobile_table_name,
    '04': mobile_table_name,
    '07': mobile_table_name,
    '01': union_table_name,
    '06': union_table_name,
    '09': union_table_name,
    '03': tele_table_name,
    '05': tele_table_name,
    '11': tele_table_name,
    '20': tele_table_name,
    'other': OTHER
}
arfcn = {mobile_table_name: 89, union_table_name: 120, tele_table_name: 0}
class Ubc(object):
    BUF_SIZE = 1024
    MESSAGE_HEADER_LENGTH = 8
    REJECT = 1
    REDIRECT = 2
    report_imsi_num_4G = 0
    report_imsi_num_4G_tmp = 0
    dispatch = {}

    def __init__(self, ip, port):
        self._create_socket(ip, port)
        self._init_database()
        self.mobile_4G_empty_ue_num = 0
        self.union_4G_empty_ue_num = 0

    #定时器函数，循环触发判断4G上报的IMSI数量是否过少了，是的话则给4G发送TAC指令重入
    @classmethod
    def func_timer(cls):
        if cls.report_imsi_num_4G_tmp is 0:#同步一下
            cls.report_imsi_num_4G_tmp = cls.report_imsi_num_4G
        else:
            if (cls.report_imsi_num_4G_tmp + 10) <  cls.report_imsi_num_4G:
                #todo send tac
                cls._response(('', 6070), id=RcvMsgId_value.ubc_chg_tac)
                cls.report_imsi_num_4G_tmp = cls.report_imsi_num_4G

    #初始化数据库，建立4张表。移动，联通，電信,OTHER
    def _init_database(self):
        """Connect to database and create all table."""
        self.database = MyDataBase()
        self.database.create_table(mobile_table_name)
        self.database.create_table(union_table_name)
        self.database.create_table(tele_table_name)
        self.database.create_table(OTHER)

    #建立本地的UDP
    def _create_socket(self, ip, port):
        """Create socket based on ip and port.Family is AF_INET and type is SOCK_DGRAM.
        ip:type:string
        port:type:int
        """
        address = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(address)

    #处理ntc模块上报的心跳包
    def _process_ntc_heartbeat(self, message, address):
        """process the heartbeat message from client.get the number of 4G Mobile translation modules \
        and the number of 4G Union translation modules.
        message:type:dict
        """
        arfcn[mobile_table_name], b2GUENum1, self.mobile_4G_empty_ue_num , b2GIMSINum1, b4GIMSINum1, \
        arfcn[union_table_name], b2GUENum2, self.union_4G_empty_ue_num, b2GIMSINum2, b4GIMSINum2 = message.get(MsgKey.info)
        self.address_2GC = address
    dispatch[RcvMsgId_value.ntc_heartbeat] = _process_ntc_heartbeat

    #处理ntc模块上报的查询数据库的消息
    def _process_ntc_query_imsi(self, message, address):
        """process the heartbeat message from client.get the number of 4G Mobile translation modules \
        and the number of 4G Union translation modules.
        message:type:dict
        address:type:tuple
        """
        response_imsi_list = []
        recv_imsi_list = message.get(MsgKey.imsi)#the type of recv_imsi_list list
        #get imsi from imsi_list
        for imsi in recv_imsi_list:
            table_name, store_code = Tool.parse_imsi(imsi, db_info)#parse imsi,return table_name and store_code in database
            try:
                row = self.database.query(table_name, store_code)
                if row:
                    pass
                else:
                    response_imsi_list.append(imsi)#返回未查询到的imsi列表
            except Exception as e:
                logger.error(e.message)
        #if response_imsi_list is empty, no response
        if response_imsi_list:
            self._response(address, id=RspMsgId_value.ntc_query_imsi_rep,
                       imsilist=response_imsi_list)
    dispatch[RcvMsgId_value.ntc_query_imsi] = _process_ntc_query_imsi

    #处理ntc模块上报的插入数据库的消息
    def _process_ntc_insert_imsi(self, message, address):
        """parse imsi and get table_name,store_code ->
        query whether the database has stored the store_code in table named table_name ->
        if not -> insert store_code to table named table_name.
        message:type:dict
        """
        imsi_list = message.get(MsgKey.imsi_list)#imsi is list
        for imsi in imsi_list:
            table_name, store_code = Tool.parse_imsi(imsi, db_info)
            row = self.database.query(table_name, store_code)
            if not row:
                try:
                    self.database.insert(table_name, store_code)
                except Exception as e:
                    logger.error(str(e.args) + str(e.message))
    dispatch[RcvMsgId_value.ntc_insert_imsi] = _process_ntc_insert_imsi

    #处理4G上报的查询IMSI是否需要翻译的消息
    def _process_ubc_get_imsi(self, message, address):
        """process the message packet form client.
        message:type:dict
        address:type:tuple
        """
        response = self._response
        self.report_imsi_num_4G += 1
        logger.debug('received get_imsi_ubc packet, it is ready to send set_imsi_ubc packet')
        imsi = message.get(MsgKey.imsi)
        table_name, store_code = Tool.parse_imsi(imsi, db_info)

        #如果移动联通4G翻译模块数量为0，则直接拒绝
        if table_name == mobile_table_name and self.mobile_4G_empty_ue_num <= 0 or \
                table_name == union_table_name and self.union_4G_empty_ue_num == 0 :
            response(address, id=RspMsgId_value.ubc_set_imsi,
                     ubc_info=[[imsi, Ubc.REJECT,0]])
            logger.info("No free translation modules are available")
            return

        #移动联通4G翻译模块数量不为0，查询数据库
        try:
            row = self._query_database(table_name, store_code)
            # 该号码翻译过，在数据库中能找到记录，给4g设备发送拒绝消息
            if row:
                logger.debug(imsi + '号码翻译过')
                response(address, id=RspMsgId_value.ubc_set_imsi,
                         ubc_info=[[imsi, Ubc.REJECT, 0]])
            # 该imsi没翻译过，指派到2G
            else:
                logger.debug(imsi + '号码没翻译过')
                # 给4g设备发送指派消息
                response(address, id=RspMsgId_value.ubc_set_imsi,
                         ubc_info=[[imsi, Ubc.REDIRECT, arfcn.get(table_name)]])
                self.database.insert(table_name, store_code)
                # 将指派的imsi发送给2g
                response(self.address_2GC, id=RspMsgId_value.ntc_set_imsi,
                         imsilist=[imsi], modulelist=[table_name])
                self._ntc_update_empty_ue_num(table_name)
        except Exception as e:
            logger.error(str(e.args) + str(e.message))
    dispatch[RcvMsgId_value.ubc_get_imsi] = _process_ubc_get_imsi

    #处理4G模块上报的心跳包
    def _process_ubc_heartbeat(self, message, address):
        """Processing the heartbeat packet that are reported from the UBC module.
        message:type:dict
        address:type:tuple
        """
        logger.debug('message:' + str(message) + 'address:' + str(address))
        self._response(address, id=RspMsgId_value.ubc_heartbeat_ack, module=MsgKey.ubc)
    dispatch[RcvMsgId_value.ubc_heartbeat] = _process_ubc_heartbeat

    #查询数据库
    def _query_database(self, table_name, store_code):
        """query data from database of table named table_name.
        table_name:type:string
        store_code:type:string
        """
        row = None
        try:
            row = self.database.query(table_name, store_code)  # 根据表名和存储的代码查询数据库
            return row
        except Exception as e:
            logger.error(str(e.args) + str(e.message))
        # return row.fetchone()

    #更新本地记录的2G翻译模块的当前的空闲的数量
    def _ntc_update_empty_ue_num(self, table_name):
        """After assigning the imsi to the translation module and update the number of the free translation
        module.
        table_name:type:string
        """
        if table_name == mobile_table_name:
            if self.mobile_4G_empty_ue_num:
                self.mobile_4G_empty_ue_num -= 1
        elif table_name == union_table_name:
            if self.union_4G_empty_ue_num:
                self.union_4G_empty_ue_num -= 1

    #send message to address use socket
    def _response(cls, address, **kwargs):
        """send data to client.
        address:type:tuple
        """
        _send = cls.sock.sendto
        packet = {}

        for key,value in kwargs.items():
            packet[key] = value
        _send(json.dumps(packet), address)
        logger.info('send' + str(json.dumps(packet)) + str(address))

    #消息处理，消息分发
    def _process_message(self, message, address):
        """process the message sent by the socket.
        message:message from socket client
        address:address of client
        """
        logger.info('message:' + message + 'address:' + str(address))
        dispatch = self.dispatch
        if message:
            message_dict = json.loads(message)
            id = message_dict.get(MsgKey.id)
            if id in dispatch:
                _func = dispatch.get(id)
                _func(self,message_dict, address)
            else:
                logger.error('unrecognized message from:' + str(address))

    def main_process(self):
        """main process function."""
        while True:
            # 接收4G和NTC的消息,message是字符,address是消息的发送地址
            message, address = self.sock.recvfrom(Ubc.BUF_SIZE)
            logger.info('receive from client:' + str(len(message)) + 'bytes data')
            self._process_message(message, address)

if __name__ == '__main__':
    logger.info(VERSION)
    ubc = Ubc('', 6080)
    timer = Timer(60, ubc.func_timer)
    ubc.main_process()
