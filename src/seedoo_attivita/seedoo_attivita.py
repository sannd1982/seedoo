# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

from openerp.osv import orm
from openerp.osv import fields, osv
import logging
from openerp.osv import *
import datetime
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)


class attivita_attivita(orm.Model):

    _inherit = "attivita.attivita"

    _columns = {
        'protocollo_id': fields.many2one('protocollo.protocollo', 'Protocollo', readonly=True),
    }

class protocollo_protocollo(orm.Model):

    _inherit = "protocollo.protocollo"

    _columns = {
        'attivita_ids': fields.one2many('attivita.attivita', 'protocollo_id', 'Attivita', readonly=True),
    }

    def action_register(self, cr, uid, ids, *args):
        super(protocollo_protocollo, self).action_register(cr, uid, ids)
        # create attività
        for prot in self.browse(cr, uid, ids):
            user_list = []
            if prot.assigne_users:
                user_list = user_list + prot.assigne_users.ids
            if prot.assigne:
                for d in prot.assigne:
                    department_manager = self.pool.get("hr.employee").browse(cr,uid,d.manager_id.id)
                    r = self.pool.get('resource.resource').browse(cr,uid, department_manager.resource_id.id)
                    if r:
                        user_list.append(r.user_id.id)

            for u in list(set(user_list)):
                now = datetime.datetime.now()
                categoria_obj = self.pool.get('attivita.categoria')
                category_ids = categoria_obj.search(cr,uid,[('name','=','Assegnazione Protocollo')])
                tempo_esecuzione_attivita = 15
                if len(category_ids) == 1:
                    category = categoria_obj.browse(cr,uid,category_ids[0])
                    tempo_esecuzione_attivita = category.tempo_standard
                data_scadenza =  now + datetime.timedelta(days=tempo_esecuzione_attivita)
                user = self.pool.get('res.users').browse(cr,uid,u)

                activity_vals = {
                    'name': "Assegnazione protocollo num %s a %s "%(prot.name,user.partner_id.name),
                    'descrizione': prot.subject,
                    'priorita': '3',
                    'referente_id': prot.user_id.id,
                    'assegnatario_id': u,
                    'state': 'assegnato',
                    'data_scadenza': data_scadenza,
                    'data_assegnazione': now,
                    'data_presa_carico': now,
                    'categoria': category.id,
                    'protocollo_id': prot.id
                }
                #TODO we need to use the uid instead of SUPERUSER_ID
                self.pool.get("attivita.attivita").create(cr,SUPERUSER_ID, activity_vals, context=None)
        return True
