# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _

class tour_service_line_details(models.Model):

    _name = "tour.service.line.details"
    _description = "Tour Service Line Details"

    product_id = fields.Many2one("product.product",'Product',required=True)
    sale_price = fields.Float('Sale Price',required=True)
    price_unit = fields.Float('Cost Price')
    product_uom_qty = fields.Float('Quantity(UOM)',required=True)
    product_uom_id = fields.Many2one("uom.uom",'Unit Of Measure',required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
   
    price_subtotal_cost = fields.Float('Cost Subtotal ',readonly=True,compute="onchange_quantity")
    price_subtotal = fields.Float('Sale Subtotal ',readonly=True,compute="onchange_quantity")
    
    discount = fields.Float('Discount ')
    pur_bol = fields.Boolean('Show Purchase Tax ')
    sale_tax_ids = fields.Many2many("account.tax",domain = [('type_tax_use','=','sale')])
    pur_tax_ids = fields.Many2many("account.tax","other_service_purchase_ref",domain = [('type_tax_use','=','purchase')])
    iternity_id = fields.Many2one("custom.tour.itinary",'Iternity Id')
    package_id = fields.Many2one("tour.package","Package Id")
    book_id = fields.Many2one("tour.booking")

    sale_tour_service = fields.Float("Sale Amount", compute="Onchnage_sale_tour")
    pur_tour_service = fields.Float("Purchase Amount",compute="Onchange_purchase_tour")

    sale_tax_amount_tour = fields.Float("Sale Tax Amount",compute="Onchnage_sale_tour")
    purchse_tax_amount_tour = fields.Float("Purchse Tax Amount",compute="Onchange_purchase_tour") 

    currency_id = fields.Many2one('res.currency', string='Currency')  

    @api.onchange('product_id')
    def onchange_product(self):
        for rec in self:
            tax_ids = rec.product_id.taxes_id
            sale_tax_ids = rec.product_id.supplier_taxes_id
           
            if tax_ids:
                taxes = [tax.id for tax in tax_ids]
                rec.sale_tax_ids = [(6,0,taxes)]
            if sale_tax_ids:
                if rec.pur_bol:
                    pur_taxes = [tax.id for tax in sale_tax_ids]
                    rec.sale_tax_ids = [(6,0,pur_taxes)]
                else:
                    rec.sale_tax_ids = [(6,0,[])]
            rec.product_uom_qty = 1.0
            rec.product_uom_id = rec.product_id.uom_id.id
            rec.sale_price = rec.product_id.lst_price
            rec.price_unit = rec.product_id.standard_price
            rec.onchange_quantity()


    @api.onchange('product_id','product_uom_qty')
    def onchange_quantity(self):
        for cqty in self:
            cqty.price_subtotal_cost = cqty.price_unit * cqty.product_uom_qty
            cqty.price_subtotal = cqty.sale_price * cqty.product_uom_qty
        

    @api.onchange("sale_price","sale_tax_ids","price_subtotal","product_id")
    def Onchnage_sale_tour(self):

        for sale_to in self:
            taxes_sale = sale_to.sale_tax_ids.compute_all(sale_to.price_subtotal)
            
            sale_to.sale_tour_service =taxes_sale['total_included']

            sale_to.sale_tax_amount_tour = sale_to.sale_tour_service - sale_to.price_subtotal 

    @api.onchange("price_subtotal_cost","pur_tax_ids","price_unit","product_id")
    def Onchange_purchase_tour(self):
        for cost_to in self:
            
            taxes_pur =cost_to.pur_tax_ids.compute_all(cost_to.price_subtotal_cost)
            cost_to.pur_tour_service =taxes_pur['total_included']

            cost_to.purchse_tax_amount_tour =cost_to.pur_tour_service - cost_to.price_subtotal_cost
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: