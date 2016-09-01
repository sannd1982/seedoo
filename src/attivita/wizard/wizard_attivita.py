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
#
##############################################################################

from openerp.osv import fields, osv
import time
from openerp.tools.translate import _

class wizard_attivita(osv.osv_memory):
    _name = 'attivita.wizard.attivita'
    _description = 'Wizard Attivita'

    _columns = {
        'name': fields.text('Note', required=True),
        'case': fields.selection([('rifiuto', 'Rifiuto'), 
                                  ('annulla', 'Annullamento'),
                                  ('integrazione', 'Integrazione')],'Caso', readonly=True)
    }


    def default_get(self, cr, uid, fields, context=None):
        res = super(wizard_attivita, self).default_get(cr, uid, fields, context=context)
        if 'case' in context.keys():
            res['case'] = context['case']
        return res
    
    def rifiuta(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        attivita_obj = self.pool.get('attivita.attivita')
        attivita_id = context and context.get('active_id') or False
        for this in self.browse(cr, uid, ids, context=context):
            attivita_obj.write(cr,uid,attivita_id,{'state': 'rifiutato','motivazione_rifiuto': this.name})
            # Gestione della notifica
            configuration_obj = self.pool.get('brains.configuration')
            configuration_ids = self.pool.get('brains.configuration').search(cr,uid,[])
            if len(configuration_ids) == 1:
                configuration = configuration_obj.browse(cr,uid,configuration_ids[0])
            if configuration.module_attivita_notifiche and configuration.notifica_referente_rifiuto:
                template_model_data = self.pool.get('ir.model.data').search(cr, uid, [('name', '=', 'template_email_notifica_referente_rifiuto')])
                if len(template_model_data):
                    template_id = self.pool.get('ir.model.data').browse(cr, uid, template_model_data[0])
                    self.pool.get('email.template').generate_email(cr, uid, template_id.res_id,attivita_id, context)
                    

    def integrazione(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        attivita_obj = self.pool.get('attivita.attivita')
        attivita_id = context and context.get('active_id') or False
        for this in self.browse(cr, uid, ids, context=context):
            attivita_obj.write(cr,uid,attivita_id,{'state': 'lavorazione','motivazione_richiesta_integrazione': this.name, 'richiesta_integrazione': True}) 

    
    def annulla(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        attivita_obj = self.pool.get('attivita.attivita')
        attivita_id = context and context.get('active_id') or False
        for this in self.browse(cr, uid, ids, context=context):
            attivita_obj.write(cr,uid,attivita_id,{'state': 'annullato','motivazione_annullamento': this.name}) 
            # Gestione della notifica
            configuration_obj = self.pool.get('brains.configuration')
            configuration_ids = self.pool.get('brains.configuration').search(cr,uid,[])
            if len(configuration_ids) == 1:
                configuration = configuration_obj.browse(cr,uid,configuration_ids[0])
            if configuration.module_attivita_notifiche and configuration.notifica_assegnatario_annullamento:
                template_model_data = self.pool.get('ir.model.data').search(cr, uid, [('name', '=', 'template_email_notifica_assegnatario_annullamento')])
                if len(template_model_data):
                    template_id = self.pool.get('ir.model.data').browse(cr, uid, template_model_data[0])
                    self.pool.get('email.template').generate_email(cr, uid, template_id.res_id,attivita_id, context)
   

