
from ncclient import manager
# from ncclient.xml_ import to_ele
import re

import Global
from spn_yang_library import *


# 回退配置eth-phy的参数，具体操作是能删除就删除，不能删除就配默认值
def eth_phy_cleanup(con_info):
	# 可删除的值
	rep_list = ['ethphy-interface', 'ipv4-address-list', 'ipv6-enable', 'linklocal-config', 'ipv6-address-list', 'bandwidth', 'loop-block']
	for i in rep_list:
		con_info = re.sub(r'(<{}[^>]*)>'.format(i), r'\1 operation="remove">', con_info)
	# 无法删除的值，配置默认值
	re_lists = {'description': None, 'ipv4-mtu': '1500', 'ipv6-mtu': '1500', 'transport-layer': 'layer-3-route'}
	for k, v in re_lists.items():
		res = '<{}/>'.format(k) if v is None else '<{}>{}</{}>'.format(k, v, k)
		con_info = re.sub(r'<{}>.*?</{}>'.format(k, k), res, con_info)
	return con_info

def del_config(cmd_list):
	cmd_list_del = []
	for i in range(len(cmd_list)):
		if 'operation="remove"' in cmd_list[i]:
			continue
		else:
			if '<type>FLEXE-PHY</type>' in cmd_list[i]:
				# flexe phy不做处理
				pass
			elif '<type>ETH-PHY</type>' in cmd_list[i]:
				# 以太phy无法删除接口，特殊处理
				cmd_list_del.append(eth_phy_cleanup(cmd_list[i]))
			else:
				# 查找到'</'时，在上一行添加remove，即删除root
				str_conf = cmd_list[i]
				conf_ele = re.findall(r'(<.+>)\n', str_conf)
				for i in range(len(conf_ele)):
					# print("conf_ele {}: {}".format(i, conf_ele[i]))
					if '</' in conf_ele[i]:
						conf_remove = str_conf.replace(conf_ele[i-1], conf_ele[i-1][:-1]+' operation="remove">')
						# print("conf_remove {}: {}".format(i, conf_remove))
						cmd_list_del.append(conf_remove)
						break
	return cmd_list_del[::-1]

def nc_edit_config(dut, cmd_list):
	commit_flag = False
	force_del_flag = False
	with manager.connect(host=dut['netconf_ip'], port=dut['netconf_port_num'], username=dut['netconf_username'], password=dut['netconf_password'], 
		hostkey_verify=False, allow_agent=False, look_for_keys=False) as dut_connect:
		print("The session id is {}.".format(dut_connect._session.id))
		print("设备{} 配置开始：".format(dut['netconf_ip']))
		for i in range(len(cmd_list)):
			# print("cmd_list %d is:\n%s" % (i, cmd_list[i]))
			try:
				rpc_conf = dut_connect.edit_config(target='candidate', config=cmd_list[i])#配置下发、预存
				# print("RPCReply for cmd_list %d is:\n%s" % (i, rpc_conf.xml))
				xml_str = rpc_conf.xml
				if "<ok/>" in xml_str or "successful" in xml_str:
					print("设备%s 端口%s cmd_list %d 返回成功" % (dut['netconf_ip'], dut['netconf_port_num'], i))
				else:
					raise Exception("设备%s 端口%s cmd_list %d 返回失败" % (dut['netconf_ip'], dut['netconf_port_num'], i))
				# dut_connect.commit(confirmed=True, timeout='300')
			except Exception as ex:
				# dut_connect.commit(confirmed=True, timeout='300')
				print("cmd_list %d is:\n%s" % (i, cmd_list[i]))
				if 'operation="remove"' in cmd_list[i]:	   #强行下发删除，其他情况直接返回
					print("设备%s 端口%s cmd_list %d 删除失败  " % (dut['netconf_ip'], dut['netconf_port_num'], i), ex)
					force_del_flag = True
					continue
				else:
					print("设备%s 端口%s cmd_list %d 配置失败  " % (dut['netconf_ip'], dut['netconf_port_num'], i), ex)
					return commit_flag,force_del_flag
		dut_connect.commit(confirmed=True, timeout='300')#缓存配置执行、生效
		commit_flag = True
		print("设备%s 配置结束。" % (dut['netconf_ip']))
		return commit_flag,force_del_flag

def multi_edit_conf(dut_list, cmd_list, cmd_delete_before=None):
	if len(dut_list) != len(cmd_list)
		raise Exception("dut_list cmd_list length is not same!")

	for i in range(len(dut_list)):
		if len(cmd_list[i]) != 0:
			commit_flag,force_del_flag = nc_edit_config(dut_list[i], cmd_list[i])

def XML_config():
	initialFunction()
	dut1, dut2, dut3, dut4 = Global.SW1, Global.SW2, Global.SW3, Global.SW4
	xml_list1, xml_list2, xml_list3, xml_list4 = [], [], [], []

	nc_info = [None, None, None, '216.1.1.4']
	nc_yang = ['fos-mpls', 'mpls', 'mpls-te', 'router-id']
	xml_list3.append(creatConfig(nc_info, nc_yang))

	nc_info = [None, None, None, None, 'loopback0', 'LOOPBACK', 'enable', None, None, None, '216.1.1.4/32', 'mast']
	nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'loopback-interface', 'ip', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
	xml_list3.append(creatConfig(nc_info, nc_yang))

	# nc_info = [None, None, None, None, Global.SW3_SW2_1.split('gi')[1], 'disable']
	# nc_yang = ['fos-device', 'device', 'ethmode-cfgs', 'ethmode-cfg', 'if-name', 'enable']
	# xml_list3.append(creatConfig(nc_info, nc_yang))

	# nc_info = [None, None, None, None, Global.SW3_SW2_1, 'FLEXE-PHY', 'enable', None, '0', 'auto', '0']
	# nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'flexe-ctrlinterface', 'unavailable-timeslot-count', 'fec-mode', 'port-laser-startup-delay-time']
	# xml_list3.append(creatConfig(nc_info, nc_yang))

	# nc_info = [None, None, None, None, Global.SW3_port3, 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500']
	# nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu']
	# xml_list3.append(creatConfig(nc_info, nc_yang))


	nc_info = [None, None, None, None, '_public_', '34.1.1.4', '48:F9:7C:E2:F1:A7', 'none']
	nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type']
	xml_list3.append(creatConfig(nc_info, nc_yang))



	print("AAAAAAAAAAAAAAAAAAAAA")
	commit_flag,force_del_flag = nc_edit_config(dut4, xml_list3)
	print("commit_flag: {}, force_del_flag: {}".format(commit_flag,force_del_flag))
	print("BBBBBBBBBBBBBBBBBBBBB")

	# for i in range(len(cmd_list_del)):
		# print("cmd_list_del {}: {}".format(i, cmd_list_del[i]))
	print("CCCCCCCCCCCCCCCCCCCCC")
	# str_tt = input("请输入：")
	# print("你的输入是：", str_tt)
	# cmd_list3_del = del_config(xml_list3)
	# commit_flag,force_del_flag = nc_edit_config(dut4, cmd_list3_del)
	# print("commit_flag: {}, force_del_flag: {}".format(commit_flag,force_del_flag))
	print("DDDDDDDDDDDDDDDDDDDDD")
	return xml_list1, xml_list2, xml_list3, xml_list4


if __name__ == '__main__':
	XML_config()

"""<config>
  <if xmlns="http://fiberhome.com/fhnw/yang/interface/fos-interface-common">
	<interfaces>
	  <interface operation="remove">
		<name>loopback0</name>
		<type>LOOPBACK</type>
	  </interface>
	</interfaces>
  </if>
</config>"""