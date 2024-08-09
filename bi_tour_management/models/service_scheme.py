# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class service_scheme(models.Model):

    _name = "service.scheme"
    _description = "Service Scheme"

    name = fields.Char('Name',required=True)
    duration = fields.Char('Duration In Days', required=True)
    service_cost = fields.Float('Service Cost ', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: