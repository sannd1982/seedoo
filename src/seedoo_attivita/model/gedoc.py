# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

from openerp.osv import orm
from openerp.osv import fields, osv
import logging
from openerp.osv import *
import datetime
from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _
from seedoo_protocollo.model.protocollo import protocollo_protocollo

_logger = logging.getLogger(__name__)


class gedoc_document(osv.Model):
    _inherit = 'gedoc.document'

    STATE_SELECTION = [
        ('draft', 'Compilazione'),
        ('protocol', 'Da protocollare'),
    ]
    _columns = {
        'typology': fields.many2one('protocollo.typology', 'Tipologia', required=True,
                                    help="Tipologia invio/ricevimento: Raccomandata, Fax, PEC, etc. si possono inserire nuove tipologie dal menu Tipologie."),
        'sender_receiver_ids': fields.one2many('protocollo.sender_receiver', 'gedoc_id', 'Destinatari'),
        'note_protocollazione': fields.text('Note Protocollazione', required=True),
        'state': fields.selection(STATE_SELECTION, 'Stato', readonly=True, help="Lo stato del documento.", select=True)
    }

    _defaults = {
        'state': 'draft',
    }

    def richiedi_protocollazione(self, cr, uid, ids, context=None):
        # gedoc = self.browse(cr, uid, ids[0], context)
        for gedoc in self.browse(cr, uid, ids[0], context):
            prot = gedoc.sender_receiver_ids.protocollo_id

            protocollo_vals = {
                'subject': gedoc.note_protocollazione,
                'sender_receivers': [(6, 0, gedoc.sender_receiver_ids.ids)],
                'typology': gedoc.typology.id,
                'type': 'out',
                'doc_id': gedoc.main_doc_id.id,
                'datas_fname': gedoc.main_doc_id.name,
                'mimetype': gedoc.main_doc_id.file_type,
                'datas': gedoc.main_doc_id.datas
            }
            self.pool.get("protocollo.protocollo").create(cr, uid, protocollo_vals, context=None)
            self.write(cr, uid, [gedoc.id], {'state': 'protocol'})
        return True


class sender_receiver(osv.Model):
    _inherit = 'protocollo.sender_receiver'

    _columns = {
        'gedoc_id': fields.many2one('gedoc.document', 'Documento'),
    }
