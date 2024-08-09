from odoo import api, fields, models

class ProductTemplates(models.Model):
    _inherit = "product.template"

    # seasonal_offer_id = fields.Many2one('seasonal.offer')
