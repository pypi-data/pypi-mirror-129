SELECT OrderDes.id_Design
FROM OrderDes
WHERE OrderDes.id_Order IN (
    SELECT Orders.ID_Order
    FROM Orders
    WHERE Orders.CustomerPurchaseOrder = '{customer_purchase_order}'
)
