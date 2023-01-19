# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

selection_data = [
    ('0', 'No','attachment'),
    ('1', 'Yes','attachment'),
]

def _get_selections(name):
   data = filter(lambda x: x[2] == name, selection_data)
   return list(map(lambda x: (x[0], x[1]), data))


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    need_attachment = fields.Selection(lambda self: _get_selections('attachment'),
        string='Need An Attachmenet',
        compute='set_need_attachment',
        default='0')
    payment_term_attachment = fields.Binary(string='Payment Term Attachment')
    has_an_attachment = fields.Selection(lambda self: _get_selections('attachment'),
        string='Has An Attachment',
        default='0')

    @api.depends('payment_term_id')
    def set_need_attachment(self):
        value = '0'
        if self.payment_term_id:
            if self.payment_term_id.name not in ['Cash', 'cash']:
                value = '1'
        self.need_attachment = value

    def action_confirm(self):
        self.validate_with_payment_term()
        res = super().action_confirm()
        return res

    def validate_with_payment_term(self):
        if not self.payment_term_id:
            return True
        if self.payment_term_id.name not in ['Cash', 'cash']:
            raise ValidationError(_('Please add Payment Term Attachment for payment term.'))

    @api.onchange('payment_term_attachment')
    def onchange_payment_term_attachment(self):
        if self.payment_term_attachment:
            self.has_an_attachment = '1'
        else:
            self.has_an_attachment = '0'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: