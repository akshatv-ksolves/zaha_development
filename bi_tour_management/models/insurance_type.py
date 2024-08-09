# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class insurance_type(models.Model):
	
    _name = "insurance.type"
    _description = "Insurance Type"

    name = fields.Char('Name',required = True)
    code = fields.Char('Code',required = True)
    adult_cost= fields.Float('For Adults Insurance Cost ',required = True)
    child_cost = fields.Float('For Child Insurance Cost ',required = True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: