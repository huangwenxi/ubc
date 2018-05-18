class GlobalVariable():
    empty_list_num = 0
    local_sock = 0
    database = None
    address_of_2G = ()
    mobile_freq = 0
    union_freq = 0

    ID = 'id'
    MODULE = 'module'
    UBC = 'ubc'
    UBC_INFO = 'ubc_info'
    IMSI = 'imsi'
    MSG_GET_IMSI_UBC = 'MSG_GET_IMSI_UBC'
    MSG_SET_IMSI_UBC = 'MSG_SET_IMSI_UBC'
    MSG_UBC_HEARTBEAT = 'MSG_UBC_HEARTBEAT'
    MSG_UBC_HEARTBEAT_ACK = 'MSG_UBC_HEARTBEAT_ACK'
    MSG_GET_IMSI_UBC = 'MSG_GET_IMSI_UBC'

    MCC_OF_CHINA = '460'
    TABLE_NAME = {
        '00': 'mobile_table',
        '02': 'mobile_table',
        '04': 'mobile_table',
        '07': 'mobile_table',
        '01': 'union_table',
        '06': 'union_table',
        '09': 'union_table',
        '03': 'telecom_table',
        '05': 'telecom_table',
        '11': 'telecom_table',
        'other': 'other_table'
    }
    OTHER = 'other'

    HOST = '127.0.0.1'

    REJECT = 1
    REDIRECT = 2
    BUF_SIZE = 1024
    MESSAGE_HEADER_LENGTH = 8