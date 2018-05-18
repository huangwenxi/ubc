from logconfig import logger
class Tool(object):

    @classmethod
    def parse_imsi(cls, imsi, database_info):
        mcc = imsi[:3]
        mnc = imsi[3:5]
        msin = imsi[5:]
        logger.debug('mcc:' + mcc + ' mnc:' + mnc + ' msin:' + msin)
        if mcc != database_info.get('mcc_of_china') or mnc not in database_info:
            return database_info.get('other'), imsi
        return database_info.get(str(mnc)), str(msin)
