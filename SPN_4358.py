#!/usr/bin/python
# coding:utf-8

# ====================================================
# 函数分类:SPN_4358测试
# 函数名称:SPN_4358_test
# 函数别名:
# 函数功能:SPN_4358_test
# 函数参数:
#     -dut1 <必选> 设备对象1名称
#     -dut2 <必选> 设备对象2名称
#     -dut3 <必选> 设备对象3名称
#     -dut4 <必选> 设备对象4名称
# 函数返回值:
# 引用函数：
#    if_intf
# 备注:
# 作者:<喻庚>
# 邮箱:<yugeng@fiberhome.com>
# 版本信息:
# 创建时间:2020-09-27
# 修改记录:2020-11-03
# ====================================================
import Global
from spn_yang_library import *

#global拓扑转换
class Local:
    tester_ip = Global.tester_ip
    port1 = Global.port2
    port2 = Global.port1

    SW1 = Global.SW2
    SW2 = Global.SW1
    SW3 = Global.SW4
    SW4 = Global.SW3

    #NNI、仪表连接
    SW1_port1 = Global.SW2_port2
    SW2_port2 = Global.SW1_port1

    SW1_SW2_1 = Global.SW2_SW1_1
    SW1_SW4_1 = Global.SW2_SW3_1

    SW2_SW1_1 = Global.SW1_SW2_1
    SW2_SW3_1 = Global.SW1_SW4_1
    SW2_SW4_1 = Global.SW1_SW3_1

    SW3_SW2_1 = Global.SW4_SW1_1
    # SW3_SW4_1 = Global.SW4_SW3_1

    SW4_SW1_1 = Global.SW3_SW2_1
    SW4_SW2_1 = Global.SW3_SW1_1
    # SW4_SW3_1 = Global.SW3_SW4_1

    #Lag组连接
    SW3_SW4_2 = Global.SW4_SW3_2
    SW3_SW4_3 = Global.SW4_SW3_3
    SW4_SW3_2 = Global.SW3_SW4_2
    SW4_SW3_3 = Global.SW3_SW4_3

SPN_4358_vlan = 10
SPN_4358_vlan2 = 20
SPN_4358_LSP_dropTime = 50
SPN_4358_LAG_dropTime = 200

def xmlConfig_list1():
    cmd_list1 = []

    # 1、loopback接口
    nc_info = [None, None, None, None, 'loopback0', 'LOOPBACK', 'enable', None, None, None, '216.1.1.1/32', 'mast']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'loopback-interface', 'ip', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    cmd_list1.append(creatConfig(nc_info, nc_yang))

    # 2、接口模式配置
    nc_info = [None, None, None, None, Local.SW1_SW4_1.split('gi')[1], 'disable']
    nc_yang = ['fos-device', 'device', 'ethmode-cfgs', 'ethmode-cfg', 'if-name', 'enable']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW1_SW2_1.split('gi')[1], 'disable']
    nc_yang = ['fos-device', 'device', 'ethmode-cfgs', 'ethmode-cfg', 'if-name', 'enable']
    cmd_list1.append(creatConfig(nc_info, nc_yang))

    # 3、Flexe PHY接口
    nc_info = [None, None, None, None, Local.SW1_SW4_1, 'FLEXE-PHY', 'enable', None, '0', 'auto', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'flexe-ctrlinterface', 'unavailable-timeslot-count', 'fec-mode', 'port-laser-startup-delay-time']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW1_SW2_1, 'FLEXE-PHY', 'enable', None, '0', 'auto', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'flexe-ctrlinterface', 'unavailable-timeslot-count', 'fec-mode', 'port-laser-startup-delay-time']
    cmd_list1.append(creatConfig(nc_info, nc_yang))

    # 4、Flexe Group
    nc_info = [None, None, None, None, 'flexe-group1', 'FLEXE-GROUP', None, 'static', '1', 'disable', '5g', None, Local.SW1_SW4_1, '1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexegrp-ctrlinterface', 'work-mode', 'group-num', 'fccas-enable', 'slot-granularity', 'flexe-group-member', 'flexe-name', 'phy-num']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-group2', 'FLEXE-GROUP', None, 'static', '2', 'disable', '5g', None, Local.SW1_SW2_1, '1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexegrp-ctrlinterface', 'work-mode', 'group-num', 'fccas-enable', 'slot-granularity', 'flexe-group-member', 'flexe-name', 'phy-num']
    cmd_list1.append(creatConfig(nc_info, nc_yang))

    #5、FLEXE-CLIENT
    nc_info = [None, None, None, None, 'flexe-client1/1', 'FLEXE-CLIENT', None, 'terminate', '1', None, Local.SW1_SW4_1, '1', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexeclient-ctrlinterface', 'work-mode', 'client-num', 'client-timeslot', 'flexe-name', 'timeslot1-64', 'timeslot65-128']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-client2/1', 'FLEXE-CLIENT', None, 'terminate', '1', None, Local.SW1_SW2_1, '1', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexeclient-ctrlinterface', 'work-mode', 'client-num', 'client-timeslot', 'flexe-name', 'timeslot1-64', 'timeslot65-128']
    cmd_list1.append(creatConfig(nc_info, nc_yang))

    #6、FLEXE-TUNNEL
    nc_info = [None, None, None, None, 'flexe-tunnel1', 'FLEXE-TUNNEL', None, 'none', 'flexe-client1/1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexetunnel-ctrlinterface', 'protect-type', 'work-flexe-client']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel2', 'FLEXE-TUNNEL', None, 'none', 'flexe-client2/1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexetunnel-ctrlinterface', 'protect-type', 'work-flexe-client']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel1', 'FLEXE-TUNNEL', None, 'layer-3-route', None, '1500', None, '14.1.1.1/24', 'mast']
    nc_yang =  ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexevethif-interface', 'transport-layer', 'ip', 'ipv4-mtu', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel2', 'FLEXE-TUNNEL', None, 'layer-3-route', None, '1500', None, '12.1.1.1/24', 'mast']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexevethif-interface', 'transport-layer', 'ip', 'ipv4-mtu', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel1']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'interface', 'ifname']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel2']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'interface', 'ifname']
    cmd_list1.append(creatConfig(nc_info, nc_yang))

    #7、以太主接口
    nc_info = [None, None, None, None, Local.SW1_port1, 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu']
    cmd_list1.append(creatConfig(nc_info, nc_yang))

    #8、静态ARP配置
    nc_info = [None, None, None, None, '_public_', '12.1.1.2', '80:3a:f4:27:e7:00', 'none']
    nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '_public_', '14.1.1.4', '80:3a:f4:59:01:00', 'none']
    nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type']
    cmd_list1.append(creatConfig(nc_info, nc_yang))

    #9、MPLS LSR ID
    nc_info = [None, None, None, '216.1.1.1']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'router-id']
    cmd_list1.append(creatConfig(nc_info, nc_yang))

    #10、MPLS-TP隧道
    nc_info = [None, None, None, None, 'meg5b7d000c', '7', '123456', '789ABC', None, '1', '1', '2', 'mep', 'enable', '3_33ms', 'disable', 'disable', 'disable', '7', '255', 'disable']
    nc_yang = ['fos-tpoam', 'tpoam', 'meg-cfg', 'meg-list', 'meg-name', 'level', 'icc', 'umc', 'me-list', 'me-name', 'mep-id', 'remote-mep-id', 'mp-type', 'ccm-send-enable', 'ccm-interval', 'aps-send-enable', 'fdi-send-enable', 'csf-send-enable', 'oam-exp', 'oam-ttl', 'dual-lm-enable']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'meg5b7d000d', '7', '123456', '789ABC', None, '2', '1', '2', 'mep', 'enable', '3_33ms', 'enable', 'disable', 'disable', '7', '255', 'disable']
    nc_yang = ['fos-tpoam', 'tpoam', 'meg-cfg', 'meg-list', 'meg-name', 'level', 'icc', 'umc', 'me-list', 'me-name', 'mep-id', 'remote-mep-id', 'mp-type', 'ccm-send-enable', 'ccm-interval', 'aps-send-enable', 'fdi-send-enable', 'csf-send-enable', 'oam-exp', 'oam-ttl', 'dual-lm-enable']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'tunnel1', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'tunnel2', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d000c_0', 'bi-head', 'bi', None, '14.1.1.4', '500', 'flexe-tunnel1', None, '501', 'flexe-tunnel1', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'mpls-te']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d000d_1', 'bi-head', 'bi', None, '12.1.1.2', '502', 'flexe-tunnel2', None, '503', 'flexe-tunnel2', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'mpls-te']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '1', '216.1.1.4', 'static', 'bi', 'private', None, 'primary-lsp', 'bi', '5b7d000c_0', None, None, 'primary', '1']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id', 'destination-ip', 'signal-protocol', 'bi-tunnel', 'aps-mode', 'static-lsp', 'lsp-type', 'lsp-bi', 'lsp-name', 'vpoams', 'vpoam', 'tunnel-type', 'me-name']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '2', '216.1.1.4', 'static', 'bi', 'private', None, 'primary-lsp', 'bi', '5b7d000d_1', None, None, 'primary', '2']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id', 'destination-ip', 'signal-protocol', 'bi-tunnel', 'aps-mode', 'static-lsp', 'lsp-type', 'lsp-bi', 'lsp-name', 'vpoams', 'vpoam', 'tunnel-type', 'me-name']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '1', '1', '2', 'revertive', '5', '0', 'hot-standby']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-bundle', 'id', 'pri-tunnel-id', 'bak-tunnel-id', 'revertive-mode', 'wtr', 'holdoff-time', 'protect-type']
    cmd_list1.append(creatConfig(nc_info, nc_yang))

    #11、L2VPN业务
    nc_info = [None, None, None, None, Local.SW1_port1 +'.'+str(SPN_4358_vlan), 'ETH-SUBIF', None, 'enable', None, 'disable', 'layer-2-switch', None, 'dot1q', None, str(SPN_4358_vlan)]
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'description', 'enabled', 'eth-option', 'loop-block', 'transport-layer', 'if-vlan-cfg', 'termination_type', 'vlan-sub-cfg', 'svlan_min']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pw-tnl-plcy-1534918668', 'TUNNEL-BINGDING', None, '216.1.1.4', '1', 'disable']
    nc_yang = ['fos-tunnelpolicy', 'tnl-plcy', 'tunnel-policies', 'tunnel-policy-list', 'tunnel-policy-name', 'tunnel-policy-mode', 'binding-policy', 'destination', 'tunnel-id', 'tunnel-down-switch']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pwclassname-1534918678', 'enable', 'pw-tnl-plcy-1534918668']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'pw-class', 'pw-class-list', 'pw-class-name', 'control-word', 'tunnel-policy']
    cmd_list1.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'vpws_1', None, Local.SW1_port1 +'.'+str(SPN_4358_vlan), None, '216.1.1.4', '1', 'raw', '16', '16', 'primary', 'pwclassname-1534918678', None]
    nc_yang = ['fos-l2vpn', 'l2vpn', 'vpws', 'vpws-list', 'service-name', 'accessif-list', 'ac-name', 'pw-list', 'peer-ip', 'pw-id', 'pw-type', 'static-transmit-label', 'static-receive-label', 'pw-role', 'pw-class-name', 'qos-vpws-cfg']
    cmd_list1.append(creatConfig(nc_info, nc_yang))

    return cmd_list1

def xmlConfig_list2():
    cmd_list2 = []

    # 1、loopback接口
    nc_info = [None, None, None, None, 'loopback0', 'LOOPBACK', 'enable', None, None, None, '216.1.1.2/32', 'mast']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'loopback-interface', 'ip', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    cmd_list2.append(creatConfig(nc_info, nc_yang))

    # 2、接口模式配置
    nc_info = [None, None, None, None, Local.SW2_SW3_1.split('gi')[1], 'disable']
    nc_yang = ['fos-device', 'device', 'ethmode-cfgs', 'ethmode-cfg', 'if-name', 'enable']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW2_SW1_1.split('gi')[1], 'disable']
    nc_yang = ['fos-device', 'device', 'ethmode-cfgs', 'ethmode-cfg', 'if-name', 'enable']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW2_SW4_1.split('gi')[1], 'disable']
    nc_yang = ['fos-device', 'device', 'ethmode-cfgs', 'ethmode-cfg', 'if-name', 'enable']
    cmd_list2.append(creatConfig(nc_info, nc_yang))

    # 3、Flexe PHY接口
    nc_info = [None, None, None, None, Local.SW2_SW3_1, 'FLEXE-PHY', 'enable', None, '0', 'auto', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'flexe-ctrlinterface', 'unavailable-timeslot-count', 'fec-mode', 'port-laser-startup-delay-time']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW2_SW1_1, 'FLEXE-PHY', 'enable', None, '0', 'auto', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'flexe-ctrlinterface', 'unavailable-timeslot-count', 'fec-mode', 'port-laser-startup-delay-time']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW2_SW4_1, 'FLEXE-PHY', 'enable', None, '0', 'auto', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'flexe-ctrlinterface', 'unavailable-timeslot-count', 'fec-mode', 'port-laser-startup-delay-time']
    cmd_list2.append(creatConfig(nc_info, nc_yang))

    # 4、Flexe Group
    nc_info = [None, None, None, None, 'flexe-group1', 'FLEXE-GROUP', None, 'static', '1', 'disable', '5g', None, Local.SW2_SW3_1, '1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexegrp-ctrlinterface', 'work-mode', 'group-num', 'fccas-enable', 'slot-granularity', 'flexe-group-member', 'flexe-name', 'phy-num']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-group2', 'FLEXE-GROUP', None, 'static', '2', 'disable', '5g', None, Local.SW2_SW1_1, '1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexegrp-ctrlinterface', 'work-mode', 'group-num', 'fccas-enable', 'slot-granularity', 'flexe-group-member', 'flexe-name', 'phy-num']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-group3', 'FLEXE-GROUP', None, 'static', '3', 'disable', '5g', None, Local.SW2_SW4_1, '1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexegrp-ctrlinterface', 'work-mode', 'group-num', 'fccas-enable', 'slot-granularity', 'flexe-group-member', 'flexe-name', 'phy-num']
    cmd_list2.append(creatConfig(nc_info, nc_yang))

    #5、FLEXE-CLIENT
    nc_info = [None, None, None, None, 'flexe-client1/1', 'FLEXE-CLIENT', None, 'terminate', '1', None, Local.SW2_SW3_1, '1', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexeclient-ctrlinterface', 'work-mode', 'client-num', 'client-timeslot', 'flexe-name', 'timeslot1-64', 'timeslot65-128']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-client2/1', 'FLEXE-CLIENT', None, 'terminate', '1', None, Local.SW2_SW1_1, '1', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexeclient-ctrlinterface', 'work-mode', 'client-num', 'client-timeslot', 'flexe-name', 'timeslot1-64', 'timeslot65-128']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-client3/1', 'FLEXE-CLIENT', None, 'terminate', '1', None, Local.SW2_SW4_1, '1', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexeclient-ctrlinterface', 'work-mode', 'client-num', 'client-timeslot', 'flexe-name', 'timeslot1-64', 'timeslot65-128']
    cmd_list2.append(creatConfig(nc_info, nc_yang))

    #6、FLEXE-TUNNEL
    nc_info = [None, None, None, None, 'flexe-tunnel1', 'FLEXE-TUNNEL', None, 'none', 'flexe-client1/1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexetunnel-ctrlinterface', 'protect-type', 'work-flexe-client']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel2', 'FLEXE-TUNNEL', None, 'none', 'flexe-client2/1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexetunnel-ctrlinterface', 'protect-type', 'work-flexe-client']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel1', 'FLEXE-TUNNEL', None, 'layer-3-route', None, '1500', None, '23.1.1.2/24', 'mast']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexevethif-interface', 'transport-layer', 'ip', 'ipv4-mtu', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel2', 'FLEXE-TUNNEL', None, 'layer-3-route', None, '1500', None, '12.1.1.2/24', 'mast']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexevethif-interface', 'transport-layer', 'ip', 'ipv4-mtu', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel1']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'interface', 'ifname']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel2']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'interface', 'ifname']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel3', 'FLEXE-TUNNEL', None, 'none', 'flexe-client3/1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexetunnel-ctrlinterface', 'protect-type', 'work-flexe-client']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel3', 'FLEXE-TUNNEL', None, 'layer-3-route', None, '1500', None, '24.1.1.2/24', 'mast']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexevethif-interface', 'transport-layer', 'ip', 'ipv4-mtu', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel3']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'interface', 'ifname']
    cmd_list2.append(creatConfig(nc_info, nc_yang))

    #7、以太主接口
    nc_info = [None, None, None, None, Local.SW2_port2, 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu']
    cmd_list2.append(creatConfig(nc_info, nc_yang))

    #8、静态ARP配置
    nc_info = [None, None, None, None, '_public_', '12.1.1.1', '80:3a:f4:27:dd:00', 'none']
    nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '_public_', '23.1.1.3', '48:f9:7c:e2:f0:00', 'none']
    nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '_public_', '24.1.1.4', '80:3a:f4:59:01:00', 'none']
    nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type']
    cmd_list2.append(creatConfig(nc_info, nc_yang))

    #9、MPLS LSR ID
    nc_info = [None, None, None, '216.1.1.2']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'router-id']
    cmd_list2.append(creatConfig(nc_info, nc_yang))

    #10、MPLS-TP隧道
    nc_info = [None, None, None, None, 'tunnel1', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d000f_0', 'bi-head', 'bi', None, '23.1.1.3', '600', 'flexe-tunnel1', None, '601', 'flexe-tunnel1', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'mpls-te']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '1', 'no-protect', '216.1.1.3', 'static', 'bi', None, 'primary-lsp', 'bi', '5b7d000f_0']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id', 'protect-type', 'destination-ip', 'signal-protocol', 'bi-tunnel', 'static-lsp', 'lsp-type', 'lsp-bi', 'lsp-name']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d000d_1', 'bi-transit', 'bi', None, '24.1.1.4', '502', 'flexe-tunnel3', None, '502', 'flexe-tunnel2', None, '503', 'flexe-tunnel3', None, '12.1.1.1', '503', 'flexe-tunnel2', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'reverse-in-segment', 'in-label', 'in-ifname', 'reverse-out-segment', 'next-hop', 'out-label', 'out-ifname', 'mpls-te']
    cmd_list2.append(creatConfig(nc_info, nc_yang))

    #11、L2VPN业务
    nc_info = [None, None, None, None, Local.SW2_port2 +'.'+str(SPN_4358_vlan), 'ETH-SUBIF', None, 'enable', None, 'disable', 'layer-2-switch', None, 'dot1q', None, str(SPN_4358_vlan)]
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'description', 'enabled', 'eth-option', 'loop-block', 'transport-layer', 'if-vlan-cfg', 'termination_type', 'vlan-sub-cfg', 'svlan_min']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pw-tnl-plcy-1534918671', 'TUNNEL-BINGDING', None, '216.1.1.3', '1', 'disable']
    nc_yang = ['fos-tunnelpolicy', 'tnl-plcy', 'tunnel-policies', 'tunnel-policy-list', 'tunnel-policy-name', 'tunnel-policy-mode', 'binding-policy', 'destination', 'tunnel-id', 'tunnel-down-switch']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pwclassname-1534918676', 'enable', 'pw-tnl-plcy-1534918671']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'pw-class', 'pw-class-list', 'pw-class-name', 'control-word', 'tunnel-policy']
    cmd_list2.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'vpws_1', None, Local.SW2_port2 +'.'+str(SPN_4358_vlan), None, '216.1.1.3', '1', 'raw', '16', '16', 'primary', 'pwclassname-1534918676', None]
    nc_yang = ['fos-l2vpn', 'l2vpn', 'vpws', 'vpws-list', 'service-name', 'accessif-list', 'ac-name', 'pw-list', 'peer-ip', 'pw-id', 'pw-type', 'static-transmit-label', 'static-receive-label', 'pw-role', 'pw-class-name', 'qos-vpws-cfg']
    cmd_list2.append(creatConfig(nc_info, nc_yang))

    return cmd_list2

def xmlConfig_list3():
    cmd_list3 = []

    # 1、loopback接口
    nc_info = [None, None, None, None, 'loopback0', 'LOOPBACK', 'enable', None, None, None, '216.1.1.3/32', 'mast']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'loopback-interface', 'ip', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    cmd_list3.append(creatConfig(nc_info, nc_yang))

    # 2、接口模式配置
    nc_info = [None, None, None, None, Local.SW3_SW2_1.split('gi')[1], 'disable']
    nc_yang = ['fos-device', 'device', 'ethmode-cfgs', 'ethmode-cfg', 'if-name', 'enable']
    cmd_list3.append(creatConfig(nc_info, nc_yang))

    # 3、Flexe PHY接口
    nc_info = [None, None, None, None, Local.SW3_SW2_1, 'FLEXE-PHY', 'enable', None, '0', 'auto', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'flexe-ctrlinterface', 'unavailable-timeslot-count', 'fec-mode', 'port-laser-startup-delay-time']
    cmd_list3.append(creatConfig(nc_info, nc_yang))

    # 4、Flexe Group
    nc_info = [None, None, None, None, 'flexe-group1', 'FLEXE-GROUP', None, 'static', '1', 'disable', '5g', None, Local.SW3_SW2_1, '1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexegrp-ctrlinterface', 'work-mode', 'group-num', 'fccas-enable', 'slot-granularity', 'flexe-group-member', 'flexe-name', 'phy-num']
    cmd_list3.append(creatConfig(nc_info, nc_yang))

    #5、FLEXE-CLIENT
    nc_info = [None, None, None, None, 'flexe-client1/1', 'FLEXE-CLIENT', None, 'terminate', '1', None, Local.SW3_SW2_1, '1', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexeclient-ctrlinterface', 'work-mode', 'client-num', 'client-timeslot', 'flexe-name', 'timeslot1-64', 'timeslot65-128']
    cmd_list3.append(creatConfig(nc_info, nc_yang))

    #6、FLEXE-TUNNEL
    nc_info = [None, None, None, None, 'flexe-tunnel1', 'FLEXE-TUNNEL', None, 'none', 'flexe-client1/1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexetunnel-ctrlinterface', 'protect-type', 'work-flexe-client']
    cmd_list3.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel1', 'FLEXE-TUNNEL', None, 'layer-3-route', None, '1500', None, '23.1.1.3/24', 'mast']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexevethif-interface', 'transport-layer', 'ip', 'ipv4-mtu', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    cmd_list3.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel1']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'interface', 'ifname']
    cmd_list3.append(creatConfig(nc_info, nc_yang))

    #7、以太主接口
    # nc_info = [None, None, None, None, Local.SW3_SW4_1, 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500', None, '34.1.1.3/24', 'mast']
    # nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    # cmd_list3.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW3_SW4_2, 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu']
    cmd_list3.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW3_SW4_3, 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu']
    cmd_list3.append(creatConfig(nc_info, nc_yang))
    # nc_info = [None, None, None, None, Local.SW3_SW4_1]
    # nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'interface', 'ifname']
    # cmd_list3.append(creatConfig(nc_info, nc_yang))

    #8、静态ARP配置
    nc_info = [None, None, None, None, '_public_', '23.1.1.2', '80:3a:f4:27:e7:00', 'none']
    nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type']
    cmd_list3.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '_public_', '34.1.1.4', '80:3a:f4:59:01:00', 'none']
    nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type']
    cmd_list3.append(creatConfig(nc_info, nc_yang))

    #9、MPLS LSR ID
    nc_info = [None, None, None, '216.1.1.3']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'router-id']
    cmd_list3.append(creatConfig(nc_info, nc_yang))

    #10、Trunk接口
    nc_info = [None, None, None, None, Local.SW3_SW4_2, 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu']
    cmd_list3.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW3_SW4_3, 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu']
    cmd_list3.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'lag1', 'ETH-LAG', None, 'enable', None, 'mac', 'lacp-load', '8', '1', None, Local.SW3_SW4_3, None, Local.SW3_SW4_2, 'layer-3-route', '500000', None, '1500']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'description', 'enabled', 'ethlag-interface', 'lag-arithmetic', 'lag-mode', 'max-active-numbers', 'min-active-numbers', 'lag-add-interface-cfg', 'eth-ifname', 'lag-add-interface-cfg', 'eth-ifname', 'transport-layer', 'bandwidth', 'ip', 'ipv4-mtu']
    cmd_list3.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'lag1.10', 'ETH-SUBIF', None, 'enable', 'layer-2-switch', None, 'dot1q', None, '10']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'description', 'enabled', 'transport-layer', 'if-vlan-cfg', 'termination_type', 'vlan-sub-cfg', 'svlan_min']
    cmd_list3.append(creatConfig(nc_info, nc_yang))

    #11、MPLS-TP隧道
    nc_info = [None, None, None, None, 'tunnel1', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    cmd_list3.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d000f_0', 'bi-head', 'bi', None, '23.1.1.2', '601', 'flexe-tunnel1', None, '600', 'flexe-tunnel1', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'mpls-te']
    cmd_list3.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '1', 'no-protect', '216.1.1.2', 'static', 'bi', None, 'primary-lsp', 'bi', '5b7d000f_0']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id', 'protect-type', 'destination-ip', 'signal-protocol', 'bi-tunnel', 'static-lsp', 'lsp-type', 'lsp-bi', 'lsp-name']
    cmd_list3.append(creatConfig(nc_info, nc_yang))

    #12、L2VPN业务
    nc_info = [None, None, None, None, 'pw-tnl-plcy-1534918671', 'TUNNEL-BINGDING', None, '216.1.1.2', '1', 'disable']
    nc_yang = ['fos-tunnelpolicy', 'tnl-plcy', 'tunnel-policies', 'tunnel-policy-list', 'tunnel-policy-name', 'tunnel-policy-mode', 'binding-policy', 'destination', 'tunnel-id', 'tunnel-down-switch']
    cmd_list3.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pwclassname-1534918676', 'enable', 'pw-tnl-plcy-1534918671']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'pw-class', 'pw-class-list', 'pw-class-name', 'control-word', 'tunnel-policy']
    cmd_list3.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'vpws_1', None, 'lag1.10', None, '216.1.1.2', '1', 'raw', '16', '16', 'primary', 'pwclassname-1534918676', None]
    nc_yang = ['fos-l2vpn', 'l2vpn', 'vpws', 'vpws-list', 'service-name', 'accessif-list', 'ac-name', 'pw-list', 'peer-ip', 'pw-id', 'pw-type', 'static-transmit-label', 'static-receive-label', 'pw-role', 'pw-class-name', 'qos-vpws-cfg']
    cmd_list3.append(creatConfig(nc_info, nc_yang))

    return cmd_list3

def xmlConfig_list4():
    cmd_list4 = []

    # 1、loopback接口
    nc_info = [None, None, None, None, 'loopback0', 'LOOPBACK', 'enable', None, None, None, '216.1.1.4/32', 'mast']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'loopback-interface', 'ip', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    # 2、接口模式配置
    nc_info = [None, None, None, None, Local.SW4_SW1_1.split('gi')[1], 'disable']
    nc_yang = ['fos-device', 'device', 'ethmode-cfgs', 'ethmode-cfg', 'if-name', 'enable']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW4_SW2_1.split('gi')[1], 'disable']
    nc_yang = ['fos-device', 'device', 'ethmode-cfgs', 'ethmode-cfg', 'if-name', 'enable']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    # 3、Flexe PHY接口
    nc_info = [None, None, None, None, Local.SW4_SW1_1, 'FLEXE-PHY', 'enable', None, '0', 'auto', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'flexe-ctrlinterface', 'unavailable-timeslot-count', 'fec-mode', 'port-laser-startup-delay-time']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW4_SW2_1, 'FLEXE-PHY', 'enable', None, '0', 'auto', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'flexe-ctrlinterface', 'unavailable-timeslot-count', 'fec-mode', 'port-laser-startup-delay-time']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    # 4、Flexe Group
    nc_info = [None, None, None, None, 'flexe-group1', 'FLEXE-GROUP', None, 'static', '1', 'disable', '5g', None, Local.SW4_SW1_1, '1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexegrp-ctrlinterface', 'work-mode', 'group-num', 'fccas-enable', 'slot-granularity', 'flexe-group-member', 'flexe-name', 'phy-num']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-group2', 'FLEXE-GROUP', None, 'static', '2', 'disable', '5g', None, Local.SW4_SW2_1, '1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexegrp-ctrlinterface', 'work-mode', 'group-num', 'fccas-enable', 'slot-granularity', 'flexe-group-member', 'flexe-name', 'phy-num']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    #5、FLEXE-CLIENT
    nc_info = [None, None, None, None, 'flexe-client1/1', 'FLEXE-CLIENT', None, 'terminate', '1', None, Local.SW4_SW1_1, '1', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexeclient-ctrlinterface', 'work-mode', 'client-num', 'client-timeslot', 'flexe-name', 'timeslot1-64', 'timeslot65-128']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-client2/1', 'FLEXE-CLIENT', None, 'terminate', '1', None, Local.SW4_SW2_1, '1', '0']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexeclient-ctrlinterface', 'work-mode', 'client-num', 'client-timeslot', 'flexe-name', 'timeslot1-64', 'timeslot65-128']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    #6、FLEXE-TUNNEL
    nc_info = [None, None, None, None, 'flexe-tunnel1', 'FLEXE-TUNNEL', None, 'none', 'flexe-client1/1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexetunnel-ctrlinterface', 'protect-type', 'work-flexe-client']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel1', 'FLEXE-TUNNEL', None, 'layer-3-route', None, '1500', None, '14.1.1.4/24', 'mast']
    nc_yang =  ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexevethif-interface', 'transport-layer', 'ip', 'ipv4-mtu', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel1']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'interface', 'ifname']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel2', 'FLEXE-TUNNEL', None, 'none', 'flexe-client2/1']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexetunnel-ctrlinterface', 'protect-type', 'work-flexe-client']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel2', 'FLEXE-TUNNEL', None, 'layer-3-route', None, '1500', None, '24.1.1.4/24', 'mast']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexevethif-interface', 'transport-layer', 'ip', 'ipv4-mtu', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'flexe-tunnel2']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'interface', 'ifname']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    #7、以太主接口
    nc_info = [None, None, None, None, Local.SW4_SW3_2, 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW4_SW3_3, 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    #8、静态ARP配置
    nc_info = [None, None, None, None, '_public_', '14.1.1.1', '80:3a:f4:27:dd:00', 'none']
    nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '_public_', '24.1.1.2', '80:3A:F4:27:E7:00', 'none']
    nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    #9、MPLS LSR ID
    nc_info = [None, None, None, '216.1.1.4']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'router-id']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    #10、Trunk接口
    nc_info = [None, None, None, None, Local.SW4_SW3_2, 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW4_SW3_3, 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    nc_info = [None, None, None, None, 'lag1', 'ETH-LAG', None, 'enable', None, 'mac', 'lacp-load', '8', '1', None, Local.SW4_SW3_3, None, Local.SW4_SW3_2, 'layer-3-route', '500000', None, '1500']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'description', 'enabled', 'ethlag-interface', 'lag-arithmetic', 'lag-mode', 'max-active-numbers', 'min-active-numbers', 'lag-add-interface-cfg', 'eth-ifname', 'lag-add-interface-cfg', 'eth-ifname', 'transport-layer', 'bandwidth', 'ip', 'ipv4-mtu']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'lag1.10', 'ETH-SUBIF', None, 'enable', 'layer-2-switch', None, 'dot1q', None, '10']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'description', 'enabled', 'transport-layer', 'if-vlan-cfg', 'termination_type', 'vlan-sub-cfg', 'svlan_min']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    #11、MPLS-TP隧道
    nc_info = [None, None, None, None, 'meg5b7d000c', '7', '123456', '789ABC', None, '1', '2', '1', 'mep', 'enable', '3_33ms', 'disable', 'disable', 'disable', '7', '255', 'disable']
    nc_yang = ['fos-tpoam', 'tpoam', 'meg-cfg', 'meg-list', 'meg-name', 'level', 'icc', 'umc', 'me-list', 'me-name', 'mep-id', 'remote-mep-id', 'mp-type', 'ccm-send-enable', 'ccm-interval', 'aps-send-enable', 'fdi-send-enable', 'csf-send-enable', 'oam-exp', 'oam-ttl', 'dual-lm-enable']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'meg5b7d000d', '7', '123456', '789ABC', None, '2', '2', '1', 'mep', 'enable', '3_33ms', 'enable', 'disable', 'disable', '7', '255', 'disable']
    nc_yang = ['fos-tpoam', 'tpoam', 'meg-cfg', 'meg-list', 'meg-name', 'level', 'icc', 'umc', 'me-list', 'me-name', 'mep-id', 'remote-mep-id', 'mp-type', 'ccm-send-enable', 'ccm-interval', 'aps-send-enable', 'fdi-send-enable', 'csf-send-enable', 'oam-exp', 'oam-ttl', 'dual-lm-enable']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'tunnel1', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'tunnel2', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d000c_0', 'bi-head', 'bi', None, '14.1.1.1', '501', 'flexe-tunnel1', None, '500', 'flexe-tunnel1', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'mpls-te']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d000d_1', 'bi-head', 'bi', None, '24.1.1.2', '503', 'flexe-tunnel2', None, '502', 'flexe-tunnel2', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'mpls-te']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    nc_info = [None, None, None, None, '1', '216.1.1.1', 'static', 'bi', 'private', None, 'primary-lsp', 'bi', '5b7d000c_0', None, None, 'primary', '1']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id', 'destination-ip', 'signal-protocol', 'bi-tunnel', 'aps-mode', 'static-lsp', 'lsp-type', 'lsp-bi', 'lsp-name', 'vpoams', 'vpoam', 'tunnel-type', 'me-name']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '2', '216.1.1.1', 'static', 'bi', 'private', None, 'primary-lsp', 'bi', '5b7d000d_1', None, None, 'primary', '2']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id', 'destination-ip', 'signal-protocol', 'bi-tunnel', 'aps-mode', 'static-lsp', 'lsp-type', 'lsp-bi', 'lsp-name', 'vpoams', 'vpoam', 'tunnel-type', 'me-name']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '1', '1', '2', 'revertive', '5', '0', 'hot-standby']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-bundle', 'id', 'pri-tunnel-id', 'bak-tunnel-id', 'revertive-mode', 'wtr', 'holdoff-time', 'protect-type']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    #12、L2VPN业务
    nc_info = [None, None, None, None, 'pw-tnl-plcy-1534918668', 'TUNNEL-BINGDING', None, '216.1.1.1', '1', 'disable']
    nc_yang = ['fos-tunnelpolicy', 'tnl-plcy', 'tunnel-policies', 'tunnel-policy-list', 'tunnel-policy-name', 'tunnel-policy-mode', 'binding-policy', 'destination', 'tunnel-id', 'tunnel-down-switch']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pwclassname-1534918678', 'enable', 'pw-tnl-plcy-1534918668']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'pw-class', 'pw-class-list', 'pw-class-name', 'control-word', 'tunnel-policy']
    cmd_list4.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'vpws_1', None, 'lag1.10', None, '216.1.1.1', '1', 'raw', '16', '16', 'primary', 'pwclassname-1534918678', None]
    nc_yang = ['fos-l2vpn', 'l2vpn', 'vpws', 'vpws-list', 'service-name', 'accessif-list', 'ac-name', 'pw-list', 'peer-ip', 'pw-id', 'pw-type', 'static-transmit-label', 'static-receive-label', 'pw-role', 'pw-class-name', 'qos-vpws-cfg']
    cmd_list4.append(creatConfig(nc_info, nc_yang))

    return cmd_list4

def xmlConfig_temp():
    cmd_list1_temp, cmd_list2_temp, cmd_list3_temp, cmd_list4_temp = [], [], [], []

    nc_info = [None, None, None, None, 'meg5b7d0018', '7', '123456', '789ABC', None, '3', '1', '2', 'mep', 'enable', '3_33ms', 'disable', 'disable', 'disable', '7', '255', 'disable']
    nc_yang = ['fos-tpoam', 'tpoam', 'meg-cfg', 'meg-list', 'meg-name', 'level', 'icc', 'umc', 'me-list', 'me-name', 'mep-id', 'remote-mep-id', 'mp-type', 'ccm-send-enable', 'ccm-interval', 'aps-send-enable', 'fdi-send-enable', 'csf-send-enable', 'oam-exp', 'oam-ttl', 'dual-lm-enable']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'meg5b7d0019', '7', '123456', '789ABC', None, '4', '1', '2', 'mep', 'enable', '3_33ms', 'enable', 'disable', 'disable', '7', '255', 'disable']
    nc_yang = ['fos-tpoam', 'tpoam', 'meg-cfg', 'meg-list', 'meg-name', 'level', 'icc', 'umc', 'me-list', 'me-name', 'mep-id', 'remote-mep-id', 'mp-type', 'ccm-send-enable', 'ccm-interval', 'aps-send-enable', 'fdi-send-enable', 'csf-send-enable', 'oam-exp', 'oam-ttl', 'dual-lm-enable']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'tunnel3', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'tunnel4', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d0018_0', 'bi-head', 'bi', None, '14.1.1.4', '650', 'flexe-tunnel1', None, '651', 'flexe-tunnel1', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'mpls-te']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d0019_1', 'bi-head', 'bi', None, '12.1.1.2', '652', 'flexe-tunnel2', None, '653', 'flexe-tunnel2', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'mpls-te']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '3', '216.1.1.4', 'static', 'bi', 'private', None, 'primary-lsp', 'bi', '5b7d0018_0', None, None, 'primary', '3']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id', 'destination-ip', 'signal-protocol', 'bi-tunnel', 'aps-mode', 'static-lsp', 'lsp-type', 'lsp-bi', 'lsp-name', 'vpoams', 'vpoam', 'tunnel-type', 'me-name']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '4', '216.1.1.4', 'static', 'bi', 'private', None, 'primary-lsp', 'bi', '5b7d0019_1', None, None, 'primary', '4']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id', 'destination-ip', 'signal-protocol', 'bi-tunnel', 'aps-mode', 'static-lsp', 'lsp-type', 'lsp-bi', 'lsp-name', 'vpoams', 'vpoam', 'tunnel-type', 'me-name']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '2', '3', '4', 'revertive', '5', '0', 'hot-standby']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-bundle', 'id', 'pri-tunnel-id', 'bak-tunnel-id', 'revertive-mode', 'wtr', 'holdoff-time', 'protect-type']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW1_port1 +'.'+str(SPN_4358_vlan2), 'ETH-SUBIF', None, 'enable', None, 'disable', 'layer-2-switch', None, 'dot1q', None, str(SPN_4358_vlan2)]
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'description', 'enabled', 'eth-option', 'loop-block', 'transport-layer', 'if-vlan-cfg', 'termination_type', 'vlan-sub-cfg', 'svlan_min']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pw-tnl-plcy-1534918680', 'TUNNEL-BINGDING', None, '216.1.1.4', '3', 'disable']
    nc_yang = ['fos-tunnelpolicy', 'tnl-plcy', 'tunnel-policies', 'tunnel-policy-list', 'tunnel-policy-name', 'tunnel-policy-mode', 'binding-policy', 'destination', 'tunnel-id', 'tunnel-down-switch']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pwclassname-1534918685', 'enable', 'pw-tnl-plcy-1534918680']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'pw-class', 'pw-class-list', 'pw-class-name', 'control-word', 'tunnel-policy']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'vpws_2', None, Local.SW1_port1 +'.'+str(SPN_4358_vlan2), None, '216.1.1.4', '2', 'raw', '17', '17', 'primary', 'pwclassname-1534918685', None]
    nc_yang = ['fos-l2vpn', 'l2vpn', 'vpws', 'vpws-list', 'service-name', 'accessif-list', 'ac-name', 'pw-list', 'peer-ip', 'pw-id', 'pw-type', 'static-transmit-label', 'static-receive-label', 'pw-role', 'pw-class-name', 'qos-vpws-cfg']
    cmd_list1_temp.append(creatConfig(nc_info, nc_yang))

    nc_info = [None, None, None, None, '5b7d0019_1', 'bi-transit', 'bi', None, '24.1.1.4', '652', 'flexe-tunnel3', None, '652', 'flexe-tunnel2', None, '653', 'flexe-tunnel3', None, '12.1.1.1', '653', 'flexe-tunnel2', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'reverse-in-segment', 'in-label', 'in-ifname', 'reverse-out-segment', 'next-hop', 'out-label', 'out-ifname', 'mpls-te']
    cmd_list2_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'tunnel2', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    cmd_list2_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d001a_0', 'bi-head', 'bi', None, '23.1.1.3', '550', 'flexe-tunnel1', None, '551', 'flexe-tunnel1', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'mpls-te']
    cmd_list2_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '2', 'no-protect', '216.1.1.3', 'static', 'bi', None, 'primary-lsp', 'bi', '5b7d001a_0']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id', 'protect-type', 'destination-ip', 'signal-protocol', 'bi-tunnel', 'static-lsp', 'lsp-type', 'lsp-bi', 'lsp-name']
    cmd_list2_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, Local.SW2_port2 +'.'+str(SPN_4358_vlan2), 'ETH-SUBIF', None, 'enable', None, 'disable', 'layer-2-switch', None, 'dot1q', None, str(SPN_4358_vlan2)]
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'description', 'enabled', 'eth-option', 'loop-block', 'transport-layer', 'if-vlan-cfg', 'termination_type', 'vlan-sub-cfg', 'svlan_min']
    cmd_list2_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pw-tnl-plcy-1534918682', 'TUNNEL-BINGDING', None, '216.1.1.3', '2', 'disable']
    nc_yang = ['fos-tunnelpolicy', 'tnl-plcy', 'tunnel-policies', 'tunnel-policy-list', 'tunnel-policy-name', 'tunnel-policy-mode', 'binding-policy', 'destination', 'tunnel-id', 'tunnel-down-switch']
    cmd_list2_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pwclassname-1534918687', 'enable', 'pw-tnl-plcy-1534918682']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'pw-class', 'pw-class-list', 'pw-class-name', 'control-word', 'tunnel-policy']
    cmd_list2_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'vpws_2', None, Local.SW2_port2 +'.'+str(SPN_4358_vlan2), None, '216.1.1.3', '2', 'raw', '17', '17', 'primary', 'pwclassname-1534918687', None]
    nc_yang = ['fos-l2vpn', 'l2vpn', 'vpws', 'vpws-list', 'service-name', 'accessif-list', 'ac-name', 'pw-list', 'peer-ip', 'pw-id', 'pw-type', 'static-transmit-label', 'static-receive-label', 'pw-role', 'pw-class-name', 'qos-vpws-cfg']
    cmd_list2_temp.append(creatConfig(nc_info, nc_yang))

    nc_info = [None, None, None, None, 'tunnel2', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    cmd_list3_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d001a_0', 'bi-head', 'bi', None, '23.1.1.2', '551', 'flexe-tunnel1', None, '550', 'flexe-tunnel1', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'mpls-te']
    cmd_list3_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '2', 'no-protect', '216.1.1.2', 'static', 'bi', None, 'primary-lsp', 'bi', '5b7d001a_0']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id', 'protect-type', 'destination-ip', 'signal-protocol', 'bi-tunnel', 'static-lsp', 'lsp-type', 'lsp-bi', 'lsp-name']
    cmd_list3_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'lag1.20', 'ETH-SUBIF', None, 'enable', 'layer-2-switch', None, 'dot1q', None, '20']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'description', 'enabled', 'transport-layer', 'if-vlan-cfg', 'termination_type', 'vlan-sub-cfg', 'svlan_min']
    cmd_list3_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pw-tnl-plcy-1534918682', 'TUNNEL-BINGDING', None, '216.1.1.2', '2', 'disable']
    nc_yang = ['fos-tunnelpolicy', 'tnl-plcy', 'tunnel-policies', 'tunnel-policy-list', 'tunnel-policy-name', 'tunnel-policy-mode', 'binding-policy', 'destination', 'tunnel-id', 'tunnel-down-switch']
    cmd_list3_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pwclassname-1534918687', 'enable', 'pw-tnl-plcy-1534918682']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'pw-class', 'pw-class-list', 'pw-class-name', 'control-word', 'tunnel-policy']
    cmd_list3_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'vpws_2', None, 'lag1.20', None, '216.1.1.2', '2', 'raw', '17', '17', 'primary', 'pwclassname-1534918687', None]
    nc_yang = ['fos-l2vpn', 'l2vpn', 'vpws', 'vpws-list', 'service-name', 'accessif-list', 'ac-name', 'pw-list', 'peer-ip', 'pw-id', 'pw-type', 'static-transmit-label', 'static-receive-label', 'pw-role', 'pw-class-name', 'qos-vpws-cfg']
    cmd_list3_temp.append(creatConfig(nc_info, nc_yang))

    nc_info = [None, None, None, None, 'meg5b7d0018', '7', '123456', '789ABC', None, '3', '2', '1', 'mep', 'enable', '3_33ms', 'disable', 'disable', 'disable', '7', '255', 'disable']
    nc_yang = ['fos-tpoam', 'tpoam', 'meg-cfg', 'meg-list', 'meg-name', 'level', 'icc', 'umc', 'me-list', 'me-name', 'mep-id', 'remote-mep-id', 'mp-type', 'ccm-send-enable', 'ccm-interval', 'aps-send-enable', 'fdi-send-enable', 'csf-send-enable', 'oam-exp', 'oam-ttl', 'dual-lm-enable']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'meg5b7d0019', '7', '123456', '789ABC', None, '4', '2', '1', 'mep', 'enable', '3_33ms', 'enable', 'disable', 'disable', '7', '255', 'disable']
    nc_yang = ['fos-tpoam', 'tpoam', 'meg-cfg', 'meg-list', 'meg-name', 'level', 'icc', 'umc', 'me-list', 'me-name', 'mep-id', 'remote-mep-id', 'mp-type', 'ccm-send-enable', 'ccm-interval', 'aps-send-enable', 'fdi-send-enable', 'csf-send-enable', 'oam-exp', 'oam-ttl', 'dual-lm-enable']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'tunnel3', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'tunnel4', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d0018_0', 'bi-head', 'bi', None, '14.1.1.1', '651', 'flexe-tunnel1', None, '650', 'flexe-tunnel1', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'mpls-te']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '5b7d0019_1', 'bi-head', 'bi', None, '24.1.1.2', '653', 'flexe-tunnel2', None, '652', 'flexe-tunnel2', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'bi-lsp-type', 'out-segment', 'next-hop', 'out-label', 'out-ifname', 'in-segment', 'in-label', 'in-ifname', 'mpls-te']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))

    nc_info = [None, None, None, None, '3', '216.1.1.1', 'static', 'bi', 'private', None, 'primary-lsp', 'bi', '5b7d0018_0', None, None, 'primary', '3']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id', 'destination-ip', 'signal-protocol', 'bi-tunnel', 'aps-mode', 'static-lsp', 'lsp-type', 'lsp-bi', 'lsp-name', 'vpoams', 'vpoam', 'tunnel-type', 'me-name']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '4', '216.1.1.1', 'static', 'bi', 'private', None, 'primary-lsp', 'bi', '5b7d0019_1', None, None, 'primary', '4']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id', 'destination-ip', 'signal-protocol', 'bi-tunnel', 'aps-mode', 'static-lsp', 'lsp-type', 'lsp-bi', 'lsp-name', 'vpoams', 'vpoam', 'tunnel-type', 'me-name']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, '2', '3', '4', 'revertive', '5', '0', 'hot-standby']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-bundle', 'id', 'pri-tunnel-id', 'bak-tunnel-id', 'revertive-mode', 'wtr', 'holdoff-time', 'protect-type']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'lag1.20', 'ETH-SUBIF', None, 'enable', 'layer-2-switch', None, 'dot1q', None, '20']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'description', 'enabled', 'transport-layer', 'if-vlan-cfg', 'termination_type', 'vlan-sub-cfg', 'svlan_min']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pw-tnl-plcy-1534918680', 'TUNNEL-BINGDING', None, '216.1.1.1', '3', 'disable']
    nc_yang = ['fos-tunnelpolicy', 'tnl-plcy', 'tunnel-policies', 'tunnel-policy-list', 'tunnel-policy-name', 'tunnel-policy-mode', 'binding-policy', 'destination', 'tunnel-id', 'tunnel-down-switch']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'pwclassname-1534918685', 'enable', 'pw-tnl-plcy-1534918680']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'pw-class', 'pw-class-list', 'pw-class-name', 'control-word', 'tunnel-policy']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))
    nc_info = [None, None, None, None, 'vpws_2', None, 'lag1.20', None, '216.1.1.1', '2', 'raw', '17', '17', 'primary', 'pwclassname-1534918685', None]
    nc_yang = ['fos-l2vpn', 'l2vpn', 'vpws', 'vpws-list', 'service-name', 'accessif-list', 'ac-name', 'pw-list', 'peer-ip', 'pw-id', 'pw-type', 'static-transmit-label', 'static-receive-label', 'pw-role', 'pw-class-name', 'qos-vpws-cfg']
    cmd_list4_temp.append(creatConfig(nc_info, nc_yang))

    return cmd_list1_temp, cmd_list2_temp, cmd_list3_temp, cmd_list4_temp

def xmlConfig_temp_del():
    cmd_list1_temp, cmd_list2_temp, cmd_list3_temp, cmd_list4_temp = [], [], [], []

    nc_info = [None, None, None, None, 'vpws_2']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'vpws', 'vpws-list', 'service-name']
    nc_del = ['vpws-list']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'pw-tnl-plcy-1534918680', 'TUNNEL-BINGDING']
    nc_yang = ['fos-tunnelpolicy', 'tnl-plcy', 'tunnel-policies', 'tunnel-policy-list', 'tunnel-policy-name', 'tunnel-policy-mode']
    nc_del = ['tunnel-policy-list']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'pwclassname-1534918685']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'pw-class', 'pw-class-list', 'pw-class-name']
    nc_del = ['pw-class-list']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, Local.SW1_port1 +'.'+str(SPN_4358_vlan2), 'ETH-SUBIF']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    nc_del = ['interface']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '2']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-bundle', 'id']
    nc_del = ['tunnel-bundle']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '4']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id']
    nc_del = ['tunnel-te']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '3']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id']
    nc_del = ['tunnel-te']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '5b7d0019_1', 'bi-head', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'mpls-te']
    nc_del = ['static-te-lsp']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '5b7d0018_0', 'bi-head', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'mpls-te']
    nc_del = ['static-te-lsp']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'tunnel3', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    nc_del = ['interface']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'tunnel4', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    nc_del = ['interface']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'meg5b7d0018']
    nc_yang = ['fos-tpoam', 'tpoam', 'meg-cfg', 'meg-list', 'meg-name']
    nc_del = ['meg-list']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'meg5b7d0019']
    nc_yang = ['fos-tpoam', 'tpoam', 'meg-cfg', 'meg-list', 'meg-name']
    nc_del = ['meg-list']
    cmd_list1_temp.append(deleteConfig(nc_info, nc_yang, nc_del))

    nc_info = [None, None, None, None, 'vpws_2']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'vpws', 'vpws-list', 'service-name']
    nc_del = ['vpws-list']
    cmd_list2_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'pw-tnl-plcy-1534918682', 'TUNNEL-BINGDING']
    nc_yang = ['fos-tunnelpolicy', 'tnl-plcy', 'tunnel-policies', 'tunnel-policy-list', 'tunnel-policy-name', 'tunnel-policy-mode']
    nc_del = ['tunnel-policy-list']
    cmd_list2_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'pwclassname-1534918687']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'pw-class', 'pw-class-list', 'pw-class-name']
    nc_del = ['pw-class-list']
    cmd_list2_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, Local.SW2_port2 +'.'+str(SPN_4358_vlan2), 'ETH-SUBIF']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    nc_del = ['interface']
    cmd_list2_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '5b7d0019_1', 'bi-transit', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'mpls-te']
    nc_del = ['static-te-lsp']
    cmd_list2_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '2']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id']
    nc_del = ['tunnel-te']
    cmd_list2_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '5b7d001a_0', 'bi-head', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'mpls-te']
    nc_del = ['static-te-lsp']
    cmd_list2_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'tunnel2', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    nc_del = ['interface']
    cmd_list2_temp.append(deleteConfig(nc_info, nc_yang, nc_del))

    nc_info = [None, None, None, None, 'vpws_2']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'vpws', 'vpws-list', 'service-name']
    nc_del = ['vpws-list']
    cmd_list3_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'pw-tnl-plcy-1534918682', 'TUNNEL-BINGDING']
    nc_yang = ['fos-tunnelpolicy', 'tnl-plcy', 'tunnel-policies', 'tunnel-policy-list', 'tunnel-policy-name', 'tunnel-policy-mode']
    nc_del = ['tunnel-policy-list']
    cmd_list3_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'pwclassname-1534918687']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'pw-class', 'pw-class-list', 'pw-class-name']
    nc_del = ['pw-class-list']
    cmd_list3_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'lag1.20', 'ETH-SUBIF']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    nc_del = ['interface']
    cmd_list3_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '2']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id']
    nc_del = ['tunnel-te']
    cmd_list3_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '5b7d001a_0', 'bi-head', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'mpls-te']
    nc_del = ['static-te-lsp']
    cmd_list3_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'tunnel2', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    nc_del = ['interface']
    cmd_list3_temp.append(deleteConfig(nc_info, nc_yang, nc_del))

    nc_info = [None, None, None, None, 'vpws_2']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'vpws', 'vpws-list', 'service-name']
    nc_del = ['vpws-list']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'pw-tnl-plcy-1534918680', 'TUNNEL-BINGDING']
    nc_yang = ['fos-tunnelpolicy', 'tnl-plcy', 'tunnel-policies', 'tunnel-policy-list', 'tunnel-policy-name', 'tunnel-policy-mode']
    nc_del = ['tunnel-policy-list']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'pwclassname-1534918685']
    nc_yang = ['fos-l2vpn', 'l2vpn', 'pw-class', 'pw-class-list', 'pw-class-name']
    nc_del = ['pw-class-list']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'lag1.20', 'ETH-SUBIF']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    nc_del = ['interface']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '2']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-bundle', 'id']
    nc_del = ['tunnel-bundle']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '4']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id']
    nc_del = ['tunnel-te']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '3']
    nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'tunnel-te', 'id']
    nc_del = ['tunnel-te']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '5b7d0019_1', 'bi-head', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'mpls-te']
    nc_del = ['static-te-lsp']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, '5b7d0018_0', 'bi-head', None]
    nc_yang = ['fos-mpls', 'mpls', 'static-te-lsps', 'static-te-lsp', 'lsp-name', 'lsp-role', 'mpls-te']
    nc_del = ['static-te-lsp']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'tunnel3', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    nc_del = ['interface']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'tunnel4', 'TUNNEL']
    nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type']
    nc_del = ['interface']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'meg5b7d0018']
    nc_yang = ['fos-tpoam', 'tpoam', 'meg-cfg', 'meg-list', 'meg-name']
    nc_del = ['meg-list']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))
    nc_info = [None, None, None, None, 'meg5b7d0019']
    nc_yang = ['fos-tpoam', 'tpoam', 'meg-cfg', 'meg-list', 'meg-name']
    nc_del = ['meg-list']
    cmd_list4_temp.append(deleteConfig(nc_info, nc_yang, nc_del))

    return cmd_list1_temp, cmd_list2_temp, cmd_list3_temp, cmd_list4_temp

def SPN_4358_test():
    SPN_4358_flag = False
    try:
        initialFunction()
        dut1, dut2, dut3, dut4 = Local.SW1, Local.SW2, Local.SW3, Local.SW4

        # 设备1、2、3、4配置生成
        cmd_list1 = xmlConfig_list1()
        cmd_list2 = xmlConfig_list2()
        cmd_list3 = xmlConfig_list3()
        cmd_list4 = xmlConfig_list4()

        # 下发全部配置
        print("SPN_4358_test下发配置开始")
        cmd_del = multi_edit_conf([dut1, dut2, dut3, dut4], [cmd_list1, cmd_list2, cmd_list3, cmd_list4])
        print("SPN_4358_test下发配置结束")

        # 用例测试步骤开始，注意：告警、性能无法通过yang查看，实际不做检查
        print("SPN_4358_test测试步骤开始")
        cmd_list_temp = ['none']
        #仪表初始化，占用端口，配置流
        importPackage()  #导入仪表库文件
        STC = FHstcAPI()
        chassisip = Local.tester_ip
        portUsed = '{%s} {%s}' % (Local.port1, Local.port2)
        STC.port_init(chassisip, portUsed)

        STC.streamconfig('-portHandle port1 -insertStreamSum 1 -editStreamID 1 -SchedulingMode rateBased -load 10000 -loadUnit FRAMES_PER_SECOND -fixedFrameLength 256')
        STC.ipconfig('-portHandle port1 -streamID 1 -ethSrcMac 00:11:00:02:05:01 -ethDstMac 00:11:00:02:05:02 -insertVlanSum 1 '
            '-editVlanID 1 -vlanId {} -vlanPri 111 -ipSourceAddr 1.11.32.2 -ipDestAddr 2.12.32.1 -ipGateWay 1.1.1.1'.format(SPN_4358_vlan))
        STC.streamconfig('-portHandle port2 -insertStreamSum 1 -editStreamID 1 -SchedulingMode rateBased -load 10000 -loadUnit FRAMES_PER_SECOND -fixedFrameLength 256')
        STC.ipconfig('-portHandle port2 -streamID 1 -ethSrcMac 00:11:00:02:05:02 -ethDstMac 00:11:00:02:05:01 -insertVlanSum 1 '
            '-editVlanID 1 -vlanId {} -vlanPri 111 -ipSourceAddr 2.12.32.1 -ipDestAddr 1.11.32.2 -ipGateWay 1.1.1.1'.format(SPN_4358_vlan))

        # 1、操作：无；检查：以太网业务丢包、LSP1:1保护、Lag保护状态、告警、性能
        print("SPN_4358_test 1.1测试步骤开始")
        STC.clearResults('port1,port2')
        STC.startTraffic('port1,port2', '5')
        time.sleep(10)
        STC.stopTraffic('port1,port2')
        ID1TX = STC.streamResultView('port1', '1', 'txFrameCountStream')
        ID1RX = STC.streamResultView('port1', '1', 'rxFrameCountStream')
        ID2TX = STC.streamResultView('port2', '1', 'txFrameCountStream')
        ID2RX = STC.streamResultView('port2', '1', 'rxFrameCountStream')
        Stream_Check_Count(ID1TX, ID1RX)
        Stream_Check_Count(ID2TX, ID2RX)

        nc_info_get = [None, None, None, None, None]
        nc_yang_get = ['fos-mpls-oper', 'mpls-oper', 'tunnel-protect-groups', 'tunnel-bundle-protect-groups', 'tunnel-bundle-protect-group']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='1', switch_state='normal', primary_lsp_state='normal', secondary_lsp_state='normal')

        nc_info_get = [None, None, None, None]
        nc_yang_get = ['fos-ethif-lag-oper', 'ethlagif-oper', 'ethlagif-states', 'ethlagif-state']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_lag_staus(rpc_info=status_result, lag_name='lag1', state='up', lag_mode='lacp-load', load_balance='mac')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_2, select_state='Active')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_3, select_state='Active')

        # 2、操作：LSP1:1保护主用路径中断；检查：以太网业务丢包、LSP1:1保护、Lag保护状态、告警、性能
        print("SPN_4358_test 2.1测试步骤开始")
        STC.clearResults('port1,port2')
        STC.startTraffic('port1,port2', '5')

        nc_info = [None, None, None, None, Local.SW1_SW4_1, 'FLEXE-PHY', 'disable']
        nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled']
        cmd_list_temp[0] = creatConfig(nc_info, nc_yang)
        multi_edit_conf([dut1], [cmd_list_temp])
        time.sleep(3)

        nc_info_get = [None, None, None, None, None]
        nc_yang_get = ['fos-mpls-oper', 'mpls-oper', 'tunnel-protect-groups', 'tunnel-bundle-protect-groups', 'tunnel-bundle-protect-group']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='1', switch_state='switch', primary_lsp_state='sf', secondary_lsp_state='normal')

        nc_info_get = [None, None, None, None]
        nc_yang_get = ['fos-ethif-lag-oper', 'ethlagif-oper', 'ethlagif-states', 'ethlagif-state']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_lag_staus(rpc_info=status_result, lag_name='lag1', state='up', lag_mode='lacp-load', load_balance='mac')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_2, select_state='Active')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_3, select_state='Active')

        STC.stopTraffic('port1,port2')
        ID1TX = STC.streamResultView('port1', '1', 'txFrameCountStream')
        ID1RX = STC.streamResultView('port1', '1', 'rxFrameCountStream')
        ID2TX = STC.streamResultView('port2', '1', 'txFrameCountStream')
        ID2RX = STC.streamResultView('port2', '1', 'rxFrameCountStream')
        Stream_Check_DropCount(ID1TX, ID1RX, 10000.0, SPN_4358_LSP_dropTime)
        Stream_Check_DropCount(ID2TX, ID2RX, 10000.0, SPN_4358_LSP_dropTime)

        # 3、操作：LSP1:1保护主用路径恢复；检查：以太网业务丢包、LSP1:1保护、Lag保护状态、告警、性能
        print("SPN_4358_test 3.1测试步骤开始")
        STC.clearResults('port1,port2')
        STC.startTraffic('port1,port2', '5')

        nc_info = [None, None, None, None, Local.SW1_SW4_1, 'FLEXE-PHY', 'enable']
        nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled']
        cmd_list_temp[0] = creatConfig(nc_info, nc_yang)
        multi_edit_conf([dut1], [cmd_list_temp])
        time.sleep(3)

        nc_info_get = [None, None, None, None, None]
        nc_yang_get = ['fos-mpls-oper', 'mpls-oper', 'tunnel-protect-groups', 'tunnel-bundle-protect-groups', 'tunnel-bundle-protect-group']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='1', switch_state='wait-to-restore', primary_lsp_state='normal', secondary_lsp_state='normal')

        nc_info_get = [None, None, None, None]
        nc_yang_get = ['fos-ethif-lag-oper', 'ethlagif-oper', 'ethlagif-states', 'ethlagif-state']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_lag_staus(rpc_info=status_result, lag_name='lag1', state='up', lag_mode='lacp-load', load_balance='mac')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_2, select_state='Active')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_3, select_state='Active')

        time.sleep(305)
        nc_info_get = [None, None, None, None, None]
        nc_yang_get = ['fos-mpls-oper', 'mpls-oper', 'tunnel-protect-groups', 'tunnel-bundle-protect-groups', 'tunnel-bundle-protect-group']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='1', switch_state='normal', primary_lsp_state='normal', secondary_lsp_state='normal')

        STC.stopTraffic('port1,port2')
        ID1TX = STC.streamResultView('port1', '1', 'txFrameCountStream')
        ID1RX = STC.streamResultView('port1', '1', 'rxFrameCountStream')
        ID2TX = STC.streamResultView('port2', '1', 'txFrameCountStream')
        ID2RX = STC.streamResultView('port2', '1', 'rxFrameCountStream')
        Stream_Check_DropCount(ID1TX, ID1RX, 10000.0, SPN_4358_LSP_dropTime)
        Stream_Check_DropCount(ID2TX, ID2RX, 10000.0, SPN_4358_LSP_dropTime)

        # 4、操作：LSP1:1保护备用路径中断；检查：以太网业务丢包、LSP1:1保护、Lag保护状态、告警、性能
        print("SPN_4358_test 4.1测试步骤开始")
        STC.clearResults('port1,port2')
        STC.startTraffic('port1,port2', '5')

        nc_info = [None, None, None, None, Local.SW1_SW2_1, 'FLEXE-PHY', 'disable']
        nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled']
        cmd_list_temp[0] = creatConfig(nc_info, nc_yang)
        multi_edit_conf([dut1], [cmd_list_temp])
        time.sleep(3)

        nc_info_get = [None, None, None, None, None]
        nc_yang_get = ['fos-mpls-oper', 'mpls-oper', 'tunnel-protect-groups', 'tunnel-bundle-protect-groups', 'tunnel-bundle-protect-group']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='1', switch_state='normal', primary_lsp_state='normal', secondary_lsp_state='sf')

        nc_info_get = [None, None, None, None]
        nc_yang_get = ['fos-ethif-lag-oper', 'ethlagif-oper', 'ethlagif-states', 'ethlagif-state']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_lag_staus(rpc_info=status_result, lag_name='lag1', state='up', lag_mode='lacp-load', load_balance='mac')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_2, select_state='Active')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_3, select_state='Active')

        STC.stopTraffic('port1,port2')
        ID1TX = STC.streamResultView('port1', '1', 'txFrameCountStream')
        ID1RX = STC.streamResultView('port1', '1', 'rxFrameCountStream')
        ID2TX = STC.streamResultView('port2', '1', 'txFrameCountStream')
        ID2RX = STC.streamResultView('port2', '1', 'rxFrameCountStream')
        Stream_Check_Count(ID1TX, ID1RX)
        Stream_Check_Count(ID2TX, ID2RX)

        # 5、操作：LSP1:1保护备用路径恢复；检查：以太网业务丢包、LSP1:1保护、Lag保护状态、告警、性能
        print("SPN_4358_test 5.1测试步骤开始")
        STC.clearResults('port1,port2')
        STC.startTraffic('port1,port2', '5')

        nc_info = [None, None, None, None, Local.SW1_SW2_1, 'FLEXE-PHY', 'enable']
        nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled']
        cmd_list_temp[0] = creatConfig(nc_info, nc_yang)
        multi_edit_conf([dut1], [cmd_list_temp])
        time.sleep(3)

        nc_info_get = [None, None, None, None, None]
        nc_yang_get = ['fos-mpls-oper', 'mpls-oper', 'tunnel-protect-groups', 'tunnel-bundle-protect-groups', 'tunnel-bundle-protect-group']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='1', switch_state='normal', primary_lsp_state='normal', secondary_lsp_state='normal')

        nc_info_get = [None, None, None, None]
        nc_yang_get = ['fos-ethif-lag-oper', 'ethlagif-oper', 'ethlagif-states', 'ethlagif-state']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_lag_staus(rpc_info=status_result, lag_name='lag1', state='up', lag_mode='lacp-load', load_balance='mac')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_2, select_state='Active')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_3, select_state='Active')

        STC.stopTraffic('port1,port2')
        ID1TX = STC.streamResultView('port1', '1', 'txFrameCountStream')
        ID1RX = STC.streamResultView('port1', '1', 'rxFrameCountStream')
        ID2TX = STC.streamResultView('port2', '1', 'txFrameCountStream')
        ID2RX = STC.streamResultView('port2', '1', 'rxFrameCountStream')
        Stream_Check_Count(ID1TX, ID1RX)
        Stream_Check_Count(ID2TX, ID2RX)

        # 6、操作：逐个断开Lag组通道；检查：以太网业务丢包、LSP1:1保护、Lag保护状态、告警、性能
        print("SPN_4358_test 6.1测试步骤开始")
        STC.clearResults('port1,port2')
        STC.startTraffic('port1,port2', '5')

        nc_info = [None, None, None, None, Local.SW4_SW3_2, 'ETH-PHY', 'disable']
        nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled']
        cmd_list_temp[0] = creatConfig(nc_info, nc_yang)
        multi_edit_conf([dut4], [cmd_list_temp])
        time.sleep(3)

        nc_info_get = [None, None, None, None, None]
        nc_yang_get = ['fos-mpls-oper', 'mpls-oper', 'tunnel-protect-groups', 'tunnel-bundle-protect-groups', 'tunnel-bundle-protect-group']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='1', switch_state='normal', primary_lsp_state='normal', secondary_lsp_state='normal')

        nc_info_get = [None, None, None, None]
        nc_yang_get = ['fos-ethif-lag-oper', 'ethlagif-oper', 'ethlagif-states', 'ethlagif-state']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_lag_staus(rpc_info=status_result, lag_name='lag1', state='up', lag_mode='lacp-load', load_balance='mac')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_2, select_state='Deactive')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_3, select_state='Active')

        STC.stopTraffic('port1,port2')
        ID1TX = STC.streamResultView('port1', '1', 'txFrameCountStream')
        ID1RX = STC.streamResultView('port1', '1', 'rxFrameCountStream')
        ID2TX = STC.streamResultView('port2', '1', 'txFrameCountStream')
        ID2RX = STC.streamResultView('port2', '1', 'rxFrameCountStream')
        Stream_Check_DropCount(ID1TX, ID1RX, 10000.0, SPN_4358_LAG_dropTime)
        Stream_Check_DropCount(ID2TX, ID2RX, 10000.0, SPN_4358_LAG_dropTime)

        # 7、操作：逐个恢复Lag组通道；检查：以太网业务丢包、LSP1:1保护、Lag保护状态、告警、性能
        print("SPN_4358_test 7.1测试步骤开始")
        STC.clearResults('port1,port2')
        STC.startTraffic('port1,port2', '5')

        nc_info = [None, None, None, None, Local.SW4_SW3_2, 'ETH-PHY', 'enable']
        nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled']
        cmd_list_temp[0] = creatConfig(nc_info, nc_yang)
        multi_edit_conf([dut4], [cmd_list_temp])
        time.sleep(10)

        nc_info_get = [None, None, None, None, None]
        nc_yang_get = ['fos-mpls-oper', 'mpls-oper', 'tunnel-protect-groups', 'tunnel-bundle-protect-groups', 'tunnel-bundle-protect-group']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='1', switch_state='normal', primary_lsp_state='normal', secondary_lsp_state='normal')

        nc_info_get = [None, None, None, None]
        nc_yang_get = ['fos-ethif-lag-oper', 'ethlagif-oper', 'ethlagif-states', 'ethlagif-state']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_lag_staus(rpc_info=status_result, lag_name='lag1', state='up', lag_mode='lacp-load', load_balance='mac')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_2, select_state='Active')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_3, select_state='Active')

        STC.stopTraffic('port1,port2')
        ID1TX = STC.streamResultView('port1', '1', 'txFrameCountStream')
        ID1RX = STC.streamResultView('port1', '1', 'rxFrameCountStream')
        ID2TX = STC.streamResultView('port2', '1', 'txFrameCountStream')
        ID2RX = STC.streamResultView('port2', '1', 'rxFrameCountStream')
        Stream_Check_DropCount(ID1TX, ID1RX, 10000.0, SPN_4358_LAG_dropTime)
        Stream_Check_DropCount(ID2TX, ID2RX, 10000.0, SPN_4358_LAG_dropTime)

        # 8、操作：多个站点掉电重启；检查：以太网业务恢复、LSP1:1保护、Lag保护状态、告警、性能
        print("SPN_4358_test 8.1测试步骤开始")
        # 9、操作：时钟交叉盘切换；检查：以太网业务丢包、LSP1:1保护、Lag保护状态、告警、性能
        print("SPN_4358_test 9.1测试步骤开始")

        # 10、操作：保护正常状态下，增删业务；检查：原有业务是否正常
        print("SPN_4358_test 10.1测试步骤开始")
        STC.clearResults('port1,port2')
        STC.startTraffic('port1,port2', '5')

        cmd_list1_temp, cmd_list2_temp, cmd_list3_temp, cmd_list4_temp = xmlConfig_temp()
        cmd_del_temp = multi_edit_conf([dut1, dut2, dut3, dut4], [cmd_list1_temp, cmd_list2_temp, cmd_list3_temp, cmd_list4_temp])

        nc_info_get = [None, None, None, None, None]
        nc_yang_get = ['fos-mpls-oper', 'mpls-oper', 'tunnel-protect-groups', 'tunnel-bundle-protect-groups', 'tunnel-bundle-protect-group']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='1', switch_state='normal', primary_lsp_state='normal', secondary_lsp_state='normal')
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='2', switch_state='normal', primary_lsp_state='normal', secondary_lsp_state='normal')

        nc_info_get = [None, None, None, None]
        nc_yang_get = ['fos-ethif-lag-oper', 'ethlagif-oper', 'ethlagif-states', 'ethlagif-state']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_lag_staus(rpc_info=status_result, lag_name='lag1', state='up', lag_mode='lacp-load', load_balance='mac')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_2, select_state='Active')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_3, select_state='Active')

        cmd_list1_temp, cmd_list2_temp, cmd_list3_temp, cmd_list4_temp = xmlConfig_temp_del()
        cmd_del_temp = multi_edit_conf([dut1, dut2, dut3, dut4], [cmd_list1_temp, cmd_list2_temp, cmd_list3_temp, cmd_list4_temp])

        nc_info_get = [None, None, None, None, None]
        nc_yang_get = ['fos-mpls-oper', 'mpls-oper', 'tunnel-protect-groups', 'tunnel-bundle-protect-groups', 'tunnel-bundle-protect-group']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='1', switch_state='normal', primary_lsp_state='normal', secondary_lsp_state='normal')

        nc_info_get = [None, None, None, None]
        nc_yang_get = ['fos-ethif-lag-oper', 'ethlagif-oper', 'ethlagif-states', 'ethlagif-state']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_lag_staus(rpc_info=status_result, lag_name='lag1', state='up', lag_mode='lacp-load', load_balance='mac')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_2, select_state='Active')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_3, select_state='Active')

        STC.stopTraffic('port1,port2')
        ID1TX = STC.streamResultView('port1', '1', 'txFrameCountStream')
        ID1RX = STC.streamResultView('port1', '1', 'rxFrameCountStream')
        ID2TX = STC.streamResultView('port2', '1', 'txFrameCountStream')
        ID2RX = STC.streamResultView('port2', '1', 'rxFrameCountStream')
        Stream_Check_Count(ID1TX, ID1RX)
        Stream_Check_Count(ID2TX, ID2RX)

        # 11、操作：保护倒换状态下，增删业务；检查：原有业务是否正常
        print("SPN_4358_test 11.1测试步骤开始")
        nc_info = [None, None, None, None, Local.SW1_SW4_1, 'FLEXE-PHY', 'disable']
        nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled']
        cmd_list_temp[0] = creatConfig(nc_info, nc_yang)
        multi_edit_conf([dut1], [cmd_list_temp])
        time.sleep(3)

        nc_info = [None, None, None, None, Local.SW4_SW3_2, 'ETH-PHY', 'disable']
        nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled']
        cmd_list_temp[0] = creatConfig(nc_info, nc_yang)
        multi_edit_conf([dut4], [cmd_list_temp])
        time.sleep(3)

        STC.clearResults('port1,port2')
        STC.startTraffic('port1,port2', '5')

        cmd_list1_temp, cmd_list2_temp, cmd_list3_temp, cmd_list4_temp = xmlConfig_temp()
        cmd_del_temp = multi_edit_conf([dut1, dut2, dut3, dut4], [cmd_list1_temp, cmd_list2_temp, cmd_list3_temp, cmd_list4_temp])

        nc_info_get = [None, None, None, None, None]
        nc_yang_get = ['fos-mpls-oper', 'mpls-oper', 'tunnel-protect-groups', 'tunnel-bundle-protect-groups', 'tunnel-bundle-protect-group']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='1', switch_state='switch', primary_lsp_state='sf', secondary_lsp_state='normal')
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='2', switch_state='switch', primary_lsp_state='sf', secondary_lsp_state='normal')

        nc_info_get = [None, None, None, None]
        nc_yang_get = ['fos-ethif-lag-oper', 'ethlagif-oper', 'ethlagif-states', 'ethlagif-state']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_lag_staus(rpc_info=status_result, lag_name='lag1', state='up', lag_mode='lacp-load', load_balance='mac')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_2, select_state='Deactive')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_3, select_state='Active')

        cmd_list1_temp, cmd_list2_temp, cmd_list3_temp, cmd_list4_temp = xmlConfig_temp_del()
        cmd_del_temp = multi_edit_conf([dut1, dut2, dut3, dut4], [cmd_list1_temp, cmd_list2_temp, cmd_list3_temp, cmd_list4_temp])

        nc_info_get = [None, None, None, None, None]
        nc_yang_get = ['fos-mpls-oper', 'mpls-oper', 'tunnel-protect-groups', 'tunnel-bundle-protect-groups', 'tunnel-bundle-protect-group']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_tunnel_bundle_protect_groups(rpc_info=status_result, tunnel_bundle_id='1', switch_state='switch', primary_lsp_state='sf', secondary_lsp_state='normal')

        nc_info_get = [None, None, None, None]
        nc_yang_get = ['fos-ethif-lag-oper', 'ethlagif-oper', 'ethlagif-states', 'ethlagif-state']
        status_result = get_spn_status(dut4, showConfig(nc_info_get, nc_yang_get))
        check_lag_staus(rpc_info=status_result, lag_name='lag1', state='up', lag_mode='lacp-load', load_balance='mac')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_2, select_state='Deactive')
        check_lag_member_status(rpc_info=status_result, lag_member_name=Local.SW4_SW3_3, select_state='Active')

        STC.stopTraffic('port1,port2')
        ID1TX = STC.streamResultView('port1', '1', 'txFrameCountStream')
        ID1RX = STC.streamResultView('port1', '1', 'rxFrameCountStream')
        ID2TX = STC.streamResultView('port2', '1', 'txFrameCountStream')
        ID2RX = STC.streamResultView('port2', '1', 'rxFrameCountStream')
        Stream_Check_Count(ID1TX, ID1RX)
        Stream_Check_Count(ID2TX, ID2RX)

        nc_info = [None, None, None, None, Local.SW1_SW4_1, 'FLEXE-PHY', 'enable']
        nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled']
        cmd_list_temp[0] = creatConfig(nc_info, nc_yang)
        multi_edit_conf([dut1], [cmd_list_temp])
        time.sleep(3)

        nc_info = [None, None, None, None, Local.SW4_SW3_2, 'ETH-PHY', 'enable']
        nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled']
        cmd_list_temp[0] = creatConfig(nc_info, nc_yang)
        multi_edit_conf([dut4], [cmd_list_temp])
        time.sleep(10)

        # 仪表端口释放
        STC.port_release(portUsed)

        print("SPN_4358_test用例测试通过")
        SPN_4358_flag = True
    except Exception as ex:
        print(ex)
        print("SPN_4358_test用例测试失败")
        SPN_4358_flag = False
    finally:
        # 删除全部配置
        print("SPN_4358_test删除配置开始")
        multi_edit_conf([dut1, dut2, dut3, dut4], cmd_del)
        print("SPN_4358_test删除配置结束")
        return SPN_4358_flag


if __name__ == '__main__':
    SPN_4358_test()