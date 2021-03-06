import json
from credentials import URL, CERT, LOGIN, PASSWORD
from fabric_data import FABRIC
from dcnmtoolkit import Session, SwitchDetails, TemplateDetails
from templates import POAP_LEAF_TMPL, POAP_SPINE_TMPL
import logging

logging.getLogger(__name__)


def build_poap_def(switch_details, template_name, template_params):
    poap_definition = {'switchDetails': [switch_details],
                       'templateDetails': [{'templateName': template_name,
                                            'templateParams': template_params}]}
    return poap_definition


def main(url=None, cert=None):
    """My Main"""
    poap_url = '/rest/poap/definitions'
    session = Session(url, LOGIN, PASSWORD, logging_lvl='INFO', verify=cert)
    session.login()

    fabric_elements = ['BorderLeaf', 'DatacenterCore', 'Spine', 'Leaf', 'BorderGateway']

    for switch_definitions in fabric_elements:
        for definitions in FABRIC[switch_definitions]:
            if switch_definitions is 'Spine' or switch_definitions is 'DatacenterCore':
                template_name = 'IPFabric_N9K_Spine_10_2_1_ST_1_TAG'
                template_params = POAP_SPINE_TMPL['templateDetails'][0]['templateParams']
            else:
                template_name = 'IPFabric_N9K_Leaf_10_2_1_ST_1_TAG'
                template_params = POAP_LEAF_TMPL['templateDetails'][0]['templateParams']

            switch_details = SwitchDetails(definitions=definitions)
            template_params = TemplateDetails(template_params=template_params, definitions=definitions)
            body = build_poap_def(switch_details.get_details(), template_name, template_params.get_details())
            resp = session.push_to_dcnm(poap_url, json.dumps(body))

            logging.info('HTTP POST response %s' % resp)


if __name__ == "__main__":
    main(url=URL['58'], cert=CERT['58'])
