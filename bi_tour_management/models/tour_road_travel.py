# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields

class tour_road_travel(models.Model):

    _name = "tour.road.travel"
    _description = "Tour Road Travel"

    tour_id = fields.Many2one('tour.package', 'package')
    from_dest_id=fields.Many2one('tour.destination','From')
    to_dest_id=fields.Many2one('tour.destination','To')
    transport_type_id=fields.Many2one('product.product','Transport Type')
    travel_class_id =fields.Many2one('travel.class','Travel Class')
    name = fields.Char('Distance In KM')
    approx_time = fields.Float('Time(Hrs)')
    provider_ids = fields.One2many('provider.information.line','travel_id','Provider Information')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: