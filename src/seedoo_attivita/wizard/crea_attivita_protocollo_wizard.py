# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

import logging
from openerp.osv import fields, osv
from openerp.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT as DSDF)
from openerp.tools.translate import _
import time
from openerp import netsvc
import datetime
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)

MAPPING_PRIORITIES = {'1': 'Alta', '2': 'Normale', '3': 'Bassa'}

AVAILABLE_PRIORITIES = [
    ('1', 'Alta'),
    ('2', 'Normale'),
    ('3', 'Bassa'),
]


class wizard(osv.TransientModel):
    """
        Wizard per la creazione di un'attività dal protocollo
    """
    _name = 'create.activity.wizard'
    _description = 'Creazione Attivita Wizard'

    _columns = {
        'name': fields.char('Nome', required=True),
        'descrizione': fields.text("Descrizione dell'attività"),
        'data_assegnazione': fields.date('Data Assegnazione'),
        'categoria': fields.many2one('attivita.categoria', 'Categoria',
                                     domain="[('protocollo', '=', True)]"),
        'assegnatario_id': fields.many2one('res.users', 'Assegnatario', domain="[('is_visible','=',True)]"),
        'priorita': fields.selection(AVAILABLE_PRIORITIES, 'Priorità', select=True),

    }

    def action_request(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context)
        if 'active_id' in context.keys():
            protocollo_id = context['active_id']
            protocollo_obj = self.pool.get('protocollo.protocollo')
            prot = protocollo_obj.browse(cr, uid, protocollo_id)

            user = wizard.assegnatario_id.user_id

            now = datetime.datetime.now()
            categoria_obj = self.pool.get('attivita.categoria')

            if len(wizard.categoria.ids) == 1:
                category = categoria_obj.browse(cr, uid, wizard.categoria.id)
                tempo_esecuzione_attivita = category.tempo_standard
            data_scadenza = now + datetime.timedelta(days=tempo_esecuzione_attivita)

            assigne_users_ids = prot.assigne_users.ids
            assegnatario_id = wizard.assegnatario_id.id
            if assegnatario_id not in assigne_users_ids:
                assigne_users_ids.append(assegnatario_id)       
                
                # aggiorno l'istanza protocollo
                protocollo_vals = {
                    'assigne_users': [(6, 0, assigne_users_ids)],
                }
                protocollo_obj.write(cr, SUPERUSER_ID, prot.id, protocollo_vals, context=None)

            activity_vals = {
                'name': "Creazione Attivita: %s - protocollo num %s a %s " % (
                    wizard.name, prot.name, wizard.assegnatario_id.name),
                'descrizione': wizard.descrizione,
                'priorita': wizard.priorita,
                'referente_id': uid,
                'assegnatario_id': assegnatario_id,
                'state': 'assegnato',
                'data_scadenza': data_scadenza,
                'data_assegnazione': now,
                'data_presa_carico': now,
                'categoria': category.id,
                'protocollo_id': prot.id
            }

            self.pool.get("attivita.attivita").create(cr, SUPERUSER_ID, activity_vals, context=None)
            return {'type': 'ir.actions.act_window_close'}
        else:
            raise osv.except_osv(_("Warning! - create.activity.wizard"), _("Errore nei campi!!."))




            # class res_users(osv.Model):
            #     _name = 'res.users'
            #     _inherit = ['res.users']
            #     _description = 'User'
            # 
            #     def _is_visible(self, cr, uid, ids, name, arg, context={}):
            #         res = {}.fromkeys(ids, '0')
            #         return res
            # 
            #     def _is_visible_search(self, cr, uid, obj, names, arg, context=None):
            #         return [('id', '>', 0)]
            # 
            #     _columns = {
            #         'is_visible': fields.function(_is_visible, fnct_search=_is_visible_search, type="boolean", method=True,
            #                                       string='Assegnatario'),
            # 
            #     }
