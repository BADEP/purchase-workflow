# Copyright 2023 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    owner_id = fields.Many2one(
        "res.partner",
        "Assign Owner",
        check_company=True,
        help="The assigned value will be set on the corresponding field of the "
        "incoming stock picking.",
    )
