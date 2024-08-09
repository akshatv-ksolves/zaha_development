# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class visa_scheme(models.Model):

    _name = "visa.scheme"
    _description = "Visa Scheme"

    name = fields.Char('Name',required=True)
    duration = fields.Char('Duration In Days', required=True)
    service_cost = fields.Float('Sale Price ', required=True)
    cost_price = fields.Float('Cost Price ', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: