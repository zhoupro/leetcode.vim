# coding:utf-8
import configparser
import os

def getConfig(config_section, config_name):
    #用os模块来读取
    curpath=os.path.dirname(os.path.realpath(__file__))
    cfgpath=os.path.join(curpath,"leet.ini")  #读取到本机的配置文件
    #调用读取配置模块中的类
    conf=configparser.ConfigParser()
    conf.read(cfgpath)
    #调用get方法，然后获取配置的数据
    return conf.get(config_section,config_name)

