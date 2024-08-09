# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _

class tour_destination_line(models.Model):

    _name = "tour.destination.line"
    _description = "Tour Destination Line"

    tour_id = fields.Many2one('tour.package', 'package')
    iternity_id = fields.Many2one("custom.tour.itinary",'Iternity Id')
    destination_id = fields.Many2one('tour.destination', 'Destinations', required=True)
    country_id = fields.Many2one('res.country', 'Country', required=True)
    nights = fields.Char('No. Of Nights')
    visa_chk = fields.Boolean('Is Visa Required')
    book_id =fields.Many2one("tour.booking")
    visa_type = fields.Selection([
        ('Tourist Visa(single Entry)', 'Tourist Visa(single Entry)'),
        ('Tourist Visa(multiple Entry)', 'Tourist Visa(multiple Entry)')],
        string="Visa Type")
    hotel_line_ids = fields.One2many('tour.destination.hotel.line','tour_destination_lines_id', 'Tour Programme Line')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    @api.onchange('destination_id')
    def onchange_destination(self):
        for rec in self:
            rec.country_id = rec.destination_id.country_id.id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: