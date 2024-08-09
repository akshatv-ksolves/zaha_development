# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields, api, _

class tour_cost_include_facility(models.Model):

    _name = "tour.cost.include.facility"
    _description = "Tour Cost Include Facility"
    
    tour_id = fields.Many2one('tour.package', 'Package')
    facility_id = fields.Many2one('tour.facility','Facility', required=True)
    name = fields.Char('Description', required=True)
    iternity_id = fields.Many2one("custom.tour.itinary",'Iternity Id')
    cost_include =fields.Float("Include Cost Price")
    book_id = fields.Many2one("tour.booking")
    company_id = fields.Many2one(
        related='facility_id.company_id',
        store=True, index=True, precompute=True)

    @api.onchange('facility_id')
    def onchange_facility(self):
        for rec in self:
            rec.name = rec.facility_id.desc

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: