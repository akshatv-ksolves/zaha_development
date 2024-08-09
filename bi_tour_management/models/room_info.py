# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields , api

class room_info(models.Model):
	
    _name = "room.info"
    _description = "Room Info"

    hotel_information_id =fields.Many2one('hotel.information', 'hotel information')
    name = fields.Char('Description',required=True)
    room_type_id  = fields.Many2one('room.type','Room Type ',required=True)
    cost_price = fields.Float('Cost Price',required=True)
    sale_price = fields.Float('Sale Price',required=True)
    company_id = fields.Many2one(
        related='hotel_information_id.company_id',
        store=True, index=True, precompute=True)

    @api.onchange("room_type_id")
    def onchange_price(self):
        for rec in self:
            rec.cost_price = rec.room_type_id.room_type_id.standard_price
            rec.sale_price = rec.room_type_id.room_type_id.lst_price



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: