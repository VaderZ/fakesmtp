#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Vadim Bobrenok"
__email__ = "vader-xai@yandex.ru"
__version__ = 1.0 

import smtpd
import asyncore
import os, sys
import time
import shutil

class FakeSMTPServer(smtpd.SMTPServer):
    def __init__(self, save, *args,**kwargs):
        smtpd.SMTPServer.__init__(self, *args,**kwargs)
        self.save = save
        self.out = StdoutWriter()
        self.count = 0
        self.start_time = 0.0
        self.rate = 0.0
        
        self.out.update(0,0,'00:00:00')
        
    def process_message(self, peer, mailfrom, rcpttos, data):
        if self.start_time == 0:
            self.start_time = time.time()
        self.count += 1
        try:
            self.rate = float(self.count)/(time.time()-self.start_time)
        except ZeroDivisionError:
            pass
        self.out.update(self.count, self.rate, time.strftime('%H:%M:%S'))
        if self.save:
            with open(r'mail\mail_%s.txt'%self.count,'w') as f:
                f.write(''.join([
                                'Time: ', time.ctime(), '\n',
                                'IP: ', peer.__str__(), '\n',
                                'From: ', mailfrom, '\n',
                                'To: ', rcpttos.__str__(), '\n',
                                'Body: ', data, '\n'                            
                                ]))
        return

class StdoutWriter(object):
    def __init__(self):
        self.last_length = 0
    
    def update(self, count, rate, con_time):
        self.__show('\b'*self.last_length)
        text = "Count: %4s Rate: %6.2f   Last at: %8s"%(count, rate, con_time)
        self.last_length = len(text)
        self.__show(text)        
    
    def __show(self, text):
        sys.stdout.write(text)
        sys.stdout.flush()
        
if __name__=='__main__':    
    if os.sys.path[0].endswith('fakesmtp.exe'):
        os.chdir(os.sys.path[0].rstrip('fakesmtp.exe'))
    else:
        os.chdir(os.sys.path[0])
    shutil.rmtree('mail', True)
    
    host = '127.0.0.1'
    port = 25
    save  = True    
    for i, arg in enumerate(sys.argv[1:]):
        if i == 0:
            host = arg
        if i == 1:
            port = int(arg)
        if i == 2:
            if arg in ['false','False','f','0','off','no']:
                save = False
    if save:
        try:
            os.mkdir('mail')
        except OSError, IOError:
            if not os.path.exists('mail'):
                time.sleep(2)
                try:
                    os.mkdir('mail')
                except OSError, IOError:
                    print 'Unable to create email storage directory.'
                    sys.exit(0)
                                        
    server = FakeSMTPServer(save, (host, port), None)
    
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print "\nShutting down fake SMTP Server..."        
        sys.exit(0)