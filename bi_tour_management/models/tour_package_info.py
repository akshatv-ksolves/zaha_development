# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class tour_package_info(models.Model):

    _name = "tour.package.info"
    _description = "Tour Package Info"

    package_type_id = fields.Many2one('tour.package.type', "Package",required=True)
    name = fields.Selection([
        ('international', 'International'),
        ('domastic', 'Domastic')], "Tour Type",required=True)
    tour_line_ids = fields.Many2many(
                    'tour.package',
                    'tour_package_tour_package_info_rel',
                    'tour_package_info_id',
                    'tour_package_id',
                    string="Tour Line"
                            )
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: