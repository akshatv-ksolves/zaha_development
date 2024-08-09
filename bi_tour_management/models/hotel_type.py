# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class hotel_type(models.Model):

    _name = "hotel.type"
    _description = "Hotel Type"

    name = fields.Char('Name',required=True)
    description = fields.Char('Description')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: