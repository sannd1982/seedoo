# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

from openerp.osv import fields, orm
from openerp import SUPERUSER_ID


class MailMessage(orm.Model):
    _inherit = "mail.message"

    _columns = {
        'pec_state': fields.selection([
            ('new', 'To Protocoll'),
            ('protocol', 'Protocols'),
            ('not_protocol', 'No Protocol')
            ], 'Pec State', readonly=True),
    }
    _defaults = {
        'pec_state': 'new'
    }

    def action_not_protocol(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, SUPERUSER_ID, ids[0], {'pec_state': 'not_protocol'})
        return True

    def name_get(self, cr, user, ids, context=None):
        if not ids:
            return []
        if isinstance(ids, (int, long)):
            ids = [ids]
        result = self.browse(cr, user, ids, context=context)
        res = []
        for rs in result:
            name = "%s - %s" % (rs.email_from, rs.subject)
            res += [(rs.id, name)]
        return res

