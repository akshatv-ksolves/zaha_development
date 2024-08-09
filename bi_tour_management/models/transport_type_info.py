# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields, api, _

class transport_type_info(models.Model):
    
    _name = "transport.type.info"
    _description = "Transport Type Info"
    
    transport_info_id = fields.Many2one('transport.information','Transport Information')
    transport_carrier_id = fields.Many2one('transport.carrier','Carrier Name',required=True)
    transport_type_id = fields.Many2one('product.product',"Transport Type " , required=True)
    travel_class_id = fields.Many2one('travel.class',"Travel Class" , required=True)
    name = fields.Char("Description" ,required=True)
    from_dest_id=fields.Many2one('tour.destination','From',required=True)
    to_dest_id=fields.Many2one('tour.destination','To',required=True)
    from_date=fields.Date('From Date',required=True)
    to_date=fields.Date('To Date',required=True)
    cost_price=fields.Float('Cost Price(Adult)',required=True)
    cost_price_child=fields.Float('Cost Price(Child)',required=True)
    sale_price=fields.Float('Sale Price(Adult)',required=True)
    sale_price_child=fields.Float('Sale Price(Child)',required=True)
    company_id = fields.Many2one(
        related='transport_info_id.company_id',
        store=True, index=True, precompute=True)

    product_catagory_id = fields.Many2one("product.category",string="Catagory Id")


    @api.onchange('transport_carrier_id')
    def onchange_cata(self):
        pro_category = self.env["product.category"]
        product_catagory_id = pro_category.search([("name","=","Transport Service Type")])
        return {'domain' : {'transport_type_id' : [('type', '=', 'service'),('categ_id', '=', product_catagory_id.id)]}}

        
    @api.onchange('transport_type_id')
    def transport_onchange(self):
        for rec in self:
            rec.name = rec.transport_type_id.name

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: