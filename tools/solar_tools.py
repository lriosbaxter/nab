from orionsdk import SwisClient
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning


class NPMDevice:
    @classmethod
    def create_npm_dictionary(cls,
                              data: dict) -> dict:
        return {
            'npm_server': data.get('ip_address'),
            'username': data.get('username'),
            'password': data.get('password')
        }

    @classmethod
    def create_props_node(cls, sheet_row) -> dict:
        return {
            'Caption': sheet_row[0].value,
            'IPAddress': sheet_row[1].value,
            'EngineID': sheet_row[3].value,
            'PollInterval': sheet_row[4].value,
            'ObjectSubType': 'SNMP',
            'SNMPVersion': 2,
            'Community': 'Int#rn4lV1#wOlny',
        }

    @classmethod
    def create_props_node_cp(cls, sheet_row) -> dict:
        return {
            'City': sheet_row[5].value,
            'CityCode_Network': sheet_row[6].value,
            'Company': sheet_row[7].value,
            'Country': sheet_row[8].value,
            'Department': sheet_row[9].value,
            'Device_Type_NCM': sheet_row[10].value,
            'EdgeRouter': sheet_row[11].value,
            'Environment': sheet_row[12].value,
            'Hillrom_App': sheet_row[13].value,
            'Hillrom_Support_Group': sheet_row[14].value,
            'Node_Contact_1': sheet_row[15].value,
            'PollingEngine': sheet_row[16].value,
            'Region': sheet_row[17].value,
            'Rtr_Bandwidth_Alerting': sheet_row[18].value,
            'ServiceNow_LCON': sheet_row[19].value,
            'ServiceNow_Queue': sheet_row[20].value,
            'SiteID': sheet_row[21].value,
            'TypeOfSite': sheet_row[22].value,
            'Voice_ISDN': sheet_row[23].value,
        }

    @classmethod
    def create_dict_from_properties(cls, properties) -> dict:
        prop_node = {}
        props = list(properties)
        for prop in props:
            value = properties[prop]
            if not value == '-':
                if prop == 'SiteID' or prop == 'PollInterval' or prop == 'EngineID':
                    prop_node[prop] = int(value)
                else:
                    prop_node[prop] = value
        return prop_node

    @classmethod
    def npm_connection(cls, data: dict):
        disable_warnings(InsecureRequestWarning)

        return SwisClient(data.get('npm_server'),
                          data.get('npm_username'),
                          data.get('npm_password'))

    @classmethod
    def npm_send_query(cls,
                       npm_connection, query: str,
                       **args):
        disable_warnings(InsecureRequestWarning)
        return npm_connection.query(query, **args)

    @classmethod
    def npm_invoke(cls, swis_connection, invoke_entity, invoke_verb,
                   *args):
        disable_warnings(InsecureRequestWarning)
        return swis_connection.invoke(invoke_entity, invoke_verb, *args)

    @classmethod
    def npm_create(cls, swis_connection, create_entity, **kwargs):
        disable_warnings(InsecureRequestWarning)
        return swis_connection.create(create_entity, **kwargs)

    @classmethod
    def npm_update(cls, swis_connection, uri, **kwargs):
        disable_warnings(InsecureRequestWarning)
        return swis_connection.update(uri, **kwargs)

    @classmethod
    def npm_read(cls, swis_connection, uri):
        disable_warnings(InsecureRequestWarning)
        return swis_connection.read(uri)
