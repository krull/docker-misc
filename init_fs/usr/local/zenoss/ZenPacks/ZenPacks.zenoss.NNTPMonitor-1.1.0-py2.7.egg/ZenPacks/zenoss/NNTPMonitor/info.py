##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import RRDDataSourceInfo
from ZenPacks.zenoss.NNTPMonitor.interfaces import INNTPMonitorDataSourceInfo


class NNTPMonitorDataSourceInfo(RRDDataSourceInfo):
    implements(INNTPMonitorDataSourceInfo)
    cycletime = ProxyProperty('cycletime')
    timeout = ProxyProperty('timeout')
    nntpServer = ProxyProperty('nntpServer')
    useSSL = ProxyProperty('useSSL')
    port = ProxyProperty('port')
    
    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False
