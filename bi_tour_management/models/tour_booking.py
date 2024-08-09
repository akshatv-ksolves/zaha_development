# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
import uuid
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import date
import dateutil.parser


class tour_booking(models.Model):

	_name = "tour.booking"
	_inherit = 'mail.thread'
	_description = "Tour Booking"

	@api.model
	def _default_access_token(self):
		return uuid.uuid4().hex

	state = fields.Selection([
			('draft', 'Draft'),
			('confirm', 'Confirm'),
			('in_process', 'In Process'),
			('booked', 'Booked'),
			('invoiced', 'invoiced'),
			('done', 'Done'),
			('cancel', 'Cancel')
			], string="Status", readonly=True, default="draft")
	name = fields.Char("Tour Booking Id" , readonly=True)
	current_date = fields.Date("Booking Date" , required=True, default=fields.date.today())
	customer_id = fields.Many2one('res.partner', 'Customer',required=True)
	email_id = fields.Char("Email Id",required=True)
	mobile1 = fields.Char("Mobile Number" , required=True)
	adult = fields.Integer("Adult Persons")
	child = fields.Integer("Child")
	via = fields.Selection([
			('direct', 'Direct'),
			('agent', 'Agent')
			], default="direct", required=True) 
	agent_id = fields.Many2one('res.partner', 'Agent')
	pricelist_id = fields.Many2one('res.currency', 'Currency')
	tour_type = fields.Selection([
			('international', 'International'),
			('domastic', 'Domastic')],
			string="Tour Type", required=True)
	season_id = fields.Many2one('tour.season', "Season" , required=True)
	tour_id = fields.Many2one('tour.package', 'Tour',required=True)
	tour_dates_id = fields.Many2one('tour.dates', "Tour Dates" , required=True)
	payment_policy_id = fields.Many2one('tour.payment.policy', "Payment Policy" , required=True)
	itinary_id = fields.Many2one('custom.tour.itinary', "Itinerary Id")
	commission_compute = fields.Char("Commission")
	tour_customer_ids = fields.One2many('tour.customer.details', 'book_id', "Tour Customer",)
	insurance_line_ids = fields.One2many('insurance.policy', 'book_id', "Services",)

	subtotal = fields.Float('Sub Total', compute='_count_amount_sale' , readonly=True)
	tax_amt = fields.Float('Total Taxed Amount' ,compute="_count_amount_sale" , readonly=True)
	total_insurance_amt = fields.Float('Insuarance Amount', readonly=True)
	total_amt = fields.Float('Total Amount',compute="_count_amount_sale", readonly=True)
	t_id = fields.Many2one('tour.cancellation')
	sale_order_count = fields.Integer("Quotation", compute="_Sale_quot_count")
	invoice_count = fields.Integer("Invoice",compute="_Invoice_count")
	company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
	mail_bool = fields.Boolean("email check Boolean" , default=False)

	tour_program_book_ids = fields.One2many('tour.program','book_id','Tour Program Lines')
	tour_destination_book_ids = fields.One2many('tour.destination.line','book_id','Tour Destination Line')
	itinary_cost_include_book_lines = fields.One2many('tour.cost.include.facility','book_id','Itinary Cost Include Facility Lines')
	itinary_cost_exclude_book_lines=  fields.One2many('tour.cost.exclude.facility','book_id','Itinary Cost Exclude Facility Lines')
	sites_costing_book_ids = fields.One2many('sites.costing.line','book_id','Site Costing Lines')
	visa_costing_book_ids =  fields.One2many('visa.costing.line','book_id','Visa Costing Lines')
	hotel_planer_book_ids = fields.One2many('hotel.planner.details','book_id','Hotel Details')
	travel_planer_book_ids= fields.One2many('travel.planner.details','book_id','Travel Details')
	product_line_ids = fields.One2many('tour.package.product.line', 'book_id', 'Package Product Line')
	service_book_ids = fields.One2many('tour.service.line.details','book_id','Others Services')
	access_token = fields.Char("Security Token", default=_default_access_token)
	tour_selection = fields.Selection([
									('Tour1', 'Created Tour'),
									('Tour2', 'Itinerary Tour'),],
									help="Selectionany one Tour type.",string="Select Tour")

	currency_id = fields.Many2one('res.currency', string='Currency')

	@api.onchange('tour_id')
	def _onchange_tour_selection(self):

		for rec in self:

			if rec.tour_id:
																	
				program_list = []
				for pro_lines in rec.tour_id.tour_program_lines:
					program_list.append(pro_lines.id)
				rec.tour_program_book_ids = [(6, 0, program_list)]

				destination_list = []
				for des_line in rec.tour_id.tour_destination_lines:
					destination_list.append(des_line.id)
				rec.tour_destination_book_ids = [(6, 0, destination_list)]

				cost_include_list = []
				for cost_include in rec.tour_id.tour_cost_include_facility_lines:
					cost_include_list.append(cost_include.id)
				rec.itinary_cost_include_book_lines = [(6, 0, cost_include_list)]

				cost_exclude_list = []
				for cost_exclude in rec.tour_id.tour_cost_exclude_facility_lines:
					cost_exclude_list.append(cost_exclude.id)
				rec.itinary_cost_exclude_book_lines = [(6, 0, cost_exclude_list)]

				site_list = []
				for site_lines in rec.tour_id.site_costing_tour_ids:
					site_list.append(site_lines.id)
				rec.sites_costing_book_ids = [(6, 0, site_list)]

				visa_list = []
				for visa_lines in rec.tour_id.visa_costing_tour_ids:
					visa_list.append(visa_lines.id)
				rec.visa_costing_book_ids = [(6, 0, visa_list)]

				hotel_list = []
				for hotel_lines in rec.tour_id.hotel_planer_tour_ids:
					hotel_list.append(hotel_lines.id)
				rec.hotel_planer_book_ids = [(6, 0, hotel_list)]

				travel_list = []
				for travel_lines in rec.tour_id.travel_planer_tour_ids:
					travel_list.append(travel_lines.id)
				rec.travel_planer_book_ids = [(6, 0, travel_list)]

				service_list = []
				for service in rec.tour_id.service_tour_ids:
					service_list.append(service.id)
				rec.service_book_ids = [(6, 0, service_list)]


	@api.onchange('adult','child')
	def _Onchnage_person(self):
		for rec in self:
			for i in rec.travel_planer_book_ids:
				i.total_sale_price_child = rec.child * i.sale_price_child
				i.total_sale_price_adult = rec.adult * i.sale_price_adult

	def _count_amount_sale(self):

		sub_tot = 0.0
		tax_sub_tot = 0.0
		insuran_sub_tot = 0.0

		for i in self:
			for tour_prog in i.tour_program_book_ids:
				sub_tot += tour_prog.expected_line_sale

			for site_cost in i.sites_costing_book_ids:
				sub_tot += site_cost.total_sale_price
																			
			for service in i.service_book_ids:
				sub_tot += service.price_subtotal
				tax_sub_tot += service.sale_tax_amount_tour

			for visa_cost in i.visa_costing_book_ids:
				sub_tot +=visa_cost.total_sale_price
				tax_sub_tot += visa_cost.sale_tax_amount_visa

			for hotel_planner in i.hotel_planer_book_ids:
				sub_tot += hotel_planner.customer_price_total
				tax_sub_tot += hotel_planner.sale_tax_amount_htl

			for travel_planner in i.travel_planer_book_ids:
				sub_tot += travel_planner.total_sale_amount
				tax_sub_tot += travel_planner.sale_tax_amt_travel

			for insurance in i.insurance_line_ids:
				sub_tot += insurance.total_cost

			i.subtotal = sub_tot
			i.tax_amt = tax_sub_tot

			i.total_amt = i.subtotal + i.tax_amt



	def check_availability(self):
		for rec in self:
			if (len(rec.tour_customer_ids)) < (rec.adult + rec.child):
				raise UserError('Customer Record Missing.')
			elif rec.tour_id.state == 'draft':
				raise UserError('There is no tour available in that season')
			else:
				rec.state = 'confirm'

	def create_order(self):   
		for rec in self:
			currency_price_list = self.env['product.pricelist'].search(['|',('currency_id','=',rec.pricelist_id.id),('company_id','=',self.env.user.company_id.id)])
			if currency_price_list:
				if rec.tour_id:
					order_obj = rec.env['sale.order']
					tax_ids = [tax.id for tax in rec.tour_id.product_id.taxes_id]
					vals = {
					'tour_book_id' : rec.id,
					'partner_id':rec.customer_id.id,
					'partner_shipping_id':rec.customer_id.id,
					'partner_invoice_id':rec.customer_id.id,
					'pricelist_id':rec.customer_id.property_product_pricelist.id or currency_price_list[0].id,
					'order_line' : [(0, 0, {
							'product_id':rec.tour_id.product_id.id,
							'name':rec.tour_id.product_id.name,
							'product_uom_qty':1,
							'product_uom':1,
							'price_unit':rec.total_amt,
										})],
					'origin':rec.name
					}
					res = order_obj.create(vals) 
					rec.t_id.tour_sale_order_ids = [(6, 0, [res.id])]
					rec.state = 'in_process'
					return res

			if rec.tour_selection == "Tour2":
				order_obj = rec.env['sale.order']
				vals = {
					'tour_book_id' : rec.id,
					'partner_id':rec.customer_id.id,
					'partner_shipping_id':rec.customer_id.id,
					'partner_invoice_id':rec.customer_id.id,
					'pricelist_id': rec.customer_id.property_product_pricelist.id or currency_price_list[0].id,
					'order_line' : [(0, 0, {
						'product_id':rec.itinary_id.product_itinary_id.id,
						'name':rec.itinary_id.product_itinary_id.name,
						'product_uom_qty':1,
						'product_uom':1,
						'price_unit':rec.total_amt,
					})],
					'origin':rec.name
				}
				res = order_obj.create(vals)
				rec.t_id.tour_sale_order_ids = [(6, 0, [res.id])]
				rec.state = 'in_process'
				return res


			else:
				raise UserError(_('No Pricelist for this currency!'))

	def _Sale_quot_count(self):
		for sale_quot in self:
			sale_order_ids = self.env["sale.order"].search([('tour_book_id','=',sale_quot.id)])
			sale_quot.sale_order_count = len(sale_order_ids)

	def button_count_quotation(self):

		self.ensure_one()
		return {
			'name': 'Quotation',
			'type': 'ir.actions.act_window',
			'view_mode': 'kanban,tree,form',
			'res_model': 'sale.order',
			'domain': [("tour_book_id",'=',self.id)],
		}

	def get_invoices(self):
		for invoi_count in self:
			order = self.env["sale.order"].search([('tour_book_id','=',invoi_count.id)])
			invoices = order.order_line.invoice_lines.move_id.filtered(lambda r: r.move_type in ('out_invoice', 'out_refund'))
			if invoi_count.t_id.tour_sale_order_ids.name != False:
				invoice_order_ids = self.env["account.move"].search([('origin','=',invoi_count.t_id.tour_sale_order_ids.name)])
				invoices = invoices + invoice_order_ids
		return invoices


	def _Invoice_count(self):
		for invoi_count in self:
			invoi_count.invoice_count = len(invoi_count.get_invoices())


	def button_count_invoice(self):
		self.ensure_one()
		invoices = self.get_invoices()
		return {
			'name': 'Invoice',
			'type': 'ir.actions.act_window',
			'view_mode': 'kanban,tree,form',
			'res_model': 'account.move',
			'domain': [('id','in',invoices.ids)],
		}

	def action_done(self):
		for rec in self:
			transport_obj = self.env['transport.booking'].search([('tour_book_id', '=', rec.id)])
			rec.state = 'done'

	def cancel_tour_book(self):
		for rec in self:
			if rec.t_id.tour_sale_order_ids.state == "sale" :
				raise ValidationError(_('Cannot Cancel Tour Booking once Quotation is confirmed.!'))
			else:
				rec.state = "cancel" 

	def confirm_booking(self):
		self.ensure_one()
		cust_line_list = []
		visa_obj = self.env['visa.booking']
		sale_obj = self.env['sale.order']
		hotel_obj = self.env['tour.hotel.reservation']
		passport_obj = self.env['passport.booking']
		transport_obj = self.env['transport.booking']
		ids = sale_obj.search([('tour_book_id', '=', self.id)])
		total = self.adult + self.child
		if total > self.tour_dates_id.available_date:
			raise  UserError('NO SEATS ARE AVAILABLE, TOUR IS ALREADY BOOKED')

			
		if self.tour_id:
			if self.tour_id.tour_date_lines:
				for line in self.tour_id.tour_date_lines:
					if line.state != 'available':
						raise  UserError('TOUR IS NOT AVAILABLE FOR THIS SEASON')
		for each in ids:
			if each.state != 'sale':
				raise  UserError('First Confirm Sale order')
			else:
				for line in self.tour_customer_ids:
					cust_line_list.append(line.id)
					line.t_flag = True
					if line.p_flag:
						value = {
							   'customer_id':line.partner_id.id,
							   'current_date' : self.current_date,
							   'email_id': line.partner_id.email,
							   'mobile': line.partner_id.mobile,
							   'product_id': self.env['product.product'].search([('name', '=', 'Passport')]).id,
							   'scheme_id' : self.env['service.scheme'].search([('name', '=', 'Regular')]).id,
							   'service_charge':self.env['service.scheme'].search([('name', '=', 'Regular')]).service_cost,
							   }
						pass_res = passport_obj.create(value)

		for line in self.hotel_planer_book_ids:
			for rec in self.tour_destination_book_ids:
				destination_id=rec.destination_id
			
			vals = {
				  'current_date' : self.current_date,
				  'customer_id' : self.customer_id.id,
				  'email_id':self.email_id,
				  'mobile':self.mobile1,
				  'child':self.child,
				  'adult':self.adult,
				  'pricelist_id':self.pricelist_id.id,
				  'room_required':line.room_req,
				  'hotel_rent':line.customer_price,
				  'hotel_type_id' : line.hotel_type_id.id,
				  'hotel_id' : line.hotel_id.id,
				  'room_type_id':line.room_type_id.id,
				  'tour_id' : self.tour_id.id,
				  'tour_date_id': self.tour_dates_id.id,
				  'tour_book_id' : self.id,
				  'destination_id':destination_id.id,
				  'tour_customer_ids':[(6, 0, cust_line_list)]
				}
			res = hotel_obj.create(vals)

						  
		for line in self.tour_id.tour_road_travel_lines:
			transport_type_id = line.transport_type_id.id
			travel_class_id = line.travel_class_id.id
			from_dest_id = line.from_dest_id.id
			to_dest_id = line.to_dest_id.id
			for provider in line.provider_ids:
				if provider.name:
					provider_id = provider.provider_id.id
					carrier_id = provider.transport_carrier_id.id
					vals = {
						  'current_date' : self.current_date,
						  'customer_id' : self.customer_id.id,
						  'email_id':self.email_id,
						  'checkin_date':self.tour_dates_id.start_date, 
						  'mobile':self.mobile1,
						  'child':self.child,
						  'adult':self.adult,
						  'transport_id' : provider_id,
						  'transport_carrier_id' : carrier_id,
						  'tour_date_id': self.tour_dates_id.id,
						  'transport_type_id':transport_type_id,
						  'travel_class_id' : travel_class_id,
						  'from_destination_id': from_dest_id,
						  'to_destination_id' : to_dest_id,
						  'tour_id':self.tour_id.id,
						  'tour_book_id' : self.id,
						  'customer_line_ids':[(6, 0, cust_line_list)],
                          'pricelist_id': self.pricelist_id.id,
							}
					res = transport_obj.create(vals)

			  
		for line in self.tour_id.tour_destination_lines:
			for line_ids in line.hotel_line_ids:
				if line_ids.name:
					vals = {
						  'current_date' : self.current_date,
						  'customer_id' : self.customer_id.id,
						  'email_id':self.email_id,
						  'mobile':self.mobile1,
						  'child':self.child,
						  'adult':self.adult,
						  'hotel_type_id' : line_ids.hotel_type_id.id,
						  'hotel_id' : line_ids.hotel_id.id,
						  'room_type_id':line_ids.room_type_id.id,
						  'tour_id' : self.tour_id.id,
						  'tour_date_id': self.tour_dates_id.id,
						  'tour_book_id' : self.id,
						  'tour_customer_ids':[(6, 0, cust_line_list)]
						  }
					res = hotel_obj.create(vals)
				
			if not line.visa_chk:
				for visa_line in self.visa_costing_book_ids:

					if line.visa_type == 'Tourist Visa(Single Entry)':
						visa = 'Tourist Visa(Single Entry)'
					elif line.visa_type == 'Tourist Visa(Multiple Entry)':
						visa = 'Tourist Visa(Multiple Entry)'
					vals = {
						  'current_date' : self.current_date,
						  'customer_id' : self.customer_id.id,
						  'email_id':self.customer_id.email,
						  'mobile':self.customer_id.mobile,
						  'country_id':line.country_id.id,
						  'product_id' : self.env['product.product'].search([('name', '=', 'Visa')]).id,
						  'service_charge':visa_line.sale_price,
						  'tour_id' : self.tour_id.id,
						  'tour_date': self.tour_dates_id.start_date,
						  'tour_book_id' : self.id,
						  }
					res = visa_obj.create(vals)
			self.state = 'booked'

	@api.constrains('adult','child')
	def Check_person(self):
		for rec in self:
			if  rec.adult <= 0 and rec.child <= 0:
				raise UserError('Please Enter Person number')
																
	@api.model
	def create(self, vals):

		if self._context.get('resource') == 'custom':
			vals['name'] = self.env['ir.sequence'].get('tour.booking.custom') or '/'
		else:
			vals['name'] = self.env['ir.sequence'].get('tour.booking') or '/'

		res = super(tour_booking, self).create(vals)
		
		for line in res.product_line_ids:
			line.update({'book_id':res.id})
		return res

	def write(self, vals):
												
		if vals.get('insurance_line_ids'):
			total_adult = 0.0
			total_child = 0.0
																		
		return super(tour_booking, self).write(vals)



	@api.onchange('tour_id')
	def tour_id_onchange(self):
		for rec in self:
			product_lines = []
			if rec.tour_id:
				for line in rec.tour_id.product_line_ids:
					product_lines.append(line.id)
				rec.product_line_ids = [(6, 0, product_lines)]             
			else:
				rec.product_line_ids = [(6, 0, [])]
																
	@api.onchange('customer_id')
	def partner_id_onchange(self):
		for rec in self:
			if rec.customer_id:
				rec.email_id = rec.customer_id.email
				rec.mobile1 = rec.customer_id.mobile

	def send_review_reminder_emails(self):
		complete_bookings = self.search([('state', '=', 'done'), ('mail_bool', '=', False)])
		template = self.env.ref(
            'bi_tour_management.rating_tour_request_email_template', raise_if_not_found=False)
		
		if complete_bookings and template:
			for record in complete_bookings:
				mail = template.send_mail(int(record.id))
				if mail:
					mail_id = self.env['mail.mail'].browse(mail)
					mail_id.sudo().send()
					record.write({'mail_bool': True})
																	

	# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
