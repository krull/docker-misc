##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """HPCPUMap
Gather HP/Compaq System Insight Manager processor information.
"""

from Products.DataCollector.plugins.CollectorPlugin \
    import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.zenoss.snmp.CpuMap \
    import getManufacturerAndModel

class HPCPUMap(SnmpPlugin):
    """Map HP/Compaq insight manager cpu table to model."""

    maptype = "HPCPUMap"
    modname = "Products.ZenModel.CPU"
    relname = "cpus"
    compname = "hw"

    cpucols = {
        '.1': '_cpuidx',
        '.3': 'setProductKey',
        '.4': 'clockspeed',
        '.5': 'null',
        '.6': 'null',
        '.7': 'extspeed',
        '.8': 'null',
        '.9': 'socket',
         }

    cachecols = {'.1': 'cpuidx', '.2': 'level', '.3': 'size'}

    snmpGetTableMaps = (
        GetTableMap('cpuTable', '.1.3.6.1.4.1.232.1.2.2.1.1', cpucols),
        GetTableMap('cacheTable', '1.3.6.1.4.1.232.1.2.2.3.1', cachecols), 
    )


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        cputable = tabledata.get("cpuTable")
        cachetable = tabledata.get("cacheTable")
        if not cputable: return
        rm = self.relMap()
        cpumap = {}
        for cpu in cputable.values():
            del cpu['null']
            om = self.objectMap(cpu)
            om.setProductKey = getManufacturerAndModel(om.setProductKey)
            idx = getattr(om, 'socket', om._cpuidx)
            om.id = self.prepId("%s_%s" % (om.setProductKey,idx))
            cpumap[cpu['_cpuidx']] = om
            rm.append(om)

        if not cachetable: return rm
        for cache in cachetable.values():
            cpu = cpumap.get(cache['cpuidx'], None)
            if cpu is None: continue
            if cache['level'] == 1: 
                cpu.cacheSizeL1 = cache.get('size',0)
            elif cache['level'] == 2:
                cpu.cacheSizeL2 = cache.get('size',0)
        return rm
