# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api

class hotel_service(models.Model):

    _name = "hotel.service"
    _description = "Hotel Service"

    hotel_information_id = fields.Many2one('hotel.information', 'hotel information')
    name = fields.Char('Description',required=True)
    service_id  = fields.Many2one('service.type','Service ',required=True)
    cost_price = fields.Float('Cost Price',required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.onchange("service_id")
    def onchange_price(self):
        for rec in self:
            rec.cost_price = rec.service_id.service_id.standard_price
            



            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: