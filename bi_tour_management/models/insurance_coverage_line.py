# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class insurance_coverage_line(models.Model):
	
    _name = "insurance.coverage.line"
    _description = "Insurance Coverage Line"

    policy_id = fields.Many2one('insurance.policy', 'Policy Id')
    product_id = fields.Many2one('product.product', 'Policy id',required = True)
    benifit_cost = fields.Float('Benifit Cost',required = True)
    company_id = fields.Many2one(
        related='policy_id.company_id',
        store=True, index=True, precompute=True)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: