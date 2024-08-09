# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class agent_commision_line(models.Model):

    _name = "agent.commission.line"
    _description = "Agent Commission Line"
    
    tour_package_id = fields.Many2one('tour.package','Tour')
    name = fields.Char('Tour Name',related= 'tour_package_id.product_id.name')
    agent_partner_id = fields.Many2one('res.partner','Partner')
    commission_percentage = fields.Integer('Commission Percentage')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: