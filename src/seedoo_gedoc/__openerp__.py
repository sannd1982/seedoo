# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

{
    'name': 'Seedoo GeDoc',
    'version': '1.0',
    'author': 'Innoviu',
    'category': 'Document Management',
    'sequence': 23,
    'summary': 'Gestione Documentale Seedoo',
    'description': """
Seedoo personalization for Public Administrations
==================================================

Manages the documents of a Public Administration

""",
    'author': 'Innoviu Srl',
    'website': 'http://www.innoviu.com',
    'depends':
        [
            'base',
            'document',
            'hr'],
    'data':
        [
            'security/gedoc_security.xml',
            'security/gedoc_security_rules.xml',
            'security/ir.model.access.csv',
            'data/gedoc_data.xml',
            'wizard/upload_doc_wizard_view.xml',
            'view/gedoc_view.xml',
            'workflow/gedoc_dossier_workflow.xml',
            ],
    'demo': [
        'demo/protocollo.classification.csv',
        'demo/data.xml',
        ],
    'css': ['static/src/css/gedoc.css'],
    'installable': True,
    'application': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
