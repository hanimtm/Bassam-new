# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOtherOrderLine(models.Model):
    _name = 'sale.other.order.line'
    _description = 'Other Order Line'
    _order = 'order_id, sequence, id'

    order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)

    product_id = fields.Many2one(
        'product.product', string='Product', domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        change_default=True, ondelete='restrict', check_company=True)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    name = fields.Text(string='Description', required=True)
    company_id = fields.Many2one(related='order_id.company_id', string='Company', store=True, index=True)
    product_uom = fields.Many2one('uom.uom', string='UoM')
    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)
    sequence = fields.Integer(string='Sequence', default=10)
    state = fields.Selection(related='order_id.state', string='Order Status', copy=False, store=True)
    currency_id = fields.Many2one(related='order_id.currency_id', depends=['order_id.currency_id'], store=True, string='Currency')

    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Total Tax', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)

    price_reduce = fields.Float(compute='_compute_price_reduce', string='Price Reduce', digits='Product Price', store=True)
    tax_id = fields.Many2many('account.tax', string='Taxes', context={'active_test': False})
    price_reduce_taxinc = fields.Monetary(compute='_compute_price_reduce_taxinc', string='Price Reduce Tax inc', store=True)
    price_reduce_taxexcl = fields.Monetary(compute='_compute_price_reduce_taxexcl', string='Price Reduce Tax excl', store=True)


    @api.onchange('product_id')
    def  onchange_product(self):
        name = ''
        uom = False
        price_unit = 0.0
        if self.product_id:
            if self.product_id.uom_id:
                uom_id = self.product_id.uom_id.id
            if self.product_id.default_code:
                name += '['+ self.product_id.default_code +'] '
            price_unit = self.product_id.lst_price
            name += self.product_id.name
        self.name = name
        self.product_uom = uom

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

    @api.depends('price_unit', 'discount')
    def _compute_price_reduce(self):
        for line in self:
            line.price_reduce = line.price_unit * (1.0 - line.discount / 100.0)

    @api.depends('price_total', 'product_uom_qty')
    def _compute_price_reduce_taxinc(self):
        for line in self:
            line.price_reduce_taxinc = line.price_total / line.product_uom_qty if line.product_uom_qty else 0.0

    @api.depends('price_subtotal', 'product_uom_qty')
    def _compute_price_reduce_taxexcl(self):
        for line in self:
            line.price_reduce_taxexcl = line.price_subtotal / line.product_uom_qty if line.product_uom_qty else 0.0

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
