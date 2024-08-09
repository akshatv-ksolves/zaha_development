# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError


class tour_package(models.Model):

    _name = "tour.package"
    _description = "Tour Package"

    name = fields.Char("Name",required=True)
    code = fields.Char("Tour Code")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    product_id = fields.Many2one('product.product', 'Tour Name', required=True)
    tour_type = fields.Selection([
        ('international', 'International'),
        ('domastic', 'Domastic')],
        string="Tour Type", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm')],
        string="state", default='draft') 
    days = fields.Integer(string="Days",required=True)
    current_date = fields.Date("Date of Publish",required=True)
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', readonly=True, help="Pricelist for current sales order.")
    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Currency", readonly=True)
    tour_intro = fields.Text("Tour Introduction")
    tour_date_lines = fields.One2many('tour.dates','tour_id', 'Tour Dates Line')
    tour_program_lines = fields.One2many('tour.program','tour_id', 'Tour Program Line')
    tour_destination_lines = fields.One2many('tour.destination.line','tour_id', 'Tour Program Lines')
    tour_cost_include_facility_lines = fields.One2many('tour.cost.include.facility','tour_id')
    tour_cost_exclude_facility_lines = fields.One2many('tour.cost.exclude.facility','tour_id')
    tour_road_travel_lines = fields.One2many('tour.road.travel','tour_id','Travel road lines')
    tour_hotel_info_lines = fields.One2many('tour.destination.hotel.line','tour_id', 'Tour Programme Line',compute ="_get_hotel_info")
    product_line_ids = fields.One2many('tour.package.product.line','tour_id', 'Package Product Line')
    subtotal = fields.Float('Sub Total',compute='_amount_all', readonly=True)
    tax_amt = fields.Float('Total Taxed Amount',compute='_amount_all', readonly=True)
    total_amt = fields.Float('Total Amount', compute='_amount_all', readonly=True)
    service_tour_ids = fields.One2many('tour.service.line.details','package_id','Others Services')
    site_costing_tour_ids = fields.One2many('sites.costing.line','package_id','Site Costing Lines')
    visa_costing_tour_ids =  fields.One2many('visa.costing.line','package_id','Visa Costing Lines')
    hotel_planer_tour_ids = fields.One2many('hotel.planner.details','package_id','Hotel Planer Details')
    travel_planer_tour_ids= fields.One2many('travel.planner.details','package_id','Travel Planer Details')

    write_cancel_policy = fields.Html(string="Write Cancellation Policy", store=True, readonly=False)
    write_term_condition = fields.Html(string="Write Terms and Conditions", store=True, readonly=False)

    @api.depends('tour_destination_lines')
    def _get_hotel_info(self):

        for line in self :
            hotel_list = []
            for hotel in line.tour_destination_lines :
                for res in hotel.hotel_line_ids :
                    hotel_list.append(res.id)

            line.update({'tour_hotel_info_lines' : [(6,0,hotel_list)]})

    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            rec.name = rec.product_id.name

    def button_dummy(self):
        return True

    def button_confirm(self):
        for rec in self:
            if not rec.tour_date_lines:
                raise UserError("Fill Tour Dates Details") 
            if not rec.tour_program_lines:
                raise UserError("Fill Tour Programme  Details") 
            if not rec.tour_destination_lines:
                raise UserError ("Fill Tour Destinations Details") 
            if not rec.tour_cost_include_facility_lines:
                raise UserError ("Fill Tour Include Facilities Details") 
            if not rec.tour_cost_exclude_facility_lines:
                raise UserError ("Fill Tour Exclude Facilities Details") 
            if not rec.tour_road_travel_lines:
                raise ValidationError('Fill Tour Transport details')
            rec.state = "confirm"

    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for tour in self:
            subtotal = tax_amt = 0.0
            for line in tour.product_line_ids:
                subtotal += line.price_subtotal
                tax_amt += line.price_tax
                self.subtotal = subtotal
                self.tax_amt = tax_amt
                self.total_amt =  subtotal + tax_amt

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: