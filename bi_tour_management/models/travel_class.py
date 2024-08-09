# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields

class travel_class(models.Model):
	
    _name = "travel.class"
    _description = "Travel Class"

    name= fields.Char('Name',required=True)
    code = fields.Char('Code')
    transport_type_id = fields.Many2one('product.product','Transport Type',required=True,domain = [('type','=','service')] )
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: