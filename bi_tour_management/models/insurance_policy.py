# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _

class insurance_policy(models.Model):

    _name = "insurance.policy"
    _description = "Insurance Policy"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ],string="Status", default="draft")
    book_id = fields.Many2one('tour.booking', 'Tour Booking')
    insurance_type_id = fields.Many2one('insurance.type', 'Insurance')
    name = fields.Char('Insurance Name')
    insurance_cost_for_adults = fields.Float('Insurance Cost For Adults',required = True)
    insurance_cost_for_childs = fields.Float('Insurance Cost For Child',required = True)
    coverage_line_ids = fields.One2many('insurance.coverage.line','policy_id','Coverage Lines')
    total_cost = fields.Float("Total Cost",compute="_compute_total_cost",readonly=True)
    insurance_policy_id = fields.Many2one('insurance.policy', 'Insurance Policy')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    

    @api.depends("book_id.adult","book_id.child")
    def _compute_total_cost(self):
        x=0.0
        y=0.0
        total_cost_ins = 0.0
        for i in self:
            if i.book_id.adult:
                x = i.book_id.adult * i.insurance_cost_for_adults
            elif i.book_id.child:
                y = i.book_id.child * i.insurance_cost_for_childs
            else:
                x = 0.0
                y = 0.0
            total_cost_ins = x+y
            i.total_cost = total_cost_ins
    def button_confirm(self):
        for rec in self:
            rec.state = 'confirm'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: