# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date
from dateutil import relativedelta

class PropertyBuilding(models.Model):
    _name = 'property.building'
    _description = 'Property Building'

    name = fields.Char('Name', index=True, required=True, translate=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Favorite'),
    ], default='0', string="Favorite")
    building_type = fields.Many2one('building.type', 'Type')
    location = fields.Char("Address")
    city = fields.Char()
    street = fields.Char()
    zipcode = fields.Integer("Zip")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    phone = fields.Char("Phone")
