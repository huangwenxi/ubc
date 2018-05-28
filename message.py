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
class RcvMsgIdValue():

    ubc_chg_tac = 'MSG_CHG_TAC'
    ntc_heartbeat = 'NTC_HEARTBEAT'
    ubc_get_imsi = 'MSG_UBC_GET_IMSI'
    ntc_query_imsi = 'NTC_QUERY_IMSI'
    ntc_insert_imsi = 'NTC_INSERT_IMSI'
    ubc_heartbeat = 'MSG_UBC_HEARTBEAT'
#response message id
class RspMsgIdValue():

    ntc_set_imsi = 'NTC_SET_IMSI'
    ubc_set_imsi = 'MSG_SET_IMSI_UBC'
    ubc_heartbeat_ack = 'MSG_UBC_HEARTBEAT_ACK'
    ntc_insert_imsi_ack = 'NTC_INSERT_IMSI_ACK'
    ntc_query_imsi_ack = 'NTC_QUERY_IMSI_ACK'
    ntc_query_imsi_rep = 'NTC_QUERY_IMSI_REP'