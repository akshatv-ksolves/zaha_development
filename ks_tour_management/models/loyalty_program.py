from odoo import api, fields, models

class LoyaltyProgram(models.Model):
    _inherit = 'loyalty.program'

    country_group_ids = fields.Many2many('res.country',string='Country Group')