import json
from dcnmtoolkit import Session, SwitchDetails, LANFabric, TemplateDetails
from credentials import URL, CERT, LOGIN, PASSWORD
from fabric_data import FABRIC


def save_objs_details_to_file(objs, filename):
    import os
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(file_dir, filename)
    details = []
    for obj in objs:
        details.append(obj.get_details())
    with open(filename, 'w') as f:
        json.dump(details, f, indent=4, sort_keys=True)
    return details


def dict_to_csv(_dict, filename='data.csv'):
    import csv
    import os
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(file_dir, filename)
    keys = _dict[0].keys()
    with open(filename, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(_dict)


def csv_to_dict(filename):
    import csv
    with open(filename) as f:
        _dict = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    return _dict


def main(url=None, cert=None):
    """My Main"""
    session = Session(url, LOGIN, PASSWORD, logging_lvl='INFO', verify=cert)
    session.login()

    save_objs_details_to_file(LANFabric.get(session), 'VXLAN_EVPN_Fabric/json/LANFabric.json')
    save_objs_details_to_file(SwitchDetails.get(session), 'VXLAN_EVPN_Fabric/json/SwitchDefinition.json')
    save_objs_details_to_file(TemplateDetails.get(session), 'VXLAN_EVPN_Fabric/json/PoapTemplateLeaf.json')

    fabric_elements = ['BorderLeaf', 'DatacenterCore', 'Spine', 'Leaf', 'BorderGateway']

    for switch_definitions in fabric_elements:
        dict_to_csv(FABRIC[switch_definitions], 'VXLAN_EVPN_Fabric/csv/' + switch_definitions + '.csv')


if __name__ == "__main__":
    main(url=URL['99'], cert=CERT['99'])
