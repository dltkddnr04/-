import upnpy

upnp = upnpy.UPnP()
devices = upnp.discover()
device = upnp.get_igd()
service = device['WANIPConn1']

def get_external_ip():
    external_ip = service.GetExternalIPAddress()
    external_ip = external_ip['NewExternalIPAddress']
    return external_ip

def get_port_mapping_list():
    port_mapping_list = []
    i = 0
    while True:
        try:
            data = service.GetGenericPortMappingEntry(NewPortMappingIndex=i)
            port_mapping_list.append(data)
            i += 1
        except:
            break
    return port_mapping_list

def make_port_mapping(internal_ip, external_port, internal_port, protocol, description):
    try:
        service.AddPortMapping(
            NewRemoteHost='',
            NewExternalPort=external_port,
            NewProtocol=protocol,
            NewInternalPort=internal_port,
            NewInternalClient=internal_ip,
            NewEnabled=1,
            NewPortMappingDescription=description,
            NewLeaseDuration=0
        )
        return True
    except:
        return False
