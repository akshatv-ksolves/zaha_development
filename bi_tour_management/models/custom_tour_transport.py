# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class custom_tour_transport(models.Model):

    _name = "custom.tour.transport"
    _description = "Custom Tour Transport"
    
    tour_preference_id = fields.Many2one('tour.preference','Tour Preference')
    name = fields.Selection([
        ('destination', 'Between Destinations'),
        ('site', 'Site Seeing')
        ],string="Destination", required=True)
    product_id = fields.Many2one("product.product",'Transport Type',domain = [('type','=','service')])
    travel_class_id = fields.Many2one("travel.class",'Travel Class',required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: