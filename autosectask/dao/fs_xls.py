import xlrd
import pandas as pd
from utility.util_logging import SimpleLogger
from xlutils.copy import copy

logger = SimpleLogger().get_logger()


class XlsFS:

    def __init__(self, path):
        self.__path = path
        self.__xlrd_wb = xlrd.open_workbook(self.__path, formatting_info=True)
        self.__wb = copy(self.__xlrd_wb)

    def __enter__(self):
        logger.info(f"opening xls file {self.__path}")
        return self

    def read_by_person(self, name, sheet_name='PATCH计划2'):
        logger.info(f"根据负责人{name}筛选数据中...")
        use_columns = ["工单编号", "子工单编号", "工单名称", "工单简介", "计划上线时间", "工时评估", "负责人", "需求负责人"]
        df = pd.read_excel(self.__path, na_values="默认为空", sheet_name=sheet_name, usecols=use_columns)
        df_by_name = df[df["负责人"].isin([name])].to_dict(orient="index")
        # 调整数据格式
        for key, value in df_by_name.items():
            minus_pos = value["工单名称"].index("-")
            value["工单名称"] = value["工单名称"][0:minus_pos]  # 去掉--4A
            logger.info("计划上线时间请使用文本格式")
            value["计划上线时间"] = value["计划上线时间"].replace("-", "")  # 日期去掉-
            value["工单简介"] = value["工单名称"] if (str(value["工单简介"]) == "nan") else value["工单简介"]
            value["工时评估"] = 10 if (str(value["工时评估"]) == "nan") else int(value["工时评估"])
        return df_by_name

    def write_cells(self, sheet_name, cells, content):
        contents = content if isinstance(content, list) else [content for _ in range(0, len(cells))]
        sheet = self.__wb.get_sheet(0)
        for cell, content in zip(cells, contents):
            logger.info(f"更新单元格{cell['row']}行{cell['column']}列内容为：{content}")
            sheet.write(cell['row'], cell['column'], content)

    def __exit__(self, e_t, e_v, t_b):
        logger.info("close xls file...")
        self.__wb.save(self.__path)

# def convert_sheet(excel_path):
#     excel = win32.gencache.EnsureDispatch('Excel.Application')
#     wb = excel.Workbooks.Open(excel_path)
#     # FileFormat = 56 is for .xls extension, 51=xlsx
#     wb.SaveAs(excel_path[0:-1.png], FileFormat=56)
#     wb.Close()
#     excel.Application.Quit()
#     os.remove(excel_path)
