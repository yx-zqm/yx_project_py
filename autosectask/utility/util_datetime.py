from datetime import datetime, timedelta


class DateUtils:
    @staticmethod
    def get_current_and_previous_month(format="%Y%m"):
        # 获取当前日期和时间
        current_date = datetime.now()

        # 获取当前月份
        current_month = current_date.strftime(format)

        # 获取上个月份
        previous_month = (current_date - timedelta(days=current_date.day)).strftime(format)

        return current_month, previous_month

# # 调用静态方法
# current_month, previous_month = DateUtils.get_current_and_previous_month(format="%Y/%m")
# print("当前月份:", current_month)
# print("上个月份:", previous_month)
