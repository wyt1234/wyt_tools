#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''                                                          
Copyright (C)2018 SenseDeal AI, Inc. All Rights Reserved                                                      
Author: xuwei                                        
Email: weix@sensedeal.ai                                 
Description:                                    
'''


import logging
import graypy
# from graypy.rabbitmq import GELFRabbitHandler


class GrayLogging(object):
    def __init__(self, host='192.168.0.29', port=12201, log_type='error'):
        self.host = host
        self.port = port
        self.log_type = log_type

    # def __init__(self, host='192.168.1.150', port=50060, log_type='error'):
    #     self.host = host
    #     self.port = port
    #     self.log_type = log_type

    # handler = graypy.GELFUDPHandler(self.host, self.port)
    # handler = graypy.GELFRabbitHandler('amqp://guest:guest@localhost/', exchange='logging.gelf')
    def __logs_to_gray(self, handler, log_class_name: str, log_msg: str):
        my_logger = logging.getLogger(log_class_name)
        my_logger.setLevel(logging.DEBUG)
        my_logger.addHandler(handler)
        if self.log_type == 'error':
            my_logger.error(log_msg)
        elif self.log_type == 'debug':
            my_logger.debug(log_msg)
        elif self.log_type == 'warning':
            my_logger.warning(log_msg)
        else:
            my_logger.info(log_msg)

    def udp_gray(self, log_class_name: str, log_msg: str):
        handler = graypy.GELFUDPHandler(self.host, self.port)
        self.__logs_to_gray(handler, log_class_name, log_msg)

    # 使用GELFRabbitHandler将消息发送到RabbitMQ，并配置Graylog服务器以通过AMQP使用消息。这样可以防止由于丢失的UDP数据包而丢失日志消息
    def rabbit_gray(self, log_class_name: str, log_msg: str, user=None, password=None, host=None,
                    port=None, topic='log-messages'):
        # amqp: // guest: guest @ localhost:5672 /
        handler = graypy.GELFRabbitHandler('amqp://%s:%s@%s:%s/' % (user, password, host, port), exchange=topic)
        self.__logs_to_gray(handler, log_class_name, log_msg)


if __name__ == '__main__':
    import json
    gray_log = GrayLogging()
    gray_log.udp_gray('udpxw', "{'123': '非rabbit测试xuwei'}")
    # gray_log.rabbit_gray('log-messages', json.dumps({'徐威': 'rabbit测试'}, ensure_ascii=False), user='admin',
    #                      password='sense_mq@2018', host='52.82.68.88', port=5672)
