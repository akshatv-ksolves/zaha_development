# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _

class custom_tour_destination(models.Model):
	
    _name = "custom.tour.destination"
    _description = "Custom Tour Destination"
    
    tour_preference_id = fields.Many2one('tour.preference','Tour Preference')
    name = fields.Char("No. Of Nights ",required=True)
    tour_destination_id = fields.Many2one('tour.destination','Destination')
    country_id = fields.Many2one('res.country','Country')
    site_line_ids = fields.One2many('custom.tour.sites','custom_tour_dest_id')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    @api.onchange('tour_destination_id')
    def oncahnge_destination_id(self):
        for rec in self:
            if rec.tour_destination_id:
                rec.country_id = rec.tour_destination_id.country_id.id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: