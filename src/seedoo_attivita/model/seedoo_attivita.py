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


class attivita_categoria(osv.Model):
    _inherit = "attivita.categoria"

    _columns = {
        'protocollo': fields.boolean("Categoria di protocollo"),
    }


class attivita_attivita(orm.Model):

    _inherit = "attivita.attivita"

    _columns = {
        'protocollo_id': fields.many2one('protocollo.protocollo', 'Protocollo', readonly=True),
        'titolario_id': fields.many2one('protocollo.classification', 'Titolario', readonly=False),
        'template': fields.boolean("Template"),
        'template_instance': fields.boolean("Creato da template"),
        'protocollo': fields.related('categoria',
            'protocollo',
            type='boolean',
            string='Attivita di Protocollo',)
    }

    _defaults ={
        'template': False,
        'template_instance': False,
    }

    def create(self, cr, uid, data, context=None):
        if data.has_key('titolario_id') and data['titolario_id']:
            data['template'] = True
        else:
            data['template'] = False
        attivita_id = super(attivita_attivita, self).create(cr, uid, data, context=context)
        return attivita_id

class protocollo_classification(orm.Model):

    _inherit = "protocollo.classification"

    _columns = {
        'attivita_ids': fields.one2many('attivita.attivita', 'titolario_id', 'Attivita', readonly=False),
    }

class protocollo_protocollo(orm.Model):

    _inherit = "protocollo.protocollo"

    _columns = {
        'attivita_ids': fields.one2many('attivita.attivita', 'protocollo_id', 'Attivita', readonly=True),
    }

    def write(self, cr, uid, ids, data, context=None):
        res_id = super(protocollo_protocollo, self).write(cr, uid, ids, data, context=context)
        now = datetime.datetime.now()
        prot = self.browse(cr,uid,ids)
        if data.has_key('classification') and prot.state != 'draft':
            attivita_obj = self.pool.get("attivita.attivita")
            for attivita in prot.attivita_ids:
                if attivita.template_instance and attivita.state in ['assegnato','lavorazione']:
                    attivita_obj.write(cr,uid,attivita.id,{'state': 'annullato','motivazione_annullamento': 'Modifica classificazione protocollo correlato'})
            if prot.classification and len(prot.classification.attivita_ids) > 0:
                for attivita_titolario in prot.classification.attivita_ids:
                    tempo_esecuzione_attivita = attivita_titolario.categoria.tempo_standard
                    data_scadenza =  now + datetime.timedelta(days=tempo_esecuzione_attivita)
                    activity_vals = {
                        'name': "Protocollo num %s - "%(prot.name) + attivita_titolario.name,
                        'descrizione': attivita_titolario.descrizione,
                        'priorita': attivita_titolario.priorita,
                        'referente_id': uid,
                        'assegnatario_id': attivita_titolario.assegnatario_id.id,
                        'state': 'assegnato',
                        'data_scadenza': data_scadenza,
                        'data_assegnazione': now,
                        'categoria': attivita_titolario.categoria.id,
                        'protocollo_id': prot.id,
                        'template_instance': True,
                    }
                    attivita_obj.create(cr,SUPERUSER_ID, activity_vals, context=None)
                    res_id = self.write(cr,uid,ids,{'assigne_users': [(4, attivita_titolario.assegnatario_id.id)]})
        return res_id



    def action_register(self, cr, uid, ids, *args):
        super(protocollo_protocollo, self).action_register(cr, uid, ids)
        # create attività
        for prot in self.browse(cr, uid, ids):
            now = datetime.datetime.now()
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
                    'categoria': category.id,
                    'protocollo_id': prot.id
                }
                #TODO we need to use the uid instead of SUPERUSER_ID
                self.pool.get("attivita.attivita").create(cr,SUPERUSER_ID, activity_vals, context=None)
            if prot.classification and len(prot.classification.attivita_ids) > 0:
                assegnatari_list = []
                for attivita_titolario in prot.classification.attivita_ids:
                    tempo_esecuzione_attivita = attivita_titolario.categoria.tempo_standard
                    data_scadenza =  now + datetime.timedelta(days=tempo_esecuzione_attivita)
                    activity_vals = {
                        'name': "Protocollo num %s - "%(prot.name) +attivita_titolario.name,
                        'descrizione': attivita_titolario.descrizione,
                        'priorita': attivita_titolario.priorita,
                        'referente_id': uid,
                        'assegnatario_id': attivita_titolario.assegnatario_id.id,
                        'state': 'assegnato',
                        'data_scadenza': data_scadenza,
                        'data_assegnazione': now,
                        'categoria': attivita_titolario.categoria.id,
                        'protocollo_id': prot.id,
                        'template_instance': True,
                    }
                    assegnatari_list.append(attivita_titolario.assegnatario_id.id)
                    self.pool.get("attivita.attivita").create(cr,SUPERUSER_ID, activity_vals, context=None)
                    self.write(cr,uid,ids,{'assigne_users': [(4, attivita_titolario.assegnatario_id.id)]})
        return True
