# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from odoo.fields import Domain


class ResPartner(models.Model):
    _inherit = "res.partner"

    purchase_user_id = fields.Many2one(
        comodel_name="res.users",
        domain="[('share', '=', False)]",
        string="Purchase representative",
        index=True,
    )
    purchase_team_id = fields.Many2one(
        comodel_name="purchase.team",
        string="Purchase team",
        index=True,
    )

    @api.model
    def _access_domain(self, operation):
        """Inject extra domain for restricting partners when the user
        has the group 'Purchase / User (own orders)."""
        res = super()._access_domain(operation)
        user = self.env.user
        group1 = "purchase_security.group_purchase_own_orders"
        group2 = "purchase_security.group_purchase_group_orders"
        group3 = "purchase.group_purchase_manager"
        if user.has_group(group1) and not user.has_group(group3):
            partner_domain = Domain.OR(
                [
                    Domain("message_partner_ids", "in", user.partner_id.ids),
                    Domain("id", "=", user.partner_id.id),
                ]
            )
            if user.has_group(group2):
                extra_domain = Domain.OR(
                    [
                        partner_domain,
                        Domain("purchase_team_id", "=", user.purchase_team_ids[:1].id),
                        Domain("purchase_team_id", "=", False),
                    ]
                )
            else:
                extra_domain = Domain.OR(
                    [
                        partner_domain,
                        Domain("purchase_user_id", "=", user.id),
                        Domain.AND(
                            [
                                Domain("purchase_user_id", "=", False),
                                Domain.OR(
                                    [
                                        Domain("purchase_team_id", "=", False),
                                        Domain(
                                            "purchase_team_id",
                                            "=",
                                            user.purchase_team_ids[:1].id,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                )
            res = Domain.AND([extra_domain, res])
        return res
