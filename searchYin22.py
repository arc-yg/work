
import os,sys
from lxml import etree

# class treeNode22:
	# def __init__(self,tree)
		# id = 0
		# parent_id = 0 
		# child_id_list = []
		# type = ""
		# value = ""
		# namespace = ""
		# depth = 0
		# store_id = 0

class yinNode:
	def __init__(self, type, value, namespace, depth, parent, child_list):
		self.type = type
		self.value = value
		self.namespace = namespace
		self.depth = depth
		self.parent = parent
		self.child_list = child_list

tree_list = []
tree_list_sub = []
yin_list = []
def init_yin():
	global tree_list, tree_list_sub, yin_list
	# cwd = os.getcwd()
	# sys.path.append(cwd)
	dirPath = os.path.join(os.path.dirname(__file__), 'yin')
	dirList = os.listdir(dirPath)

	tree_list = []
	tree_list_sub = []
	for file in dirList:
		tempFile = dirPath + "\\" + file
		# if os.path.isfile(tempFile):
		tree = etree.ElementTree(file=tempFile)
		root = tree.getroot()
		moduleType = root.tag.split("}")[1]
		if moduleType == "module":
			tree_list.append(tree)
		elif moduleType == "submodule":
			tree_list_sub.append(tree)

	# root = tree_list_sub[0].getroot()
	# xmlnsName = root.tag.split("}")[0] + "}"
	# result1 = root.find("./" + xmlnsName + "importwww")
	# result2 = root.findall("./" + xmlnsName + "importwww")
	# print(type(result1), result1)
	# print(type(result2), result2)
	# node = root.find("./" + xmlnsName + "augment")
	# for child in node:
		# print("11", child.tag)
	# for child in node.iter():
		# print("22", child.tag)

	yin_list = []
	for tree in tree_list:
		yinNode1 = tree_convert(tree, tree_list)
		yin_list.append(yinNode1)

	for tree in tree_list:    #augment单独延后处理
		root = tree.getroot()
		xmlnsName = root.tag.split("}")[0] + "}"
		augmentNodeList = root.findall("./"+xmlnsName+"augment")
		for node in augmentNodeList:
			deal_augmentNode(root, node)
			
	for tree in tree_list_sub:    #augment单独延后处理
		root = tree.getroot()
		xmlnsName = root.tag.split("}")[0] + "}"
		augmentNodeList = root.findall("./"+xmlnsName+"augment")
		belongstoNode = root.find("./"+xmlnsName+"belongs-to")
		belongstoName = belongstoNode.get("module")
		for i in tree_list:
			root2 = i.getroot()
			if root2.get("name") == belongstoName:
				for node in augmentNodeList:
					deal_augmentNode(root2, node)

def deal_augmentNode(root, augmentNode):
	augmentPath = augmentNode.get("target-node")
	prifix, path_list = deal_augmentPath(augmentPath)

	flag1 = False
	for tree in tree_list:
		root2 = tree.getroot()
		xmlnsName2 = root2.tag.split("}")[0] + "}"
		prefixNode2 = root2.find("./"+xmlnsName2+"prefix")
		prefixName2 = prefixNode2.get("value")
		if prefixName2 == prifix:
			moduleName2 = root2.get("name")
			flag1 = True
			break
	flag2 = False
	if flag1 == True:
		for i in yin_list:
			if i.value == moduleName2:
				yinRoot = i
				flag2 = True
				break
	
	if flag2 == True:
		# insert_augmentNode(root, augmentNode, path_list, yinRoot)
		startNode = yinRoot
		for i in range(len(path_list)):
			child_list = startNode.child_list
			for j in range(len(child_list)):
				if path_list[i] == child_list[j].value:
					startNode = child_list[j]
					break
				elif j == (len(child_list)-1):
					raise Exception("augmentPath not found")
		child_list1 = search_child(root, tree_list, augmentNode, startNode.depth)
		
		xmlnsName = root.tag.split("}")[0] + "}"
		namespaceNode = root.find("./"+xmlnsName+"namespace")
		namespace = namespaceNode.get("uri")
		for k in child_list1:
			k.namespace = namespace
		
		startNode.child_list += child_list1
	else:
		if prifix not in ["nc"]:
			raise Exception("augment target-node not found {} {}".format(root.get("name"), augmentPath))


def deal_augmentPath(augmentPath):
	list1 = augmentPath.split("/")
	list2 = list1[1:]
	list3 = []
	prifix = list2[0].split(":")[0]
	for i in list2:
		str1 = i.split(":")[0]
		str2 = i.split(":")[1]
		list3.append(str2)
		if str1 != prifix:
			if prifix != "bd":
				raise Exception("augmentPath prifix is not same! {}".format(augmentPath))
	return prifix, list3


def tree_convert(tree, tree_list):
	root = tree.getroot()

	type = root.tag.split("}")[1]
	value = root.get("name")
	namespace = None
	depth = 0
	parent = None
	child_list = search_child(root, tree_list, root, depth)

	xmlnsName = root.tag.split("}")[0] + "}"
	namespaceNode = root.find("./"+xmlnsName+"namespace")
	namespace = namespaceNode.get("uri")
	for k in child_list:
		k.namespace = namespace

	yinRoot = yinNode(type, value, namespace, depth, parent, child_list)
	return yinRoot

#root：node节点所在的module文件根节点，node节点所在的submodule对应的module文件根节点
def search_child(root, tree_list, node, depth):
	child_listP = []

	for child in node:
		type = child.tag.split("}")[1]

		if type == "container" or type == "list" or type == "leaf":
			value = child.get("name")
			namespace = None
			parent = node
			depthC = depth + 1
			child_listC = search_child(root, tree_list, child, depthC)

			yinNode1 = yinNode(type, value, namespace, depthC, node, child_listC)
			child_listP.append(yinNode1)

		elif type == "uses":
			# child_list = deal_uses(root, tree_list, child, depth)
			value = child.get("name")
			value1 = value.split(":")[0]
			if value1 == value:
				groupingName = value1
				child_list = deal_grouping(root, tree_list, groupingName, depth)
				if len(child_list) == 0:
					str_Exception = "module:{} grouping:{} not found or has no effect child!".format(root.get("name"), groupingName)
					raise Exception(str_Exception)
				child_listP += child_list
			else:
				value2 = value.split(":")[1]
				xmlnsName = root.tag.split("}")[0] + "}"
				prefixNode = root.find("./"+xmlnsName+"prefix")
				prefix = prefixNode.get("value")
				if value1 == prefix:
					groupingName = value2
					child_list = deal_grouping(root, tree_list, groupingName, depth)
					if len(child_list) == 0:
						str_Exception = "module:{} grouping:{} not found or has no effect child!".format(root.get("name"), groupingName)
						raise Exception(str_Exception)
					child_listP += child_list
				else:
					for tree in tree_list:
						root2 = tree.getroot()
						xmlnsName2 = root2.tag.split("}")[0] + "}"
						prefixNode2 = root2.find("./"+xmlnsName+"prefix")
						prefix2 = prefixNode2.get("value")
						if value1 == prefix2:
							groupingName = value2
							child_list = deal_grouping(root2, tree_list, groupingName, depth)
							if len(child_list) == 0:
								str_Exception = "module:{} grouping:{} not found or has no effect child!".format(root.get("name"), groupingName)
								raise Exception(str_Exception)
							child_listP += child_list
							break
		elif type == "include":
			includeName = child.get("module")
			for tree in tree_list_sub:
				root2 = tree.getroot()
				submoduleName = root2.get("name")
				if submoduleName == includeName:
					child_list = search_child(root, tree_list, root2, depth)
					# print(root.get("name"), root2.get("name"), child_list)
					child_listP += child_list
					break

	return child_listP

def deal_grouping(root, tree_list, groupingName, depth):
	child_list = []
	xmlnsName = root.tag.split("}")[0] + "}"
	groupingNode = root.find("./"+xmlnsName+"grouping[@name='{}']".format(groupingName))
	if groupingNode != None:
		child_list = search_child(root, tree_list, groupingNode, depth)
		return child_list
	else:
		includeNodeList = root.findall("./"+xmlnsName+"include")
		for includeNode in includeNodeList:
			includeName = includeNode.get("module")
			for tree in tree_list_sub:
				root2 = tree.getroot()
				submoduleName = root2.get("name")
				if submoduleName == includeName:
					groupingNode2 = root2.find("./"+xmlnsName+"grouping[@name='{}']".format(groupingName))
					if groupingNode2 != None:
						belongstoNode = root2.find("./"+xmlnsName+"belongs-to")
						belongstoName = belongstoNode.get("module")
						for i in tree_list:
							root3 = i.getroot()
							moduleName3 = root3.get("name")
							if moduleName3 == belongstoName:
								child_list = search_child(root3, tree_list, groupingNode2, depth)
								# for j in child_list:
									# print(j.type, j.value)
								return child_list
					else:
						break
	return child_list




def search_yin(nc_info, nc_yang):
	if len(nc_info) != len(nc_yang):
		raise Exception("lenth is not same.")
		return None
	
	str_tab = '\t'
	search_depth = 0
	depth = 0

	xml_str = str_tab*depth + "<config xmlns=\"urn:ietf:params:xml:ns:netconf:base:1.0\">\n"
	search_depth += 1
	depth += 1
	
	for i in yin_list:
		if i.value == nc_yang[0]:
			# print("%%%%%%%%%%%%%%",i.value, nc_yang[0])
			search_depth, depth, xml_str = search_internal(i, nc_info, nc_yang, search_depth, depth, xml_str)
			break

	depth -= 1
	xml_str += str_tab*depth + "</config>\n"

	print(search_depth, depth, len(nc_yang))
	if depth != 0:
		raise Exception("depth error.")
		return None
	return xml_str


def search_internal(yinNode1, search_info, search_yang, search_depth, depth, xml_str):

	if search_depth == len(search_yang):
		return search_depth, depth, xml_str

	# print("***********",search_depth)
	# print(xml_str,search_yang[search_depth:])
	# print("***********",search_depth)

	# if search_depth == 7:
		# print(yinNode1.type, yinNode1.value)

	str_tab = '    '
	startNode = yinNode1
	for i in startNode.child_list:
		if i.value == search_yang[search_depth]:
			if i.type == "container" or i.type == "list":
				if i.namespace == None:
					xml_str += str_tab*depth + "<" + i.value + ">\n"
				else:
					xml_str += str_tab*depth + "<" + i.value + " xmlns=\"" + i.namespace + "\">\n"
				search_depth += 1
				depth += 1
				search_depth, depth, xml_str = search_internal(i, search_info, search_yang, search_depth, depth, xml_str)
				depth -= 1
				xml_str += str_tab*depth + "</" + i.value + ">\n"
				
				if search_depth != len(search_yang):
					search_depth, depth, xml_str = search_internal(yinNode1, search_info, search_yang, search_depth, depth, xml_str)
				return search_depth, depth, xml_str
			elif i.type == "leaf":
				if i.namespace == None:
					xml_str += str_tab*depth + "<" + i.value + ">"
				else:
					xml_str += str_tab*depth + "<" + i.value + " xmlns=\"" + i.namespace + "\">"
				if search_info[search_depth] != None:
					xml_str += search_info[search_depth] + "</" + i.value + ">\n"
				else:
					xml_str += "</" + i.value + ">\n"
				search_depth += 1
				# if search_depth != len(search_yang):
				search_depth, depth, xml_str = search_internal(yinNode1, search_info, search_yang, search_depth, depth, xml_str)
				return search_depth, depth, xml_str
	
	return search_depth, depth, xml_str


def creatConfig(nc_info, nc_yang):
	# print(nc_info)
	# print(nc_yang)
	return search_yin(nc_info, nc_yang)

if __name__ == "__main__":
	init_yin()
	nc_info = [None, None, None, None, 'eth-10gi0/9/0/3.20', 'ETH-SUBIF', None, 'enable', None, 'disable', 'layer-2-switch', None, 'dot1q', None, '20']
	nc_yang = ['fos-interface-common', 'if', 'interfaces', 'interface', 'name', 'type', 'description', 'enabled', 'eth-option', 'loop-block', 'transport-layer', 'if-vlan-cfg', 'termination_type', 'vlan-sub-cfg', 'svlan_min']
	print(creatConfig(nc_info, nc_yang))

	nc_info = [None, None, None, None, '_public_', '13.1.1.1', '80:3A:F4:27:E7:00', 'none']
	nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type']
	print(creatConfig(nc_info, nc_yang))
	nc_info = [None, None, None, None, '_public_', '13.1.1.1', '80:3A:F4:27:E7:00', 'none', '123']
	nc_yang = ['fos-arp', 'arp', 'arp-statics', 'arp-static', 'vrf-name', 'ip-addr', 'mac-addr', 'vlan-type', '123123']
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
