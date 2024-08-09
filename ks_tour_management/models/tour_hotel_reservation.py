from odoo import api, fields, models, tools


class TourHotelReservation(models.Model):
    _inherit = "tour.hotel.reservation"

    # offer_id = fields.Many2one('seasonal.offer')
    program_id = fields.Many2one('loyalty.program')
    discount_coupon = fields.Char(string='Discount Coupon', readonly=True)
    discounted_price = fields.Integer(string='Price After Discount')
    # offer_rate = fields.Integer(related='offer_id.offer_rate', string='Discount Rate')
    # untax_amt = fields.Float(string='Untax Amount',compute='_amount_all')
    pricelist_name = fields.Many2one('product.pricelist', string='Pricelist', readonly=True)
    program_ids = fields.Many2many('loyalty.program')
    extra_cost_lines = fields.One2many('extra.cost', 'hotel_reservation_id', string='Extra Cost')
    country_id = fields.Many2one('res.country', string='Country')

    def _find_matching_rule(self, product):
        self.ensure_one()
        date = fields.Date.context_today(self)

        items = self.env['product.pricelist.item'].search([
            ('pricelist_id', '=', self.hotel_id.property_product_pricelist.id),
            '|', ('product_tmpl_id', '=', product.id),
            '|', ('product_id', '=', product.id),
            ('applied_on', '=', '3_global'),
            '|', ('date_start', '<=', date),
            ('date_start', '=', False),
            '|', ('date_end', '>=', date),
            ('date_end', '=', False),
        ])

        # Sort items by priority and specificity
        return items.sorted(lambda r: (
            r.applied_on == '3_global',
            r.product_id and r.product_id != product,
            r.date_start,  # Later start date gets higher priority
            -r.min_quantity,  # Higher min_quantity gets higher priority
            -r.price_discount,
            -r.price_surcharge
        ), reverse=True)[:1]

    @api.onchange('hotel_id')
    def _onchange_pricelist_hotel(self):
        if self.hotel_id.property_product_pricelist:
            for line in self.extra_cost_lines:
                if line.name:
                    matching_rule = self._find_matching_rule(line.name)
                    if matching_rule:
                        line.price = self._compute_price_rule(matching_rule, line.name, line.product_uom_qty)
                    else:
                        line.price = line.name.list_price

    def _compute_price_rule(self, rule, product, quantity):
        base_price = product.list_price
        if rule.base == 'pricelist' and rule.base_pricelist_id:
            base_price = rule.base_pricelist_id.get_product_price(product, quantity, self.env.user.partner_id)
        elif rule.base == 'standard_price':
            base_price = product.standard_price

        if rule.compute_price == 'fixed':
            price = rule.fixed_price
        elif rule.compute_price == 'percentage':
            price = base_price * (1.0 - (rule.percent_price / 100.0))
        else:  # formula
            price_limit = base_price
            price = base_price
            context = dict(self.env.context, pricelist=self.pricelist_product_id.id, quantity=quantity)
            price = rule.with_context(context)._compute_price_rule_multi(product)[product.id][0]
            if rule.price_discount:
                price = price * (1.0 - rule.price_discount / 100.0)
            if rule.price_round:
                price = tools.float_round(price, precision_rounding=rule.price_round)
            if rule.price_surcharge:
                price += rule.price_surcharge
            if rule.price_min_margin:
                price = max(price, base_price + rule.price_min_margin)
            if rule.price_max_margin:
                price = min(price, base_price + rule.price_max_margin)
        return price


    @api.onchange('offer_id')
    def onchange_offer_id(self):
        self.discount_coupon = self.offer_id.discount_coupon


    def compute_amt(self):
        # if self.offer_id.compute_price == 'fixed':
        #     self.discounted_price = self.hotel_rent - self.offer_id.offer_rate
        # elif self.offer_id.compute_price == 'percentage':
        #     self.discounted_price = self.hotel_rent - ((self.offer_id.offer_percentage/100) * self.hotel_rent)
        # self.program_id = offers

        hotel_id = self.hotel_id.id
        pricelist_id = self.hotel_id.property_product_pricelist
        room_id = self.room_type_id.id
        room_name = self.room_type_id.display_name
        # room_att_ids = self.room_type_id.attribute_line_ids.mapped('id')

        # room_product_id = self.env['product.pricelist'].search([('id', '=', pricelist_id.id)]).item_ids
        # room_price = room_product_id.search([('pricelist_id','=',pricelist_id.id),('product_id','=',room_id)]).fixed_price

        # Searches for the product associated with the pricelist
        room_product_id_detail = self.env['product.pricelist.item'].search(
            [('pricelist_id', '=', pricelist_id.id), ('product_id', '=', room_id)])
        # room_product_id_direct = self.find_prod_id_in_pricelist(pricelist_id,room_id)

        # room_rate = self.env['product.pricelist'].search([('id','=',pricelist_id.id)]).item_ids.search([('product_id','=',room_id)])

        print(hotel_id, room_id, room_name, pricelist_id)
        if room_product_id_detail.compute_price == 'fixed':
            self.pricelist_name = pricelist_id.id
            self.room_rent = room_product_id_detail.fixed_price
        elif room_product_id_detail.compute_price == 'formula':
            self.pricelist_name = pricelist_id.id
            self.room_rent = self.env['product.pricelist.item'].search(
                [('pricelist_id', '=', room_product_id_detail.base_pricelist_id.id),
                 ('product_id', '=', room_id)]).fixed_price
        else:
            self.pricelist_name = ''
            self.room_rent = 0

        # offers = self.env['loyalty.program'].search([('pricelist_ids', 'in', self.pricelist_name.id)])
        offers = self.env['loyalty.program'].search([
            ('pricelist_ids', 'in', self.pricelist_name.id),
            ('country_group_ids', 'in', self.country_id.id),
            '&',
            ('date_from', '<=', self.checkin_date), ('date_to', '>=', self.checkin_date),
            ('date_from', '<=', self.checkout_date), ('date_to', '>=', self.checkout_date)
        ])
        print(offers.mapped('name'))

        if offers:
            self.program_ids = offers
        else:
            self.program_id = ''
        # offers = self.env['loyalty.program'].search([('pricelist_ids', 'in', self.pricelist_name.id)])
        # print(offers.mapped('name'))
        # domain = [('id', 'in', offers)]
        # return {'domain': {'program_id': domain}}
        # self.room_rent = self.env['product.product'].search([('id','=',room_id)]).list_price

    # def find_prod_id_in_pricelist(self,pricelist_id,room_id):
    #     room_product_item_ids = self.env['product.pricelist'].search([('id', '=', pricelist_id.id)]).item_ids
    #     room_product_id = room_product_item_ids.search([('pricelist_id', '=', pricelist_id.id), ('product_id', '=', room_id)])
    #     return room_product_id

    # def _amount_all(self):
    #     if self.discounted_price > 0:
    #         price = self.discounted_price
    #     else:
    #         price = self.hotel_rent
    #     self.untax_amt = price * self.no_of_days * self.room_required
    #     self.tax_amt = 0
    #     self.total_amt = self.untax_amt + self.tax_amt
    #     self.hotel_invoice_amt = self.room_rent * self.no_of_days * self.room_required


# class PricelistItem(models.Model):
#     _inherit = "product.pricelist.item"
#
#     hotel_id = fields.Many2one('res.partner', 'Hotel', required=True, domain=[('is_hotel', '=', True)])
