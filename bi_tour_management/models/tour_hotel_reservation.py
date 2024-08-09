# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _
import datetime
from odoo.exceptions import UserError,ValidationError

class tour_hotel_reservation(models.Model):

		_name = "tour.hotel.reservation"
		_description = "Tour Hotel Reservation"

		name = fields.Char("Registration ID ",readonly=True)
		state = fields.Selection([
				('draft', 'Draft'),
				('confirm', 'Confirm'),
				('approve','Approved'),
				('book', 'Booked'),
				('issue', 'Ticket Issue'),
				('done', 'Done'),
				('cancel', 'Cancel'),
				],
				string="Status", default="draft")
		current_date = fields.Date("Date ",required=True)
		customer_id = fields.Many2one('res.partner','Customer',required=True)
		email_id = fields.Char("Email Id")
		mobile = fields.Char("Mobile Number",required=True)
		adult = fields.Integer("Adult Persons")
		child = fields.Integer("Child")
		pricelist_id = fields.Many2one('res.currency',"currency")
		hotel_type_id= fields.Many2one('hotel.type','Hotel Type',required=True)
		hotel_id = fields.Many2one('res.partner','Hotel ',required=True)
		room_type_id = fields.Many2one('product.product','Room Type',required=True)
		room_rent = fields.Float('Cost Price')
		hotel_rent = fields.Float('Sale Price')
		checkin_date = fields.Date('Check In Date')
		checkout_date = fields.Date('Check Out Date')
		room_required = fields.Integer('Rooms Required')
		no_of_days = fields.Float('No. Of Days',readonly=True)
		tour_id = fields.Many2one('tour.package','Tour')
		tour_date_id = fields.Many2one('tour.dates','Tour Start Date')
		tour_book_id = fields.Many2one('tour.booking','Tour Booking Ref')
		destination_id = fields.Many2one('tour.destination','Tour Destination')
		tour_customer_ids = fields.One2many('tour.customer.details','hotel_book_id','Tour-Destination')
		tax_ids = fields.Many2many('account.tax','hotel_reservation_account_tax_rel','res_id','tax_id')
		hotel_room_reserve_invoice_ids = fields.Many2many('account.move','hotel_room_reserve_invoice_rel','reserv_id','inv_id')
		hotel_room_reserve_supplier_invoice_ids = fields.Many2many('account.move','hotel_room_reserve_supply_invoice_rel','ress_id','sup_inv_id')
		untax_amt = fields.Float('Untaxed Amt',compute='_amount_all',readonly=True)
		tax_amt = fields.Float('Taxes ',readonly=True)
		total_amt = fields.Float('Customer Invoice Amt',compute='_amount_all',readonly=True)
		hotel_invoice_amt = fields.Float('Hotel Invoice Amt',compute='_amount_all',readonly=True)

		invoice_count = fields.Integer("Invoice",compute="_Invoice_count")
		company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)


		@api.constrains('checkin_date')
		def check_checkin_date(self):
			for rec in self:
				if rec.checkin_date and rec.checkout_date and rec.checkin_date > rec.checkout_date:
					raise ValidationError("Checkin Date Can not Greater than Check Out Date.")
				if not rec.checkin_date:
					raise ValidationError("Check In Date Is Not Set.")

		@api.constrains('checkout_date')
		def check_checkout_date(self):
			for rec in self:
				if rec.checkin_date and rec.checkout_date and rec.checkout_date < rec.checkin_date:
					raise ValidationError("Check Out Date Can not Less than Checkin Date.")
				if not rec.checkout_date:
					raise ValidationError("Check Out Date Is Not Set.")

		@api.model
		def create(self,vals):
			vals['name'] = self.env['ir.sequence'].get('hotel.booking') or '/'
			res = super(tour_hotel_reservation, self).create(vals)
			return res

		def make_done(self):
			for rec in self:
				rec.state="done"
		
		def _amount_all(self):
			for rec in self:
				tax = 0.0
				rec.untax_amt = rec.hotel_rent * rec.no_of_days * rec.room_required
				if rec.tax_ids :
						tax = sum(line.amount for line in rec.tax_ids)
				rec.tax_amt = tax
				rec.total_amt = rec.untax_amt  + tax
				rec.hotel_invoice_amt = rec.room_rent * rec.no_of_days * rec.room_required
				if rec.tax_ids :+ tax
		
		def make_confirm(self):
			for rec in self:
				if (len(rec.tour_customer_ids))<(rec.adult+rec.child):
					raise UserError('Customer Record Missing.')
				else:
					rec.state = 'confirm'

		def send_to_hotel(self):
			self.ensure_one()
			ir_model_data = self.env['ir.model.data']
			template_id = ir_model_data._xmlid_lookup('bi_tour_management.email_template_hotel_edi')[1]
			compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[1]
			

			ctx = {
				'default_model': 'tour.hotel.reservation',
				'default_res_ids': self.ids,
				'default_use_template': bool(template_id),
				'default_template_id': template_id,
				'default_composition_mode': 'comment',
				'mark_so_as_sent': True,
				'force_email': True
			}
			return {
				'type': 'ir.actions.act_window',
				'view_type': 'form',
				'view_mode': 'form',
				'res_model': 'mail.compose.message',
				'views': [(compose_form_id, 'form')],
				'view_id': compose_form_id,
				'target': 'new',
				'context': ctx,
			}

		def button_cancel(self):
			for rec in self:
				rec.state = 'cancel'
		
		def make_approval(self):
			for rec in self:
				rec.state = 'approve'

		def make_booking(self):
			for rec in self:
				account_obj = self.env['account.move']
				company_id = self.env.user.company_id
				if rec.room_type_id.property_account_income_id :
					vals={'partner_id':rec.customer_id.id, 
								'user_id':rec.env.user.id,
								'move_type':'out_invoice',
								'currency_id':company_id.currency_id.id,
								'company_id':company_id.id,
								'invoice_origin':rec.name,
								'name':rec.name,
								'invoice_line_ids':[(0,0,{'product_id':rec.room_type_id.id,'name':rec.name,'account_id':rec.room_type_id.property_account_income_id.id,'quantity':1,'price_unit':rec.untax_amt})]
								}

				else :
					vals={'partner_id':rec.customer_id.id, 
								'user_id':rec.env.user.id,
								'move_type':'out_invoice',
								'currency_id':company_id.currency_id.id,
								'company_id':company_id.id,
								'invoice_origin':rec.name,
								'name':rec.name,
								'invoice_line_ids':[(0,0,{'product_id':rec.room_type_id.id,'name':rec.name,'account_id':rec.room_type_id.categ_id.property_account_income_categ_id.id,'quantity':1,'price_unit':rec.untax_amt})]
								}

				if rec.room_type_id.property_account_expense_id :                  
					vals2={'partner_id':rec.hotel_id.id, 
									'user_id':rec.env.user.id,
									'currency_id':company_id.currency_id.id,
									'company_id':company_id.id,
									'move_type':'in_invoice',
									'invoice_origin':rec.name,
									'name':rec.name,
									'invoice_line_ids':[(0,0,{'product_id':rec.room_type_id.id,'name':rec.name,'account_id':rec.room_type_id.property_account_expense_id.id,'quantity':1,'price_unit':rec.hotel_invoice_amt})]
									}

				else : 
					vals2={'partner_id':rec.hotel_id.id, 
									'user_id':rec.env.user.id,
									'currency_id':company_id.currency_id.id,
									'company_id':company_id.id,
									'move_type':'in_invoice',
									'invoice_origin':rec.name,
									'name':rec.name,
									'invoice_line_ids':[(0,0,{'product_id':rec.room_type_id.id,'name':rec.name,'account_id':rec.room_type_id.categ_id.property_account_expense_categ_id.id,'quantity':1,'price_unit':rec.hotel_invoice_amt})]
									}
				account_obj.create(vals)
				account_obj.create(vals2)
				rec.state = 'book'

		def _Invoice_count(self):
			for rec in self:
				if rec.name != False:
					invoice_order_ids = rec.env["account.move"].search([('name','=',rec.name)])
					rec.invoice_count = len(invoice_order_ids)
				else:
					rec.invoice_count = 0

		def button_count_invoice(self):
			self.ensure_one()
			return {
				'name': 'Invoice',
				'type': 'ir.actions.act_window',
				'view_mode': 'kanban,tree,form',
				'res_model': 'account.move',
				'domain': [('name','=',self.name)],
			}

		def issue_ticket(self):
			for rec in self:
				invoice_obj = self.env['account.move'].search([('name','=',rec.name)])
				for invoice in invoice_obj:
					if invoice.move_type == 'in_invocie':
						rec.hotel_room_reserve_invoice_ids = [(6,0,{'partner_id':rec.customer_id.id, 
						'user_id':rec.env.user.id,
						'currency_id':rec.env.user.company_id.currency_id.id,
						'company_id':rec.env.user.company_id.id,
						'invoice_origin':rec.name,
						'name':rec.name,
						'invoice_line_ids':[(0,0,{'product_id':rec.room_type_id.id,'name':rec.name,'account_id':rec.room_type_id.property_account_income_id.id or rec.room_type_id.categ_id.property_account_income_categ_id.id,'quantity':1,'price_unit':rec.untax_amt})]
						})]
				rec.state = 'issue'

		def compute_amt(self):
			for rec in self:
				if not rec.checkin_date:
					raise UserError(_("Check In Date in not defined")) 
				if not rec.checkout_date:
					raise UserError(_("Check Out Date in not defined")) 
				if not rec.hotel_rent:
					raise UserError(_("Rate is not define for above Hotel information.")) 
				if not rec.room_rent:
					raise UserError(_("Rate is not define for above Hotel information.")) 
				s_date = datetime.datetime.strptime(str(rec.checkin_date), '%Y-%m-%d').date()
				e_date = datetime.datetime.strptime(str(rec.checkout_date), '%Y-%m-%d').date()
				ans = abs( e_date - s_date)
				rec.no_of_days = ans.days 
				
		@api.onchange('room_type_id')
		def room_type_id_onchange(self):
			for rec in self:
				tax = []
				if rec.room_type_id:
					if  rec.room_type_id.taxes_id:
						for tax_id in rec.room_type_id.taxes_id:
							tax.append(tax_id.id)
						rec.tax_ids =  [(6, 0, tax)]
								
		
		@api.onchange('customer_id')
		def customer_id_onchange(self):
			for rec in self:
				if rec.customer_id:
					rec.mobile = rec.customer_id.mobile
					rec.email_id = rec.customer_id.email

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
