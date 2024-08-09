# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields

class tour_destination_hotel_line(models.Model):

    _name = "tour.destination.hotel.line"
    _description = "Tour Destination Hotel Line"
    
    tour_id = fields.Many2one('tour.package', 'package')
    tour_destination_lines_id = fields.Many2one('tour.destination.line', 'Tour Destination Lines')
    hotel_type_id = fields.Many2one('hotel.type', 'Hotel Type', required=True)
    hotel_id = fields.Many2one('res.partner', 'Hotel Name', required=True)
    room_type_id = fields.Many2one('product.product', 'Room Type', required=True)
    name = fields.Boolean('Primary')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: