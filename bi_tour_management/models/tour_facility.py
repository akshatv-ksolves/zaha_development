# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields

    
class tour_facility(models.Model):

    _name = "tour.facility"
    _description = "Tour Facility"

    name = fields.Char('Facility Name ', required=True)
    code = fields.Char('Code',required=True)
    desc = fields.Char('Description')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: