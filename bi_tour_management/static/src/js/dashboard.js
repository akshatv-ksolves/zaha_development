/** @odoo-module **/
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { Component , onWillStart ,useState, onMounted, onWillUnmount} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";
const actionRegistry = registry.category("actions");

export class TourDashDoard extends Component {
    
    static template = 'TourDashDoard';
    static props = ["*"];
    
    setup() {
        this.user = useService("user")
        this.action = useService("action");
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.state = useState({
            dashboards_templates: ['TourDashDoard'],
            templates: [],
            total_tour_booking :0,
            total_draft_inquiry :0,
            total_confirmed_inquiary :0,
            total_tour_inprogress_booking :0,
            total_bookings_of_week :0,
            total_bookings_of_month :0,
        
        })
        this.today_sale = [];

        onMounted(async () => {
            var self = this;
            await self.fetch_data();
            self.render_graphs();
        });
    }

    render_graphs() {
        this.get_weekly_booking_chart_canvas();
        this.get_monthly_booking_chart_canvas();
    }
    async get_weekly_booking_chart_canvas() {
        var self = this;
        var weekly_booking_chart_canvas = $(".weekly_booking_chart_canvas");
        var get_weekly_booking = await this.orm.call('tour','action_get_weekly_booking')
            var chart = new Chart(weekly_booking_chart_canvas, {
                type: "bar",
                data: {
                    labels: get_weekly_booking[1],
                    datasets: [{
                        backgroundColor: get_weekly_booking[2],
                        data: get_weekly_booking[0],
                    }]
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        position: "top",
                        text: " Weekly Booking Chart",
                    },
                    legend: {
                        display: false,
                    },
                }
            });
        
    }

    async get_monthly_booking_chart_canvas() {
        var self = this;
        var monthly_booking_chart_canvas = $(".monthly_booking_chart_canvas");
        var get_weekly_booking =await this.orm.call("tour","action_get_monthly_booking")
        
            var chart = new Chart(monthly_booking_chart_canvas, {
                type: "bar",
                data: {
                    labels: get_weekly_booking[1],
                    datasets: [{
                        backgroundColor: get_weekly_booking[2],
                        data: get_weekly_booking[0],
                    }]
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        position: "top",
                        text: " Monthly Booking Chart",
                    },
                    legend: {
                        display: false,
                    },
                }
            });
    }
  
    async fetch_data() {
        var self = this;
        var def1 = await this.orm.call('tour', 'get_data',)
            self.state.total_draft_inquiry = def1['total_draft_inquiry']
            self.state.total_confirmed_inquiary = def1['total_confirmed_inquiary']
            self.state.total_tour_booking = def1['total_tour_booking']
            self.state.total_tour_inprogress_booking = def1['total_tour_inprogress_booking']
            self.state.total_bookings_of_week = def1['total_bookings_of_week']
            self.state.total_bookings_of_month = def1['total_bookings_of_month']
        return def1;
    }
    
    // total draft inquires
    draft_inquiry() {
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.action.doAction({
            name: _t("Draft Inquiries", options),
            type: 'ir.actions.act_window',
            res_model: 'tour.preference',
            view_mode: 'tree,form',
            views: [
                [false, 'list'],
                [false, 'form']
            ],
            domain: [
                ['state', '=', 'draft']
            ],
            target: 'current',
        }, options)
    }

    // Total membership action
    confirmed_inquiry() {
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.action.doAction({
            name: _t("Confimed Inquiries"),
            type: 'ir.actions.act_window',
            res_model: 'tour.preference',
            view_mode: 'tree,form',
            views: [
                [false, 'list'],
                [false, 'form']
            ],
            domain: [
                ['state', '=', 'confirm']
            ],
            target: 'current'
        }, options)
    }

    confimed_booking() {
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.action.doAction({
            name: _t("Memberships"),
            type: 'ir.actions.act_window',
            res_model: 'tour.booking',
            view_mode: 'tree,form',
            views: [
                [false, 'list'],
                [false, 'form']
            ],
            domain: [
                ['state', '=', 'confirm']
            ],
            target: 'current'
        }, options)
    }

    inprogress_booking() {
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.action.doAction({
            name: _t("Memberships"),
            type: 'ir.actions.act_window',
            res_model: 'tour.booking',
            view_mode: 'tree,form',
            views: [
                [false, 'list'],
                [false, 'form']
            ],
            domain: [
                ['state', '=', 'in_process']
            ],
            target: 'current'
        }, options)
    }

}
registry.category("actions").add("tour_dashboard_tag", TourDashDoard)
