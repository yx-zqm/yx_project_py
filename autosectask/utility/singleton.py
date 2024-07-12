# -*- coding: utf-8 -*-
# @Author : Wei XiLi (wei.xl@asiainfo-sec.com)
# @Date   : 2021-08-12 14:23:36
# @Memo   : base class of Singleton
# @Revision:
#   * 2021-08-12, Wei.xl,

class Singleton(object):
    """
    单例类：
        概述：要求一个类有且仅有一个实例，并且提供了一个全局的访问点。
        应用场景：日志插入、计时器、权限校验、回收站、网站计数器、线程池、数据库连接池等资源池。
    原理：
        一个对象的实例化过程是先执行类的__new__方法,
        如果我们没有写,默认会调用object的__new__方法,返回一个实例化对象,
        然后再调用__init__方法,对这个对象进行初始化

        在一个类的__new__方法中先判断是不是存在实例,如果存在实例,就直接返回,如果不存在实例就创建
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
