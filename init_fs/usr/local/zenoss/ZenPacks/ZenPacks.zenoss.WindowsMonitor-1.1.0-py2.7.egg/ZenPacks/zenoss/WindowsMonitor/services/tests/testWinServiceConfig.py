##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals

from Products.ZenModel.Device import Device, manage_createDevice
from Products.ZenModel.WinService import WinService, manage_addWinService
from Products.ZenTestCase.BaseTestCase import BaseTestCase
from ZenPacks.zenoss.WindowsMonitor.services.WinServiceConfig import WinServiceConfig

class TestWinServiceConfig(BaseTestCase):
    def afterSetUp(self):
        super(TestWinServiceConfig, self).afterSetUp()

        dev = manage_createDevice(self.dmd, "test-dev1",
                                  "/Server/Windows",
                                  manageIp="10.0.10.1")
        dev.zWmiMonitorIgnore = False
        winService = manage_addWinService(dev.os.winservices, 'wsvc', 'test service')
        winService.zMonitor = True
        winService.monitor = True
        winService.startMode = 'Auto'
        winService.index_object()
        
        self._testDev = dev
        self._deviceNames = [ "test-dev1" ]
        self._configService = WinServiceConfig(self.dmd, "localhost")

    def beforeTearDown(self):
        self._testDev = None
        self._deviceNames = None
        self._configService = None
        super(TestWinServiceConfig, self).beforeTearDown()

    def testProductionStateFilter(self):
        self._testDev.setProdState(-1)

        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertEqual(len(proxies), 0)

        self._testDev.setProdState(1000)
        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertEqual(len(proxies), 1)

    def testWmiMonitorFlagFilter(self):
        self._testDev.zWmiMonitorIgnore = True
        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertEqual(len(proxies), 0)

        self._testDev.zWmiMonitorIgnore = False
        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertEqual(len(proxies), 1)

    def testMultipleDevicesWithDuplicate(self):
        dev = manage_createDevice(self.dmd, "test-dev2",
                                  "/Server/Windows",
                                  manageIp="10.0.10.2")
        dev.setManageIp("10.0.10.1")

        proxies = self._configService.remote_getDeviceConfigs()
        self.assertEqual(len(proxies), 1)

    def testUnmonitoredService(self):
        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertEqual(len(proxies), 1)

        self._testDev.os.winservices()[0].zMonitor = False
        self._testDev.os.winservices()[0].index_object()
        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertEqual(len(proxies), 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestWinServiceConfig))
    return suite

if __name__=="__main__":
    framework()
