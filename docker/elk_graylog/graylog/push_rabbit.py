#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''                                                          
Copyright (C)2018 SenseDeal AI, Inc. All Rights Reserved                                                      
Author: xuwei                                        
Email: weix@sensedeal.ai                                 
Description:                                    
'''

import sense_core as sd
sd.log_init_config(root_path=sd.config('log_path'))
import json

producer = sd.RabbitProducer(label='rabbit')
log = "徐威rabbit"

producer.send_safely('log-messages', log)
