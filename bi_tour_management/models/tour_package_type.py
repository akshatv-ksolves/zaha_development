# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class tour_package_type(models.Model):

    _name = "tour.package.type"
    _description = "Tour Package Type"

    name = fields.Char("Tour Package",required=True)
    code = fields.Char("Package Code",required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

   
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: