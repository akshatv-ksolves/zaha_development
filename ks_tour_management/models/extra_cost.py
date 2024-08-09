from odoo import api, models, fields

class ExtraCost(models.Model):
    _name = 'extra.cost'
    _description = 'Extra Cost'

    name = fields.Many2one('product.product',string='Product Name')
    description = fields.Text(string='Description')
    price = fields.Integer(string='Price')
    # discount = fields.Integer(string='Discount')
    sub_total = fields.Float(string='Subtotal', compute='_compute_sub_total', store=True)
    hotel_reservation_id = fields.Many2one('tour.hotel.reservation', string='Hotel Reservation')
    product_uom_qty = fields.Float(
        string="Quantity",
        digits='Product Unit of Measure', default=1.0,
        store=True, readonly=False, required=True)


    @api.onchange('name', 'product_uom_qty')
    def _onchange_product_quantity(self):
        if self.name and self.hotel_reservation_id.hotel_id and self.hotel_reservation_id.hotel_id.property_product_pricelist :
            matching_rule = self.hotel_reservation_id._find_matching_rule(self.name)
            if matching_rule:
                self.price = self.hotel_reservation_id._compute_price_rule(
                    matching_rule,
                    self.name,
                    self.product_uom_qty
                )
            else:
                self.price = self.name.list_price

            self.description = self.name.description or ''
        else:
            self.price = self.name.list_price if self.name else 0
            self.description = self.name.description if self.name else ''


    @api.depends('price', 'product_uom_qty')
    def _compute_sub_total(self):
        for record in self:
            record.sub_total = record.price * record.product_uom_qty