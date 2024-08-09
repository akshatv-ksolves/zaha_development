# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class tour_deduction_policy(models.Model):

    _name = "tour.deduction.policy"
    _description = "Tour Deduction Policy"

    name = fields.Integer("Minimum Limit (days) ",required=True)
    max_limit = fields.Integer("Maximum Limit (days) ",required=True)
    deduction_percentage = fields.Float("Deduction Percentage ",required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: