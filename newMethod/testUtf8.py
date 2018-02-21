#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
print "Hello World!\n"
thau = "thầu"
th = "thấu"
print thau.decode('utf-8', 'ignore')
print th.decode('utf-8', 'ignore')