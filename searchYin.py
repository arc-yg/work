
import os,sys
from lxml import etree
# from ncclient import xml_
# from .parseYinFile import *

class tree_module:
	def __init__(self, tree):
		root = tree.getroot()
		xmlnsName = root.tag.split("}")[0] + "}"

		self.tree = tree
		self.root = root

		self.moduleName = root.get("name")
		self.xmlnsName = root.tag.split("}")[0] + "}"
		self.prefixName = (root.find("./"+xmlnsName+"prefix")).get("value")
		self.namespace = (root.find("./"+xmlnsName+"namespace")).get("uri")

		self.grouping_list = root.findall("./"+xmlnsName+"grouping")
		self.augment_list = root.findall("./"+xmlnsName+"augment")
		self.import_list = root.findall("./"+xmlnsName+"import")

class tree_submodule:
	def __init__(self, tree):
		root = tree.getroot()
		xmlnsName = root.tag.split("}")[0] + "}"

		self.tree = tree
		self.root = root

		self.moduleName = root.get("name")
		self.xmlnsName = root.tag.split("}")[0] + "}"
		self.belongsToName = (root.find("./"+xmlnsName+"belongs-to")).get("module")

		self.grouping_list = root.findall("./"+xmlnsName+"grouping")
		self.augment_list = root.findall("./"+xmlnsName+"augment")
		self.import_list = root.findall("./"+xmlnsName+"import")


tree_list = []
tree_list_sub = []
main_tree_module = None
def init_yin():
	# cwd = os.getcwd()
	# sys.path.append(cwd)
	dirPath = os.path.join(os.path.dirname(__file__), 'yin')
	dirList = os.listdir(dirPath)

	global tree_list, tree_list_sub

	for file in dirList:
		tempFile = dirPath + "\\" + file
		tree = etree.ElementTree(file=tempFile)
		root = tree.getroot()
		moduleType = root.tag.split("}")[1]

		if moduleType == "module":
			tree_module1 = tree_module(tree)
			tree_list.append(tree_module1)
		elif moduleType == "submodule":
			tree_module2 = tree_submodule(tree)
			tree_list_sub.append(tree_module2)
		else:
			raise Exception('module name error!')


def search_yin(nc_info, nc_yang):
	global tree_list, tree_list_sub, main_tree_module

	if len(nc_info) != len(nc_yang):
		raise Exception("lenth is not same.")
		return None

	for i in tree_list:
		if i.moduleName == nc_yang[0]:
			root = i.root
			tree_module1 = i
			break
	main_tree_module = tree_module1

	str_tab = '\t'
	search_depth = 0
	depth = 0

	xml_str = str_tab*depth + "<config xmlns=\"urn:ietf:params:xml:ns:netconf:base:1.0\">\n"
	search_depth += 1
	depth += 1
	search_depth, depth, xml_str = search_internal(root, nc_info, nc_yang, search_depth, root, depth, xml_str)
	depth -= 1
	xml_str += str_tab*depth + "</config>\n"

	xml_str = xml_str.replace("<{}>".format(tree_module1.prefixName), "<{} xmlns=\"{}\">".format(tree_module1.prefixName, tree_module1.namespace), 1)

	print(search_depth, depth, len(nc_yang))
	if depth != 0:
		raise Exception("depth error.")
		return None
	return xml_str


def search_internal(root, search_info, search_yang, search_depth ,node, depth, xml_str):
	# str_tab = '\t'
	str_tab = '    '
	if search_depth == len(search_yang):
		return search_depth, depth, xml_str

	# print(root.get("name"), node.tag.split("}")[1], sorted(node.items()) )
	# print("\t", search_yang[search_depth:])

	xmlnsName = node.tag.split("}")[0] + "}"

	containerNode = node.find("./"+xmlnsName+"container[@name='{}']".format(search_yang[search_depth]))
	if containerNode != None:
		xml_str += (str_tab*(depth) + '<' + search_yang[search_depth] + '>' + '\n')
		search_depthT = search_depth
		search_depth += 1
		depth += 1
		search_depth, depth, xml_str = search_internal(root, search_info, search_yang, search_depth, containerNode, depth, xml_str)
		depth -= 1
		xml_str += (str_tab*(depth) + '</' + search_yang[search_depthT] + '>' + '\n')
		if search_depth != len(search_yang):
			search_depth, depth, xml_str = search_internal(root, search_info, search_yang, search_depth, node, depth, xml_str)
		return search_depth, depth, xml_str

	listNode = node.find("./"+xmlnsName+"list[@name='{}']".format(search_yang[search_depth]))
	if listNode != None:
		xml_str += (str_tab*(depth) + '<' + search_yang[search_depth] + '>' + '\n')
		search_depthT = search_depth
		search_depth += 1
		depth += 1
		search_depth, depth, xml_str = search_internal(root, search_info, search_yang, search_depth, listNode, depth, xml_str)
		depth -= 1
		xml_str += (str_tab*(depth) + '</' + search_yang[search_depthT] + '>' + '\n')
		if search_depth != len(search_yang):
			search_depth, depth, xml_str = search_internal(root, search_info, search_yang, search_depth, node, depth, xml_str)
		return search_depth, depth, xml_str

	leafNode = node.find("./"+xmlnsName+"leaf[@name='{}']".format(search_yang[search_depth]))
	if leafNode != None:
		if search_info[search_depth] != None:
			xml_str += (str_tab*(depth) + '<' + search_yang[search_depth] + '>' + search_info[search_depth])
			xml_str += ('</' + search_yang[search_depth] + '>' + '\n')
		else:
			xml_str += (str_tab*(depth) + '<' + search_yang[search_depth] + '>')
			xml_str += ('</' + search_yang[search_depth] + '>' + '\n')
		search_depth += 1
		search_depth, depth, xml_str = search_internal(root, search_info, search_yang, search_depth, node, depth, xml_str)
		return search_depth, depth, xml_str

	submoduleList = node.findall("./"+xmlnsName+"include")
	for i in submoduleList:
		for j in tree_list_sub:
			if j.moduleName == i.get("module"):
				root2 = j.root
				break
		search_depth2, depth2, xml_str2 = search_internal(root2, search_info, search_yang, search_depth, root2, depth, xml_str)
		if(xml_str2 != xml_str):
			if search_depth != len(search_yang):
				search_depth2, depth2, xml_str2 = search_internal(root, search_info, search_yang, search_depth2, node, depth2, xml_str2)
			return search_depth2, depth2, xml_str2


	usesList = node.findall("./"+xmlnsName+"uses")
	for i in usesList:
		name = i.get("name")
		name1 = name.split(":")[0]
		if name1 == name:
			groupingNode = root.find("./"+xmlnsName+"grouping[@name='{}']".format(name1))
			search_depth2, depth2, xml_str2 = search_internal(root, search_info, search_yang, search_depth, groupingNode, depth, xml_str)
			if(xml_str2 != xml_str):
				if search_depth != len(search_yang):
					search_depth2, depth2, xml_str2 = search_internal(root, search_info, search_yang, search_depth2, node, depth2, xml_str2)
				return search_depth2, depth2, xml_str2
		else:
			name2 = name.split(":")[1]
			for i in tree_list:
				if i.prefixName == name1:
					root2 = i.root
					break
			groupingNode2 = root2.find("./"+xmlnsName+"grouping[@name='{}']".format(name2))
			search_depth2, depth2, xml_str2 = search_internal(root2, search_info, search_yang, search_depth, groupingNode2, depth, xml_str)
			if(xml_str2 != xml_str):
				xml_str2 = add_namespace(root, xml_str, root2, xml_str2)
				if search_depth != len(search_yang):
					search_depth2, depth2, xml_str2 = search_internal(root, search_info, search_yang, search_depth2, node, depth2, xml_str2)
				return search_depth2, depth2, xml_str2

	prefixName = (root.find("./"+xmlnsName+"prefix")).get("value")
	# print(root.get("name"), prefixName)
	attr = sorted(node.keys())[0]
	# print(node.tag, attr )
	nameT = node.get(attr)
	# print(nameT)
	flag = False
	for i in tree_list:
		for j in i.augment_list:
			targetPath = j.get("target-node")
			str_temp = targetPath.split(":")
			name_temp = str_temp[-1]
			prefixNameT = str_temp[0].split("/")[1]
			if prefixName == prefixNameT and nameT == name_temp:
				root2 = i.root
				augmentNode2 = j
				# print( root2.get("name"), augmentNode2.get("target-node"),"**********")
				search_depth2, depth2, xml_str2 = search_internal(root2, search_info, search_yang, search_depth, augmentNode2, depth, xml_str)
				if(xml_str2 != xml_str):
					flag = True
					# print("********")
					# print(xml_str, search_depth, "\n", xml_str2, search_depth2)
					# print("********")
					xml_str2 = add_namespace(root, xml_str, root2, xml_str2)
					if search_depth != len(search_yang):
						search_depth2, depth2, xml_str2 = search_internal(root, search_info, search_yang, search_depth2, node, depth2, xml_str2)
					return search_depth2, depth2, xml_str2

	return search_depth, depth, xml_str

# import re
def add_namespace(root, xml_str, root2, xml_str2):#namespace后处理，也可以添加search_shift（类似search_internal）来处理，交叉递归


	xmlnsName = root.tag.split("}")[0] + "}"
	namespace = (root.find("./"+xmlnsName+"namespace")).get("uri")
	xmlnsName2 = root2.tag.split("}")[0] + "}"
	namespace2 = (root2.find("./"+xmlnsName2+"namespace")).get("uri")
	if namespace == namespace2:#检查module文件假跳转
		return xml_str2

	if main_tree_module.namespace != namespace:#只添加外层namespace
		return xml_str2

	xml_diff = xml_str2.split(xml_str)[1]
	# xml_diff.replace(">", " xmlns=\"{}\">".format(namespace2), 1)
	# xml_str2 = xml_str+xml_diff

	str_temp = '\n'
	str_temp += xml_diff[:(xml_diff.find("<"))+1]
	str_list = xml_diff.split(str_temp)
	# print(str_temp, str_list)
	for i in range(0, len(str_list)):
		if str_list[i][0] != "/":
			str_list[i] = str_list[i].replace(">", " xmlns=\"{}\">".format(namespace2), 1)
	xml_str2 = xml_str + str_list[0]
	for i in range(1, len(str_list)):
		xml_str2 += str_temp + str_list[i]

	return xml_str2

def creatConfig(nc_info, nc_yang):
	return search_yin(nc_info, nc_yang)

if __name__ == "__main__":
	init_yin()
	nc_info = [None, None, None, None, 'eth-10gi0/9/0/3.20', 'ETH-SUBIF', None, 'enable', None, 'disable', 'layer-2-switch', None, 'dot1q', None, '20']
	nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'description', 'enabled', 'eth-option', 'loop-block', 'transport-layer', 'if-vlan-cfg', 'termination_type', 'vlan-sub-cfg', 'svlan_min']
	print(creatConfig(nc_info, nc_yang))

	nc_info = [None, None, None, None, '_public_', '13.1.1.1', '80:3A:F4:27:E7:00', 'none']
	nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type']
	print(creatConfig(nc_info, nc_yang))
	nc_info = [None, None, None, None, 'flexe-client1/2', 'FLEXE-CLIENT', None]
	nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexe-oam']
	print(creatConfig(nc_info, nc_yang))
	nc_info = [None, None, None, None, 'loopback0', 'LOOPBACK', 'enable', None, None, None, '216.1.1.3/32', 'mast']
	nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'loopback-interface', 'ip', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
	print(creatConfig(nc_info, nc_yang))
	nc_info = [None, None, None, None, 'flexe-tunnel3', 'FLEXE-TUNNEL', None, 'layer-2-switch', None, '1500']
	nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexevethif-interface', 'transport-layer', 'ip', 'ipv4-mtu']
	print(creatConfig(nc_info, nc_yang))
	nc_info = [None, None, None, None, 'flexe-tunnel3', 'FLEXE-TUNNEL', None, 'flexe-client1/2']
	nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'flexetunnel-ctrlinterface', 'protect-flexe-client']
	print(creatConfig(nc_info, nc_yang))
	nc_info = [None, None, None, None, "eth-10gi0/4/0/2", 'ETH-PHY', 'enable', None, 'disable', None, '200', '0', 'disable', 'lan', '0', 'layer-3-route', None, '1500', None, '24.1.1.2/24', 'mast']
	nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'enabled', 'eth-option', 'loop-block', 'ethphy-interface', 'up-holdtime', 'down-holdtime', 'tp-mode-enable', 'port-mode', 'port-laser-startup-delay-time', 'transport-layer', 'ip', 'ipv4-mtu', 'ipv4-address-list', 'ipv4-address', 'secondry-use']
	print(creatConfig(nc_info, nc_yang))
	nc_info = [None, None, None, None, 'l3vpn_96', None, 'ipv4', '160:1', 'per_vrf', None, 'import', '160:1', None, 'export', '160:1', 'l3vpn-tnl-plcy-96', 'Ipv4RouteMap_65758', None, 'ipv6', '165:1', 'per_vrf', None, 'import', '165:1', None, 'export', '165:1', 'l3vpn-tnl-plcy-96', 'Ipv6RouteMap_65758', None, 'ipv4', '160', None, 'ipv6', '165']
	nc_yang = ['fos-l3vpn', 'l3vpn', 'vpn-instances', 'vpn-instance', 'vpn-instance-name', 'vpnInst', 'af-mode', 'route-distinguisher', 'apply-label-mode', 'route-target', 'route-target-type', 'route-target-value', 'route-target', 'route-target-type', 'route-target-value', 'tunnel-policy', 'vpn-frr-route-policy', 'vpnInst', 'af-mode', 
	'route-distinguisher', 'apply-label-mode', 'route-target', 'route-target-type', 'route-target-value', 'route-target', 'route-target-type', 'route-target-value', 'tunnel-policy', 'vpn-frr-route-policy', 'static-l3vpn', 'af-mode', 'static-local-label', 'static-l3vpn', 'af-mode', 'static-local-label']
	print(creatConfig(nc_info, nc_yang))