/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToElement } from "@web/core/utils/render";

    publicWidget.registry.TourBooking = publicWidget.Widget.extend({
        selector: '#wrapwrap',
        events: {
            "click .booking_create_btn": "_onClick_booking_create_btn",
            "click #add_person": "_onClick_addPerson",
            "click #add_program": "_onClick_addProgram",
            "click #add_desti": "_onClick_add_dest",
            "click #add_include": "_onClick_addinclude",
            "click #add_exclude": "_onClick_addexclude",
            "click #add_site": "_onClick_addsite",
            "click #add_visa": "_onClick_addvisa",
            "click #add_hotel": "_onClick_addHotel",
            "click #add_travel": "_onClick_addTravel",
            "click #add_other": "_onClick_addOther",
            "click #add_service": "_onClick_addService",
            "click #submit_booking": "_onClick_submitbtn",
            'change #tour_id': '_onChangeTour',
            'change #season_id': '_onChangeSeason',
        },
        init: function(parent) {
            this._super(parent);
            this.rpc = this.bindService("rpc");
            $('.booking_create').hide()
            

        },
        start: async function () {
            var self = this;
            this._super.apply(this, arguments);

            var currentDateField = this.$('#current_date');
            if (currentDateField.length) {
                currentDateField.val(new Date().toISOString().split('T')[0]);
            }
            self.rpc("/booking/data", {}).then(function (result) {
                self.booking_data = result;
                });
        },

        _onClick_booking_create_btn: function() {

            $('.booking_create').show()
            $('#booking_data').hide()
        },

        _onClick_addPerson:async function () {
            var self = this;
            var person_line = renderToElement('Persons',{widget:this.booking_data});
            $('.add_person_tr').before(person_line);
            var new_line = $('.add_person_tr').prev('tr.orderline1');
            var deleter_button = new_line.find('.js_delete_person');

            $(deleter_button).click(function(e){
                $(e.currentTarget).parents('tr.orderline1').remove()
            });
        },
        
        _onClick_addProgram:async function () {
            var self = this;
            var program_line = renderToElement('Program',{widget:this.booking_data});
            $('.add_program_tr').before(program_line);
            var new_line = $('.add_program_tr').prev('tr.orderline2');
            var deleter_button = new_line.find('.js_delete_program');

            $(deleter_button).click(function(e){
                $(e.currentTarget).parents('tr.orderline2').remove()
            });
        },

        _onClick_add_dest:async function () {
            var self = this;
            var dest_line = renderToElement('Destinations',{widget:this.booking_data});
            $('.add_desti_tr').before(dest_line);
            var new_line = $('.add_desti_tr').prev('tr.orderline3');
            var deleter_button = new_line.find('.js_delete_dest');

            $(deleter_button).click(function(e){
                $(e.currentTarget).parents('tr.orderline3').remove()
            });


        },

        _onClick_addinclude:async function () {
            var self = this;
            var include_line = renderToElement('Cost_Include',{widget:this.booking_data});
            $('.add_include_tr').before(include_line);
            var new_line = $('.add_include_tr').prev('tr.orderline4');
            var deleter_button = new_line.find('.js_delete_include');

            $(deleter_button).click(function(e){
                $(e.currentTarget).parents('tr.orderline4').remove()
            });
        },

        _onClick_addexclude:async function () {
            var self = this;
            var exclude_line = renderToElement('Cost_Exclude',{widget:this.booking_data});
            $('.add_exclude_tr').before(exclude_line);
            var new_line = $('.add_exclude_tr').prev('tr.orderline5');
            var deleter_button = new_line.find('.js_delete_exclude');

            $(deleter_button).click(function(e){
                $(e.currentTarget).parents('tr.orderline5').remove()
            });
        },

        _onClick_addsite:async function () {
            var self = this;
            var site_line = renderToElement('Site',{widget:this.booking_data});
            $('.add_site_tr').before(site_line);
            var new_line = $('.add_site_tr').prev('tr.orderline6');
            var deleter_button = new_line.find('.js_delete_site');

            $(deleter_button).click(function(e){
                $(e.currentTarget).parents('tr.orderline6').remove()
            });
        },

        _onClick_addvisa:async function () {
            var self = this;
            var visa_line = renderToElement('Visa',{widget:this.booking_data});
            $('.add_visa_tr').before(visa_line);
            var new_line = $('.add_visa_tr').prev('tr.orderline7');
            var deleter_button = new_line.find('.js_delete_visa');

            $(deleter_button).click(function(e){
                $(e.currentTarget).parents('tr.orderline7').remove()
            });
        },

        _onClick_addHotel:async function () {
            var self = this;
            var hotel_line = renderToElement('Hotel',{widget:this.booking_data});
            $('.add_hotel_tr').before(hotel_line);
            var new_line = $('.add_hotel_tr').prev('tr.orderline8');
            var deleter_button = new_line.find('.js_delete_hotel');

            $(deleter_button).click(function(e){
                $(e.currentTarget).parents('tr.orderline8').remove()
            });
        },

        _onClick_addTravel:async function () {
            var self = this;
            var tavel_line = renderToElement('Travel',{widget:this.booking_data});
            $('.add_travel_tr').before(tavel_line);
            var new_line = $('.add_travel_tr').prev('tr.orderline9');
            var deleter_button = new_line.find('.js_delete_travel');

            $(deleter_button).click(function(e){
                $(e.currentTarget).parents('tr.orderline9').remove()
            });
        },

        _onClick_addOther:async function () {
            var self = this;
            var other_line = renderToElement('Other',{widget:this.booking_data});
            $('.add_other_tr').before(other_line);
            var new_line = $('.add_other_tr').prev('tr.orderline10');
            var deleter_button = new_line.find('.js_delete_other');

            $(deleter_button).click(function(e){
                $(e.currentTarget).parents('tr.orderline10').remove()
            });
        },

        _onClick_addService:async function () {
            var self = this;
            var service_line = renderToElement('Service',{widget:this.booking_data});
            $('.add_service_tr').before(service_line);
            var new_line = $('.add_service_tr').prev('tr.orderline11');
            var deleter_button = new_line.find('.js_delete_service');

            $(deleter_button).click(function(e){
                $(e.currentTarget).parents('tr.orderline11').remove()
            });
        },


        _createbook: async function (form_data) {
            const bookingResponse = await this.rpc(
                '/create-book', {'form_data': form_data,})
            return bookingResponse
        },

        _prepareData: function (form) {
            var person_ids = []
            $('.person_tbody tr.orderline1').each(function(i, j){
                person_ids.push({
                    'partner_id':parseInt($(j).find('select[name=partner_id]').val()),
                    'name': $(j).find('input[name=name]').val(),
                    'gender': $(j).find('select[name=gender]').val(),
                    'type': $(j).find('select[name=type]').val(),   
                })
            })
            
            var program_ids = []
            $('.tour_tbody tr.orderline2').each(function(i, j){
                program_ids.push({
                    'name':$(j).find('input[name=name]').val(),
                    'days':parseInt($(j).find('input[name=days]').val()),
                    'description':$(j).find('input[name=description]').val(),
                    'breakfast':$(j).find('input[name=breakfast]').prop('checked'),
                    'lunch':$(j).find('input[name=lunch]').prop('checked'),
                    'dinner':$(j).find('input[name=dinner]').prop('checked'),
                    'expected_line_sale':parseFloat($(j).find('input[name=expected_line_sale]').val()),
                })
            })
    
            var destination_ids = []
            $('.desti_tbody tr.orderline3').each(function(i, j){
                destination_ids.push({
                    'destination_id':parseInt($(j).find('select[name=destination_id]').val()),
                    'country_id': parseInt($(j).find('select[name=country_id]').val()),
                    'nights':parseInt($(j).find('input[name=nights]').val()),
                    'visa_chk':$(j).find('input[name=visa_chk]').prop('checked'),
                })
            })

            var include_ids = []
            $('.include_tbody tr.orderline4').each(function(i, j){
                include_ids.push({
                    'facility_id': parseInt($(j).find('select[name=facility_id]').val()),
                    'name':($(j).find('input[name=name]').val()),
                    
                })
            })

            var exclude_ids = []
            $('.exclude_tbody tr.orderline5').each(function(i, j){
                exclude_ids.push({
                    'facility_id': parseInt($(j).find('select[name=facility_id]').val()),
                    'name':($(j).find('input[name=name]').val()),
                })
            })

            var site_ids = []
            $('.site_tbody tr.orderline6').each(function(i, j){
                site_ids.push({
                    'site_name':($(j).find('select[name=site_name]').val()),
                    'new_sale_price': ($(j).find('input[name=new_sale_price]').val()),
                    'total_sale_price': parseFloat($(j).find('input[name=total_sale_price]').val())
                })
            })

            var visa_ids = []
            $('.visa_tbody tr.orderline7').each(function(i, j){
                visa_ids.push({
                    'country_id':parseInt($(j).find('select[name=country_id]').val()),
                    'visa': ($(j).find('input[name=visa]').val()),
                    'visa_type': ($(j).find('select[name=visa_type]').val()),
                    'sale_price': parseFloat($(j).find('input[name=sale_price]').val()),
                    'total_person': parseInt($(j).find('input[name=total_person]').val()),
                    'total_sale_price': parseFloat($(j).find('input[name=total_sale_price]').val()),
                })
            })

            var  hotel_ids= []
            $('.hotel_tbody tr.orderline8').each(function(i, j){
                hotel_ids.push({
                    'name':($(j).find('input[name=name]').val()),
                    'destination_id': parseInt($(j).find('select[name=destination_id]').val()),
                    'hotel_type_id': parseInt($(j).find('select[name=hotel_type_id]').val()),
                    'hotel_id': parseInt($(j).find('select[name=hotel_id]').val()),
                    'room_type_id': parseInt($(j).find('select[name=room_type_id]').val()),
                    'room_req':parseInt($(j).find('input[name=room_req]').val()),
                    'days':parseInt($(j).find('input[name=days]').val()),
                    'customer_price':parseFloat($(j).find('input[name=customer_price]').val()),
                    'customer_price_total':parseFloat($(j).find('input[name=customer_price_total]').val()),
                })
            })

            var travel_ids = []
            $('.travel_tbody tr.orderline9').each(function(i, j){
                travel_ids.push({
                    'name':($(j).find('input[name=name]').val()),
                    'transport_id': parseInt($(j).find('select[name=transport_id]').val()),
                    'date':($(j).find('input[name=date]').val()),
                    'transport_carrier_id': parseInt($(j).find('select[name=transport_carrier_id]').val()),
                    'transport_type_id': parseInt($(j).find('select[name=transport_type_id]').val()),
                    'travel_class_id': parseInt($(j).find('select[name=travel_class_id]').val()),
                    'from_dest_id': parseInt($(j).find('select[name=from_dest_id]').val()),
                    'to_dest_id': parseInt($(j).find('select[name=to_dest_id]').val()),
                    'sale_price_adult': parseFloat($(j).find('input[name=sale_price_adult]').val()),
                    'sale_price_child': parseFloat($(j).find('input[name=sale_price_child]').val()),
                    'cost_price_adult': parseFloat($(j).find('input[name=cost_price_adult]').val()),
                    'cost_price_child': parseFloat($(j).find('input[name=cost_price_child]').val()),
                })
            })

            var other_ids = []
            $('.other_tbody tr.orderline10').each(function(i, j){
                other_ids.push({
                    'product_id': parseInt($(j).find('select[name=product_id]').val()),
                    'sale_price':parseFloat($(j).find('input[name=sale_price]').val()),
                    'product_uom_qty':parseFloat($(j).find('input[id=product_uom_qty]').val()),
                    'product_uom_id': parseInt($(j).find('select[name=product_uom_id]').val()),
                    'discount':parseFloat($(j).find('input[name=discount]').val()),
                    'price_subtotal':parseFloat($(j).find('input[name=price_subtotal]').val()),
                })
            })

            var service_ids = []
            $('.service_tbody tr.orderline11').each(function(i, j){
                service_ids.push({
                    'insurance_type_id': parseInt($(j).find('select[name=insurance_type_id]').val()),
                    'insurance_cost_for_adults':parseFloat($(j).find('input[name=insurance_cost_for_adults]').val()),
                    'insurance_cost_for_childs':parseFloat($(j).find('input[name=insurance_cost_for_childs]').val()),
                    'total_cost': parseFloat($(j).find('input[name=total_cost]').val()),
                })
            })
            
            return {
                'customer_id': $('#customer_id').data().id,
                'current_date':$('#current_date').val(),
                'current_date':form.find('#current_date').val(),
                'mobile1':$('#mobile1').val(),
                'email_id':$('#email_id').val(),
                'via':$('#via').val(),
                'agent_id':parseInt($('#agent_id').val()),
                'pricelist_id':parseInt($('#pricelist_id').val()),
                'adult':parseInt($('#adult').val()),
                'child':parseInt($('#child').val()),
                'tour_type':$('#tour_type').val(),
                'tour_dates_id': parseInt($('#tour_dates_id option:selected').data('dateId')),
                'tour_id':parseInt($('#tour_id').val()),
                'season_id':parseInt($('#season_id').val()),
                'payment_policy_id':parseInt($('#payment_policy_id').val()),
                'tour_customer_ids': person_ids,
                'tour_program_book_ids': program_ids,
                'tour_destination_book_ids': destination_ids,
                'itinary_cost_include_book_lines': include_ids,
                'itinary_cost_exclude_book_lines': exclude_ids,
                'sites_costing_book_ids': site_ids,
                'visa_costing_book_ids': visa_ids,
                'hotel_planer_book_ids': hotel_ids,
                'travel_planer_book_ids': travel_ids,
                'service_book_ids': other_ids,
                'insurance_line_ids': service_ids,


            }
        },

        _onClick_submitbtn: async function (ev) {
            ev.preventDefault();
            var data = this._prepareData($(ev.currentTarget).parents('form'))
            if(data.customer_id != '' && data.pricelist_id != '' && data.tour_type != ''  && data.tour_dates_id != '' && data.tour_id != '' && data.season_id != '' && data.payment_policy_id != '') 
            {
                var response = await this._createbook(data)
                alert("Booking created sucessfully")
                $('#booking_create').hide();
                $('#booking_data').show();
                $('#booking_create').hide();
                location.href = location.origin + '/thankyou/booking/' + response.booking;
            } else {
                alert('Please fill details')
            }
        },

        _onChangeTour: function () {
            var self = this;
            var tourId = $('#tour_id').val();
            var visa = document.getElementById('visa_chk');

            if (tourId) {
                self.rpc('/tour/data', { 'tour_id': tourId},).then(function (tourData) {
                    var tourdate = tourData.dates
                    var tourDatesSelect = $('#tour_dates_id');
                    tourDatesSelect.empty();

                        tourDatesSelect.append($('<option>', {
                            text: 'Select a date'  
                        }));

                        tourdate.forEach(function (dates) {
                      
                            tourDatesSelect.append($('<option>', {
                                'data-season-id':dates.season_id,
                                'data-date-id': dates.tour_dates_id, 
                                text: dates.rec_id,     
                            }));
                        });

                    var programData = tourData.program
                    var destinationData = tourData.destinations
                    var includeData = tourData.include
                    var excludeData = tourData.exclude
                    var siteData = tourData.site
                    var visaData = tourData.visa
                    var hotelData = tourData.hotel
                    var travelData = tourData.travel
                    var serviceData = tourData.service

                    $('tbody tr.orderline2').remove();
                    programData.forEach(function (programElement) {
                        $('#add_program').trigger('click');
                        var line = $('tbody tr.orderline2:last')
                        line.find('#name').val(programElement.name);
                        line.find('#name').val(programElement.name);
                        line.find('#days').val(programElement.days);
                        line.find('#description').val(programElement.description);
                        line.find('#expected_line_sale').val(programElement.expected_line_sale);
                        line.find('#breakfast').prop('checked', programElement.breakfast);
                        line.find('#lunch').prop('checked', programElement.lunch);
                        line.find('#dinner').prop('checked', programElement.dinner);
                    });

                    
                    $('tbody tr.orderline3').remove();
                    destinationData.forEach(function (destinationElement) {
                        $('#add_desti').trigger('click');
                        var line = $('tbody tr.orderline3:last')
                        line.find('#destination_id').val(destinationElement.destination_id);
                        line.find('#country_id').val(destinationElement.country_id);
                        line.find('#nights').val(destinationElement.nights);
                        line.find('#visa_chk').prop('checked',destinationElement.visa_chk);

                    });
                    
                    $('tbody tr.orderline4').remove();
                    includeData.forEach(function (includeElement) {
                        $('#add_include').trigger('click');
                        var line = $('tbody tr.orderline4:last')
                        line.find('#facility_id').val(includeElement.include_facility_id);
                        line.find('#description').val(includeElement.includename);
                    });

                    $('tbody tr.orderline5').remove();
                    excludeData.forEach(function (excludeElement) {
                        $('#add_exclude').trigger('click');
                        var line = $('tbody tr.orderline5:last')
                        line.find('#facility_id').val(excludeElement.exclude_facility_id);
                        line.find('#description').val(excludeElement.excludename);
                    });
                    
                    $('tbody tr.orderline6').remove();
                    siteData.forEach(function (siteElement) {
                        $('#add_site').trigger('click');
                        var line = $('tbody tr.orderline6:last')
                        line.find('#site_name').val(siteElement.sitename);
                        line.find('#new_sale_price').val(siteElement.new_sale_price);
                        line.find('#total_sale_price').val(siteElement.total_sale_price);
                    });
                    
                    $('tbody tr.orderline7').remove();
                    visaData.forEach(function (visaElement) {
                        $('#add_visa').trigger('click');
                        var line = $('tbody tr.orderline7:last')
                        line.find('#country_id').val(visaElement.country_id);
                        line.find('#visa').val(visaElement.visaname);
                        line.find('#visa_type').val(visaElement.visa_type);
                        line.find('#sale_price').val(visaElement.sale_price);
                        line.find('#total_person').val(visaElement.total_person);
                        line.find('#total_sale_price').val(visaElement.total_sale_price);
                    });

                    $('tbody tr.orderline8').remove();
                    hotelData.forEach(function (hotelElement) {
                        $('#add_hotel').trigger('click');
                        var line = $('tbody tr.orderline8:last')
                        line.find('#name').val(hotelElement.hotelname);
                        line.find('#destination_id').val(hotelElement.destination_id);
                        line.find('#hotel_type_id').val(hotelElement.hotel_type_id);
                        line.find('#hotel_id').val(hotelElement.hotel_id);
                        line.find('#room_type_id').val(hotelElement.room_type_id);
                        line.find('#room_req').val(hotelElement.room_req);
                        line.find('#days').val(hotelElement.days);
                        line.find('#customer_price').val(hotelElement.customer_price);
                        line.find('#customer_price_total').val(hotelElement.customer_price_total);
                    });

                    $('tbody tr.orderline9').remove();
                    travelData.forEach(function (travelElement) {
                        $('#add_travel').trigger('click');
                        var line = $('tbody tr.orderline9:last')
                        line.find('#name').val(travelElement.travelname);
                        line.find('#transport_id').val(travelElement.transport_id);
                        line.find('#date').val(travelElement.date);
                        line.find('#transport_carrier_id').val(travelElement.transport_carrier_id);
                        line.find('#transport_type_id').val(travelElement.transport_type_id);
                        line.find('#travel_class_id').val(travelElement.travel_class_id);
                        line.find('#from_dest_id').val(travelElement.from_dest_id);
                        line.find('#to_dest_id').val(travelElement.to_dest_id);
                        line.find('#cost_price_adult').val(travelElement.cost_price_adult);
                        line.find('#cost_price_child').val(travelElement.cost_price_child);
                        line.find('#sale_price_adult').val(travelElement.sale_price_adult);
                        line.find('#sale_price_child').val(travelElement.sale_price_child);
                        
                    });

                    $('tbody tr.orderline10').remove();
                    serviceData.forEach(function (serviceElement) {
                        $('#add_other').trigger('click');
                        var line = $('tbody tr.orderline10:last')
                        line.find('#product_id').val(serviceElement.product_id);
                        line.find('#sale_price').val(serviceElement.sale_price);
                        line.find('#product_uom_qty').val(serviceElement.product_uom_qty);
                        line.find('#product_uom_id').val(serviceElement.product_uom_id);
                        line.find('#discount').val(serviceElement.discount);
                        line.find('#price_subtotal').val(serviceElement.price_subtotal);
                    });
            });
            }
        },

        // get date according season
        _onChangeSeason : function() {
            var seasonId = $('#season_id').val();
            $('#tour_dates_id option').each(function () {
                var dateSeasonId = $(this).data('season-id'); 
        
                if (dateSeasonId == seasonId) {
                    $(this).show(); 
                } else {
                    $(this).hide(); 
                }
            });
        },
    });

 
    publicWidget.registry.TourInquiry = publicWidget.Widget.extend({
        selector: '#wrapwrap',
        events: {
            "click .inquiry_create_btn": "_onClick_inquiry_create_btn",
            "click #add_dest": "_onClick_addDestination",
            "click #add_line": "_onClick_addLine",
            "click #submit_inquiry": "_onClick_submit",
            'change #lead_id': '_onChangeLead',

        },

        init: function(parent, options) {
            $('.inquiry_create').hide();
            this._super(parent);
            this.rpc = this.bindService("rpc");
        },

        start: async function () {
            var self = this;
            this._super.apply(this, arguments);

            self.rpc('/inquiry/data', {},
            ).then(function (result) {
                self.inquiry_data = result;
                    });
        },

        _onClick_inquiry_create_btn:function() {
            $('.inquiry_create').show();
            $('#inquiry_data').hide();
        },

        _onChangeLead: function () {
            var self = this;
            var leadId = $('#lead_id').val();

            if (leadId) {
                self.rpc('/lead/data', { 'lead_id': leadId },
                ).then(function (leadData) {
                    $('#street').val(leadData.street);
                    $('#street2').val(leadData.street2);
                    $('#zip').val(leadData.zip);
                    $('#city').val(leadData.city);
                    $('#state_id').val(leadData.state_id);
                    $('#email_id').val(leadData.email_id);
                    $('#contact_name').val(leadData.contact_name);
                    $('#mobile').val(leadData.mobile);
                    $('#country_id').val(leadData.country_id);
                    
                });
            }
        },
 
        _onClick_addDestination:async function () {
            var self = this;
    
            var destination_line = renderToElement('Destination',{widget:this.inquiry_data});
            $('.add_destination_tr').before(destination_line);
            var new_line = $('.add_destination_tr').prev('tr.order_line');
            var deleter_button = new_line.find('.js_delete_destination');

            $(deleter_button).click(function(e){
                $(e.currentTarget).parents('tr.order_line').remove()
            });
        },

        _onClick_addLine:async function () {
            var self = this;

            var add_line = renderToElement('Trasport', {widget:this.inquiry_data});
            $('.add_dest_tr').before(add_line);
            var new_line = $('.add_dest_tr').prev('tr.order_line1');
            var delete_button = new_line.find('.js_delete_line');

            // Delete line
            $(delete_button).click(function(e){
                $(e.currentTarget).parents('tr.order_line1').remove()
            });
        },

        _createinq: async function (form_data) {
            const inquiryResponse = await this.rpc('/create-inq',{'form_data': form_data,})
            return inquiryResponse
        },

        _prepareFormData: function (form) {
            var line_ids = []
            var add_ids = []
            $('.line_tbody tr.order_line').each(function(i, j){
                line_ids.push({
                    'tour_destination_id':parseInt($(j).find('select[name=tour_destination_id]').val()),
                    'country_id': parseInt($(j).find('select[name=country_id]').val()),
                    'name': parseInt($(j).find('input[name=name]').val())
                })
            })

            $('.dest_tbody tr.order_line1').each(function(i, j){
                add_ids.push({
                    'name':($(j).find('select[name=name]').val()),
                    'product_id': parseInt($(j).find('select[name=product_id]').val()),
                    'travel_class_id': parseInt($(j).find('select[name=travel_class_id]').val())
                })
            })
            return {
                'current_date': $('#current_date').val(),
                'lead_id':$('#lead_id').val(),
                'email_id':$('#email_id').val(),
                'via':$('#via').val(),
                'agent_id':$('#agent_id').val(),
                'contact_name':$('#contact_name').val(),
                'mobile':$('#mobile').val(),
                'adult':$('#adult').val(),
                'child':$('#child').val(),
                'street':$('#street').val(),
                'street2':$('#street2').val(),
                'zip':$('#zip').val(),
                'city':$('#city').val(),
                'state_id':$('#state_id').val(),
                'country_id':$('#country_id').val(),
                'checkin_date':$('#checkin_date').val(),
                'checkout_date':$('#checkout_date').val(),
                'tour_low_price':$('#tour_low_price').val(),
                'tour_high_price':$('#tour_high_price').val(),
                'hotel_type_id':$('#hotel_type_id').val(),
                'room_type_id':$('#room_type_id').val(),
                'room_req':$('#room_req').val(),
                'low_price':$('#low_price').val(),
                'high_price':$('#high_price').val(),
                'destination_lines_ids': line_ids,
                'transport_ids': add_ids,
            }
        },
        
        _onClick_submit: async function (ev) {
            ev.preventDefault();
            var data = this._prepareFormData($(ev.currentTarget).parents('form'))
            if(data.current_date != '' && data.checkin_date != '' && data.checkin_date != '' && data.mobile != '') 
            {
                var response = await this._createinq(data)
                alert("inquiry created sucessfully")
                $('#inquiry_create').hide();
                $('#inquiry_data').show();
                $('#inquiry_create').hide();
                location.href = location.origin + '/thankyou/inquiry/' + response.inquiry;
            } else {
                alert('Please fill details')
            }          
        },
 
    });

