from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

selection_data = [
    ('regular', 'Regular','timesheet_type'),
    ('overtime', 'Overtime','timesheet_type'),
]

def _get_selections(name):
   data = filter(lambda x: x[2] == name, selection_data)
   return list(map(lambda x: (x[0], x[1]), data))


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    timesheet_type = fields.Selection(lambda self: _get_selections('timesheet_type'), string='Type', default='regular', required=True)

    def write(self, vals):
        if 'unit_amount' in vals:
            self.validate_hours_spent(vals)
        res = super().write(vals)
        return res
    
    @api.model
    def validate_hours_spent(self, vals):
        date = False
        if self:
            date = self.date
        else:
            date = vals.get('date')
        timesheet_ids = self.env['account.analytic.line'].search([('date', '=', date),('is_timesheet', '=', True)])
        timeshee_hor_lst = [timesheet.unit_amount for timesheet in timesheet_ids]
        total_amount = sum(timeshee_hor_lst)
        if total_amount > 10:
            raise ValidationError(_("Total hours spent on '%s' can not be more than 10 hours."%(date)))
