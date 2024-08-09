# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _

class hotel_planner_details(models.Model):

    _name = "hotel.planner.details"
    _description = "Hotel Planner Details"


    name = fields.Char("Sequence",required=True)
    destination_id = fields.Many2one("tour.destination",'Destination',required=True)
    hotel_type_id = fields.Many2one('hotel.type','Hotel Type',required=True)
    hotel_id = fields.Many2one('res.partner','Hotel',required=True,domain=[('is_hotel','=',True)])
    room_type_id = fields.Many2one("product.product",'Room Type',required=True,domain=[('type','=','service')])
    room_req = fields.Integer('Room Required')
    days = fields.Integer('No. Of Days To Stay')
    supplier_price = fields.Float('Supplier Rent / Night ')
    customer_price = fields.Float('Customer Rent / Night ')
    supplier_price_total = fields.Float('Total Supplier Price ')
    customer_price_total = fields.Float("Total Customer Price")
    pur_bol = fields.Boolean('Show Purchase Tax ')
    sale_tax_ids = fields.Many2many("account.tax","htl_planner_sale_ref",domain = [('type_tax_use','=','sale')])
    pur_tax_ids = fields.Many2many("account.tax","htl_planner_purchase_ref",domain = [('type_tax_use','=','purchase')])
    iternity_id = fields.Many2one("custom.tour.itinary",'Iternity Id')
    book_id = fields.Many2one("tour.booking")
    package_id = fields.Many2one("tour.package")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    hotel_pln_sale = fields.Float("Sale Amount",compute ="Onchnage_sale_hotel")
    hotel_pln_purchase = fields.Float("Purchase Amount",compute ="Onchange_purchase_hotel")

    sale_tax_amount_htl = fields.Float("Sale Tax Amount",compute="Onchnage_sale_hotel")
    purchse_tax_amount_htl = fields.Float("Purchse Tax Amount",compute="Onchange_purchase_hotel") 

    currency_id = fields.Many2one('res.currency', string='Currency')

    @api.onchange('room_type_id','pur_bol')
    def onchange_room_type(self):
        for rec in self:
            tax_ids = rec.room_type_id.taxes_id
            sale_tax_ids = rec.room_type_id.supplier_taxes_id
           
            if tax_ids:
                taxes = [tax.id for tax in tax_ids]
                rec.sale_tax_ids = [(6,0,taxes)]
            if sale_tax_ids:
                if rec.pur_bol:
                    pur_taxes = [tax.id for tax in sale_tax_ids]
                    rec.sale_tax_ids = [(6,0,pur_taxes)]
                else:
                    rec.sale_tax_ids = [(6,0,[])]

    @api.onchange("days","supplier_price","customer_price")
    def onchnage_days(self):
        for rec in self:
            rec.supplier_price_total = rec.days * rec.supplier_price
            rec.customer_price_total = rec.days * rec.customer_price

    @api.onchange("customer_price_total","sale_tax_ids")
    def Onchnage_sale_hotel(self):
        for sale_hotel in self:

            taxes_sale = sale_hotel.sale_tax_ids.compute_all(sale_hotel.customer_price_total)

            sale_hotel.hotel_pln_sale =taxes_sale['total_included']

            sale_hotel.sale_tax_amount_htl = sale_hotel.hotel_pln_sale - sale_hotel.customer_price_total

    @api.onchange("supplier_price_total","sale_tax_ids")
    def Onchange_purchase_hotel(self):
        for cost_hotel in self:
            
            taxes_pur =cost_hotel.sale_tax_ids.compute_all(cost_hotel.supplier_price_total)
        
            cost_hotel.hotel_pln_purchase =taxes_pur['total_included']

            cost_hotel.purchse_tax_amount_htl = cost_hotel.hotel_pln_purchase - cost_hotel.supplier_price_total

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: