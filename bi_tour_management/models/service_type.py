# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class service_type(models.Model):

    _name = "service.type"
    _description = "Service Type"

    name = fields.Char('Description',required=True)
    service_id  = fields.Many2one('product.product','Service ',required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: