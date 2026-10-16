# Copyright 2023 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        res = super()._get_new_picking_values()
        owner = self.purchase_line_id.order_id.owner_id
        if len(owner) == 1:
            res["owner_id"] = owner.id
        return res
