# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

import logging
from openerp.osv import fields, osv
from tools.translate import _
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)


class protocollo_sender_receiver_wizard(osv.TransientModel):
    _name = 'protocollo.sender_receiver.wizard'

    def on_change_partner(self, cr, uid, ids, partner_id, context=None):
        values = {}
        if partner_id:
            partner = self.pool.get('res.partner').\
                browse(cr, uid, partner_id, context=context)
            values = {
                'type': partner.is_company and 'individual' or 'legal',
                'name': partner.name,
                'street': partner.street,
                'city': partner.city,
                'country_id': partner.country_id and
                partner.country_id.id or False,
                'email_from': partner.email,
                'phone': partner.phone,
                'mobile': partner.mobile,
                'fax': partner.fax,
                'zip': partner.zip,
            }
        return {'value': values}

    _columns = {
        # TODO: inserire anche AOO in type?
        'wizard_id': fields.many2one('protocollo.pec.wizard',
                                     'Crea Protocollo'),
        'type': fields.selection([
            ('individual', 'Persona Fisica'),
            ('legal', 'Persona Giuridica'),
            ],
            'Tipologia',
            size=32,
            required=True,
            ),
        'partner_id': fields.many2one('res.partner', 'Anagrafica'),
        'name': fields.char('Nome Cognome/Ragione Sociale',
                            size=512,
                            required=True),
        'street': fields.char('Via/Piazza num civico', size=128),
        'zip': fields.char('Cap', change_default=True, size=24),
        'city': fields.char('Citta\'', size=128),
        'country_id': fields.many2one('res.country', 'Paese'),
        'email': fields.char('Email', size=240),
        'pec_mail': fields.char('PEC', size=240, required=True, readonly=True),
        'phone': fields.char('Telefono', size=64),
        'fax': fields.char('Fax', size=64),
        'mobile': fields.char('Cellulare', size=64),
        'notes': fields.text('Note'),
        'send_type': fields.many2one('protocollo.typology',
                                     'Mezzo di Spedizione'
                                     ),
        'send_date': fields.date('Data Spedizione'),
    }


class wizard(osv.TransientModel):
    """
        A wizard to manage the creation of
        document protocollo from pec message
    """
    _name = 'protocollo.pec.wizard'
    _description = 'Create Protocollo From PEC'
    _rec_name = 'subject'

    _columns = {
        'subject': fields.text('Oggetto',
                               required=True, readonly=True),
        'body': fields.html('Corpo della mail', readonly=True),
        'receiving_date': fields.datetime(
            'Data Ricezione',
            required=True,
            readonly=True),
        'classification': fields.many2one(
            'protocollo.classification',
            'Titolario di Classificazione',
            required=True,),
        'sender_receivers': fields.one2many(
            'protocollo.sender_receiver.wizard',
            'wizard_id',
            'Mittenti/Destinatari',
            required=True,
            limit=1),
        'dossier_ids': fields.many2many(
            'protocollo.dossier',
            'dossier_protocollo_pec_rel',
            'wizard_id', 'dossier_id',
            'Fascicoli'),
        # TODO: insert assigne here
        'notes': fields.text('Note'),
    }

    def _default_subject(self, cr, uid, context):
        mail_message = self.pool.get('mail.message').browse(
            cr,
            uid,
            context['active_id'],
            context=context
            )
        return mail_message.subject

    def _default_receiving_date(self, cr, uid, context):
        mail_message = self.pool.get('mail.message').browse(
            cr,
            uid,
            context['active_id'],
            context=context
            )
        # TODO: to verify
        return mail_message.date

    def _default_body(self, cr, uid, context):
        mail_message = self.pool.get('mail.message').browse(
            cr,
            uid,
            context['active_id'],
            context=context
            )
        return mail_message.body

    def _default_sender_receivers(self, cr, uid, context):
        mail_message = self.pool.get('mail.message').browse(
            cr,
            uid,
            context['active_id'],
            context=context
            )
        partner = mail_message.author_id
        res = []
        if partner:
            res.append({
                'partner_id': partner.id,
                'type': partner.is_company and 'legal' or 'individual',
                'name': partner.name,
                'street': partner.street,
                'zip': partner.zip,
                'city': partner.city,
                'country_id': partner.country_id.id,
                'email': partner.email,
                'phone': partner.phone,
                'fax': partner.fax,
                'mobile': partner.mobile,
                'pec_mail': mail_message.email_from
            })
        else:
            res.append({
                'name': mail_message.email_from,
                'pec_mail': mail_message.email_from,
                'type': 'individual',
            })
        return res

    _defaults = {
        'subject': _default_subject,
        'receiving_date': _default_receiving_date,
        'body': _default_body,
        'sender_receivers': _default_sender_receivers,
    }

    def action_save(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context=context)
        protocollo_obj = self.pool.get('protocollo.protocollo')
        sender_receiver_obj = self.pool.get('protocollo.sender_receiver')
        ir_attachment_obj = self.pool.get('ir.attachment')
        protocollo_typology_obj = self.pool.get('protocollo.typology')
        typology_id = protocollo_typology_obj.search(cr, uid,
                                                     [('pec', '=', True)]
                                                     )[0]
        mail_message_obj = self.pool.get('mail.message')
        mail_message = mail_message_obj.browse(cr, uid,
                                               context['active_id'],
                                               context=context)
        vals = {}
        vals['type'] = 'in'
        vals['typology'] = typology_id
        vals['receiving_date'] = wizard.receiving_date
        vals['subject'] = wizard.subject
        vals['body'] = wizard.body
        vals['classification'] = wizard.classification.id
        vals['dossier_ids'] = [[6, 0, [d.id for d in wizard.dossier_ids]]]
        vals['notes'] = wizard.notes
        vals['mail_pec_ref'] = context['active_id']
        vals['user_id'] = uid
        sender_receiver = []
        for send_rec in wizard.sender_receivers:
            srvals = {
                'type': send_rec.type,
                'partner_id': send_rec.partner_id and
                send_rec.partner_id.id or False,
                'name': send_rec.name,
                'street': send_rec.street,
                'zip': send_rec.zip,
                'city': send_rec.city,
                'country_id': send_rec.country_id and
                send_rec.country_id.id or False,
                'email': send_rec.email,
                'pec_mail': send_rec.pec_mail,
                'phone': send_rec.phone,
                'fax': send_rec.fax,
                'mobile': send_rec.mobile,
            }
            sender_receiver.append(sender_receiver_obj.create(cr, uid, srvals))
        vals['sender_receivers'] = [[6, 0, sender_receiver]]
        protocollo_id = protocollo_obj.create(cr, uid, vals)
        self.pool.get('mail.message').write(
            cr,
            SUPERUSER_ID,
            context['active_id'],
            {'pec_state': 'protocol'},
            context=context
            )
        # Attachments
        for attach in mail_message.attachment_ids:
            if attach.name == 'original_email.eml':
                protocollo_obj.write(
                    cr, uid, protocollo_id,
                    {
                        'datas_fname': attach.name,
                        'datas': attach.datas
                    }
                )
            else:
                ir_attachment_obj.create(
                    cr,
                    uid,
                    {
                        'name': attach.name,
                        'datas': attach.datas,
                        'datas_fname': attach.datas_fname,
                        'res_model': 'protocollo.protocollo',
                        'is_protocol': True,
                        'res_id': protocollo_id,
                    }
                )
        obj_model = self.pool.get('ir.model.data')
        model_data_ids = obj_model.search(
            cr,
            uid,
            [('model', '=', 'ir.ui.view'),
             ('name', '=', 'protocollo_protocollo_form')]
            )
        resource_id = obj_model.read(cr, uid,
                                     model_data_ids,
                                     fields=['res_id'])[0]['res_id']
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'protocollo.protocollo',
            'res_id': protocollo_id,
            'views': [(resource_id, 'form')],
            'type': 'ir.actions.act_window',
            'context': context,
        }
