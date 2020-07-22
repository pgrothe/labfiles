import pyipmi
import pyipmi.interfaces

# Supported interface_types for ipmitool are: 'lan' , 'lanplus', and 'serial-terminal'
interface = pyipmi.interfaces.create_interface('ipmitool', interface_type='lan')

connection = pyipmi.create_connection(interface)

connection.target = pyipmi.Target(0x82)
connection.target.set_routing([(0x81,0x20,0),(0x20,0x82,7)])

connection.session.set_session_type_rmcp('172.16.31.11', port=623)
connection.session.set_auth_type_user('admin', 'admin')
connection.session.establish()

connection.get_device_id()