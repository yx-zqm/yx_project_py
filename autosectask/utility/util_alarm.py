# message alarm

# 适配器模式 oracle + mysql + email ...
#
# from ais.utility.util_conn_oracle import ConnOracle
#
# template = """
#         INSERT INTO aiuap20.uap_notice
#         SELECT aiuap20.uap_notice_seq.nextval,
#             'SMS',
#             '{message}',
#             t1.MOBILE,
#             '',
#             '',
#             '',
#             sysdate,
#             ''
#           FROM aiuap20.v_uap_main_acct t1
#           WHERE t1.LOGIN_NAME IN ('yx_liuyaqi','yx_weixili','yx_chenyun')"""
#
#
# def notify(message):
#     with ConnOracle('audita/vfr4321`@10.11.180.174:1521/ltdb') as db:
#         stmt = template.format(message=message)
#         try:
#             cursor = db.cursor()
#             cursor.execute(stmt)
#             db.commit()
#         except Exception as exp:
#             db.rollback()
#             print(exp)
#         finally:
#             cursor.close()
def notify():
    return None