# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields

class tour_insurance_line(models.Model):
	
    _name = "tour.insurance.line"
    _description = "Tour Insurance Line"
    
    book_id = fields.Many2one('tour.booking', 'Tour Booking')
    cancel_id = fields.Many2one('tour.cancellation', "Cancel Id")
    insurance_policy_id = fields.Many2one('insurance.policy', 'Insurance Policy', required=True)
    name = fields.Char('Adult Policy Coverage', required=True)
    chile_coverage1 = fields.Integer('Child Policy Coverage', required=True)
    insurance_cost = fields.Float('Total Cost', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: