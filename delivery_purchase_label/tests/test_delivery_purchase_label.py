# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import SavepointCase


class TestDeliveryPurchaseLabel(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.picking_type = cls.env.ref(
            "delivery_purchase_label.picking_type_send_label"
        )
        cls.supplier = cls.env.ref("base.res_partner_1")
        cls.customer = cls.env.ref("base.res_partner_2")
        cls.carrier = cls.env.ref("delivery.delivery_carrier")
        cls.carrier.purchase_label_picking_type = cls.picking_type
        cls.supplier.purchase_delivery_carrier_id = cls.carrier

        cls.product = cls.env.ref("product.product_product_5")
        cls.order = cls.env["purchase.order"].new(
            {
                "partner_id": cls.supplier.id,
                "dest_address_id": cls.customer.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product.name,
                            "product_id": cls.product.id,
                            "product_qty": 5.0,
                            "product_uom": cls.product.uom_id.id,
                            "price_unit": 10,
                        },
                    )
                ],
            }
        )
        cls.order.order_line._onchange_quantity()

    def test_transfer_label_generated(self):
        self.carrier.purchase_label_picking_type = self.picking_type
        self.order._generate_purchase_delivery_label()
        label_picking = self.order.picking_ids
        self.assertEqual(label_picking.picking_type_id, self.picking_type)
        self.assertEqual(label_picking.state, "done")

    def test_transfer_label_not_generated(self):
        self.carrier.purchase_label_picking_type = False
        self.order._generate_purchase_delivery_label()
        self.assertFalse(self.order.picking_ids)
