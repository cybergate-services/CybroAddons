# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Niyas Raphy and Sreejith p (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import fields, models, api
from odoo.exceptions import Warning


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    barcode = fields.Char(string='Barcode')

    @api.onchange('barcode')
    def barcode_scanning(self):
        match = False
        product_obj = self.env['product.product']
        product_id = product_obj.search([('barcode', '=', self.barcode)])
        if self.barcode and not product_id:
            self.barcode = None
            raise Warning('No product is available for this barcode')
        if self.barcode and self.move_ids_without_package:
            for line in self.move_ids_without_package:
                if line.product_id.barcode == self.barcode:
                    line.quantity_done += 1
                    self.barcode = None
                    match = True
        if self.barcode and not match:
            self.barcode = None
            if product_id:
                raise Warning('This product is not available in the order.'
                              'You can add this product by clicking the "Add an item" and scan')


class StockPickingOperation(models.Model):
    _inherit = 'stock.move'

    barcode = fields.Char(string='Barcode')

    @api.onchange('barcode')
    def _onchange_barcode_scan(self):
        product_rec = self.env['product.product']
        if self.barcode:
            product = product_rec.search([('barcode', '=', self.barcode)])
            self.product_id = product.id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
