# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields
    
class transport_carrier(models.Model):
	
    _name = "transport.carrier"
    _description = "Transport Carrier"

    name = fields.Char('Name',required=True)
    code = fields.Char('Code')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: