# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
{
    'name' : 'attivita',
    'version' : '1.0',
    'author' : 'Flosslab S.r.l',
    'sequence': 1,
    'category': 'Processi',
    'website' : 'http://www.flosslab.com',
    'description' : """
Gestione della attività
""",
    'css' : [
    "static/src/css/style.css",
    ],
    'depends': [
        'base_setup',
        'board',
        'mail',
        'resource',
        'web_kanban',
        'hr',
    ],
    'data' : [
        'security/account_security.xml',
        'security/ir.model.access.csv',
        'wizard/assegna_attivita_view.xml',
        'wizard/wizard_attivita_view.xml',
        'wizard/registra_aggiornamento_view.xml',
        'view/attivita_view.xml',
        'data/email_notifications.xml'
    ],
    'images': [],
    'update_xml' : [],

    'demo': [],
    'application': True,
    'installable' : True,
}
#
##############################################################################
