

from delivery_module.routes import *

def register_routes(app,mysql):
    app.add_url_rule("/delivery/login",view_func=delivery_login,methods=["GET","POST"])
    app.add_url_rule("/delivery/delivery_dashboard",view_func=delivery_dashboard,methods=["GET","POST"])
    app.add_url_rule("/delivery/logout",view_func=delivery_logout)
    app.add_url_rule("/delivery/forgot_password",view_func=delivery_forgot_password,methods=["GET","POST"])
    app.add_url_rule("/delivery/assigned_deliveries",view_func=delivery_assigned_deliveries,methods=["GET","POST"])
    app.add_url_rule("/delivery/reject_pickup/<int:order_id>",view_func=delivery_reject_pickup, methods=["POST"])
    app.add_url_rule("/delivery/accept_pickup/<int:order_id>",view_func=delivery_accept_pickup, methods=["POST"])
    app.add_url_rule("/delivery/confirm_pickup/<int:order_id>",view_func=delivery_confirm_pickup, methods=["GET","POST"])
    app.add_url_rule("/delivery/order_updates",view_func=delivery_order_updates)
    app.add_url_rule("/delivery/mark_picked/<int:assignment_id>",view_func=delivery_mark_picked, methods=["POST"])
    app.add_url_rule("/delivery/reject_assignment/<int:assignment_id>",view_func=delivery_reject_assignment, methods=["POST"])
    app.add_url_rule("/delivery/mark_delivered/<int:assignment_id>",view_func=delivery_mark_delivered, methods=["POST"])
    app.add_url_rule("/delivery/total_earnings",view_func=delivery_total_earnings, methods=["GET","POST"])

