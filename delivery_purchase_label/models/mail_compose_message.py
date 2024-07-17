# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models

class MailComposer(models.TransientModel):
    _inherit="mail.compose.message"

    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields):
        res = super().generate_email_for_composer(template_id, res_ids, fields)
        if self.model != "purchase.order":
            return res
        if isinstance(res_ids, int):
            res_ids = [res_ids]
        # check we only have one res_id
        for res_id in res_ids:
            purchase_order = self.env["purchase.order"].browse(res_id)
            label_picking = purchase_order.delivery_label_picking_id
            # What if there is multiple attachment
            # How do I find the attachment containtin the labels ?
            attachment = self.env["ir.attachment"].search(
                [
                    ("res_model", "=", label_picking._name),
                    ("res_id", "=", label_picking.id),
                ]
            )
            if attachment:
                attachment_ids = res[res_id].get("attachment_ids", [])
                attachment_ids.append(attachment[0].id)
                res[res_id]["attachment_ids"] = attachment_ids
        return res
