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

    _columns = {
        'sender_receiver_ids': fields.one2many('protocollo.sender_receiver', 'gedoc_id', 'Destinatari'),
        'note_protocollazione': fields.text(
            'Note Protocollazione',
            required=True,
        ),
    }

    def richiedi_protocollazione(self, cr, uid, ids, *args):
        for gedoc in self.browse(cr, uid, ids):
            prot = gedoc.sender_receiver_ids.protocollo_id
            
            # super(protocollo_protocollo, self).action_register(cr, uid, [prot])
            # create attività
            # for prot in self.browse(cr, uid, prot_ids):
            now = datetime.datetime.now()
            user_list = []
            if prot.assigne_users:
                user_list = user_list + prot.assigne_users.ids
            if prot.assigne is not False:
                for d in prot.assigne:
                    department_manager = self.pool.get("hr.employee").browse(cr,uid,d.manager_id.id)
                    r = self.pool.get('resource.resource').browse(cr,uid, department_manager.resource_id.id)
                    if r:
                        user_list.append(r.user_id.id)


class sender_receiver(osv.Model):
    _inherit = 'protocollo.sender_receiver'

    _columns = {
        'gedoc_id': fields.many2one('gedoc.document', 'Documento'),
    }
