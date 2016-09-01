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

class registra_aggiornamento(osv.osv_memory):
    _name = 'attivita.registra.aggiornamento'
    _description = 'Registra Aggiornamento'

    _columns = {
        'name': fields.text('Note', required=True),
        'avanzamento_attivita': fields.boolean('Aggiorna Stato Avanzamento'),
        'avanzamento': fields.integer('Avanzamento'),
            }
    
    def default_get(self, cr, uid, fields, context=None):
        res = super(registra_aggiornamento, self).default_get(cr, uid, fields, context=context)
        attivita_obj = self.pool.get('attivita.attivita')
        attivita_id = context and context.get('active_id') or False
        attivita = attivita_obj.browse(cr,uid,attivita_id)
        res['avanzamento'] = attivita.avanzamento
        return res

    
    def registra(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        attivita_obj = self.pool.get('attivita.attivita')
        aggiornamento_obj = self.pool.get('attivita.aggiornamento')
        attivita_id = context and context.get('active_id') or False
        attivita = attivita_obj.browse(cr,uid,attivita_id)
        if attivita.assegnatario_id.id != uid:
            raise osv.except_osv(_('Attenzione!'), _("Solo l'assegnatario puo' aggiornare l'attivita'!"))
        for this in self.browse(cr, uid, ids, context=context):
            aggiornamento_obj.create(cr,uid,{'name': this.name,  'attivita_id': attivita_id, 'referente_id': attivita.referente_id.id, 'autore_id': uid})
            attivita_vals = {'ultimo_aggiornamento':  time.strftime("%Y-%m-%d %H:%M:%S")}
            if this.avanzamento_attivita:
                attivita_vals['avanzamento'] = this.avanzamento
            attivita_obj.write(cr,uid,attivita_id,attivita_vals)
    

