# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp


class travel_planner_details(models.Model):
    
    _name = "travel.planner.details"
    _description = "Travel Planner Details"

    name = fields.Char("Sequence",required=True)
    transport_id = fields.Many2one("transport.information",'Transport Company',required=True)
    date = fields.Date('Booking Date',required=True)
    transport_carrier_id = fields.Many2one('transport.carrier','Carrier Name',required=True)
    transport_type_id = fields.Many2one("product.product",'Transport Type',required=True,domain = [('type','=','service')])
    travel_class_id = fields.Many2one('travel.class', 'Travel Class',required=True )
    from_dest_id = fields.Many2one("tour.destination",'From',required=True)
    to_dest_id = fields.Many2one("tour.destination",'To',required=True)
    cost_price_adult = fields.Float('Cost Price (Adult) ')
    sale_price_adult = fields.Float('Sale Price (Adult) ')
    cost_price_child = fields.Float('Cost Price (Child) ')
    sale_price_child = fields.Float('Sale Price (Child) ')
    total_cost_price_adult = fields.Float('Total Cost Price (Adult)')
    total_sale_price_adult = fields.Float('Total Sale Price (Adult)')
    total_cost_price_child = fields.Float('Total Cost Price (Child)')
    total_sale_price_child = fields.Float('Total Sale Price (Child)')
    pur_bol = fields.Boolean('Show Purchase Tax ')
    sale_tax_ids = fields.Many2many("account.tax",string = "Sale Taxes" ,domain = [('type_tax_use','=','sale')])
    pur_tax_ids = fields.Many2many("account.tax","travel_planner_purchase_ref",domain = [('type_tax_use','=','purchase')])
    iternity_id = fields.Many2one("custom.tour.itinary",'Iternity Id')
    total_sale_amount = fields.Float(compute='Onchange_sale_tax')
    total_purchase_amount = fields.Float(compute='Onchange_purchase_tax')
    book_id = fields.Many2one("tour.booking")
    package_id = fields.Many2one("tour.package")
    company_id = fields.Many2one(
        related='transport_id.company_id',
        store=True, index=True, precompute=True)
    sale_amount = fields.Float(compute='Onchange_sale_tax', string='Sale Amount')
    purchase_amount = fields.Float(compute='Onchange_purchase_tax', string='Purchase Amount')

    sale_tax_amt_travel = fields.Float(compute="Onchange_sale_tax",string="Sale Tax Amount")
    pur_tax_amt_travel = fields.Float(compute="Onchange_purchase_tax",string="Purchase Tax Amount")

    currency_id = fields.Many2one('res.currency', string='Currency')

    @api.onchange('cost_price_adult','cost_price_child','sale_price_adult','sale_price_child')
    def onchnage_price(self):
        for rec in self:
            if rec.iternity_id:
                rec.total_cost_price_adult = rec.cost_price_adult * rec.iternity_id.adult
                rec.total_sale_price_adult = rec.sale_price_adult * rec.iternity_id.adult
                rec.total_cost_price_child = rec.cost_price_child * rec.iternity_id.child
                rec.total_sale_price_child = rec.sale_price_child * rec.iternity_id.child

    @api.onchange('cost_price_adult','cost_price_child','sale_price_adult','sale_price_child')
    def onchnage_package(self):
        for rec in self:
            if rec.book_id:
                rec.total_cost_price_adult = rec.cost_price_adult * rec.book_id.adult
                rec.total_sale_price_adult = rec.sale_price_adult * rec.book_id.adult
                rec.total_cost_price_child = rec.cost_price_child * rec.book_id.child
                rec.total_sale_price_child = rec.sale_price_child * rec.book_id.child

    @api.onchange("sale_tax_ids","total_sale_price_adult","total_sale_price_child")
    def Onchange_sale_tax(self):
        for sale_travel in self:

            sale_travel.total_sale_amount = sale_travel.total_sale_price_adult + sale_travel.total_sale_price_child 
            taxes_sale = sale_travel.sale_tax_ids.compute_all(sale_travel.total_sale_amount)
            
            sale_travel.sale_amount =taxes_sale['total_included']

            sale_travel.sale_tax_amt_travel = sale_travel.sale_amount - sale_travel.total_sale_amount
            

    @api.onchange("sale_tax_ids","total_cost_price_adult","total_cost_price_child")
    def Onchange_purchase_tax(self):
        for cost_travel in self:
            
            cost_travel.total_purchase_amount = cost_travel.total_cost_price_adult + cost_travel.total_cost_price_child
            taxes_pur =cost_travel.sale_tax_ids.compute_all(cost_travel.total_purchase_amount)
        
            cost_travel.purchase_amount =taxes_pur['total_included']

            cost_travel.pur_tax_amt_travel = cost_travel.purchase_amount - cost_travel.total_purchase_amount

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: