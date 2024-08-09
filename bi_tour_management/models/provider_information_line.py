# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields
    
class provider_information_line(models.Model):
	
    _name = "provider.information.line"
    _description = "Provider Information Line"

    travel_id=fields.Many2one('tour.road.travel','travel information')
    provider_id = fields.Many2one('transport.information','Service Providers')
    transport_carrier_id = fields.Many2one('transport.carrier','Service Provider')
    name = fields.Boolean("primary")
    company_id = fields.Many2one(
        related='provider_id.company_id',
        store=True, index=True, precompute=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: