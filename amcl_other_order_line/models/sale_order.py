# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	other_order_line_ids = fields.One2many('sale.other.order.line', 'order_id', string='Other Order Lines')
	total_other_excluding_vat = fields.Monetary(string='Total Without VAT')
	other_tax_ids = fields.Many2many('account.tax', 'sale_order_other_tax_rel', string='Other Taxes', context={'active_test': False})
	total_other_vat = fields.Monetary(string='Total VAT')
	other_total = fields.Monetary(string='Total Net')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
