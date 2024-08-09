/** @odoo-module **/

console.log('JS loaded');

document.addEventListener('DOMContentLoaded', function() {
    // Set default inquiry date to today's date
    var inquiryDateInput = document.getElementById('inquiry_date');
    var today = new Date();
    var day = String(today.getDate()).padStart(2, '0');
    var month = String(today.getMonth() + 1).padStart(2, '0');
    var year = today.getFullYear();
    var todayDate = year + '-' + month + '-' + day;
    if (inquiryDateInput) {
        inquiryDateInput.value = todayDate;
    }
    var adultPersonsInput = $('#adult_persons')[0];
    var childInput = $('#child')[0];
    var preferStartDate = $('#prefer_start_date')[0];
    var preferEndDate = $('#prefer_end_date')[0];
    var mobileInput = $('#mobile')[0];
    var noOfRoomInput = $('#hotel_number_of_rooms')[0];
//    var tripBudgetMax = $('#budget_max')[0];
//    var tripBudgetMin = $('#budget_min')[0];
    var arrivalDateInput = $("#arrival_date")[0];
    var departureDateInput = $("#departure_date")[0];
    var nightsDisplay = $("#no_of_nights")[0];
    var hotelBudgetMax = $('#hotel_budget_max')[0];
    var hotelBudgetMin = $('#hotel_budget_min')[0];
    var submitButton = $('#submit_enquiry_button')[0];

    // Booking Template Variables
    var arrivalDateBooking = $('#arrivalDateBooking')[0];
    var departureDateBooking = $('#departureDateBooking')[0];
    var checkInBooking = $('#checkIn')[0];
    var checkOutBooking = $('#checkOut')[0];
    var numRoomsBooking = $('#numRooms')[0];
    var adultsBooking = $('#adultsBooking')[0];
    var childBooking = $('#childBooking')[0];
    var infantsBooking = $('#infantsBooking')[0];
    var submitButtonBooking = $('#submit_booking_button')[0];

    // Validation functions
    function validateMobile(input){
       var temp = parseInt(input.value)
       if(input.value){
            const regex = /^[0-9]*$/;
            if (!regex.test(input.value)) {
                alert("Mobile number should have only numbers");
                event.preventDefault();
            }
       }
    }
    function validatePersonCount(input) {
        if (input.value < 0) {
            alert("Count cannot be less than 0");
            event.preventDefault();
        }
    }
    function validateNegativeValue(input,string){
    if (input.value < 0) {
            alert(string + " cannot be less than 0");
            event.preventDefault();
        }
    }
    function validateTripDates(startDate, endDate) {
        if (startDate.value > endDate.value) {
            alert("Start date should be greater than End date");
             event.preventDefault();
        }
    }
    function validateBudget(min,max,string){
        if(min.value>max.value){
            alert(string + ' Budget Values are Incorrect')
            event.preventDefault();
        }
    }
     function calculateNights() {
            var arrivalDate = new Date(arrivalDateInput.value);
            var departureDate = new Date(departureDateInput.value);

            if (arrivalDate && departureDate) {
                const timeDiff = departureDate - arrivalDate;
                const nights = timeDiff / (1000 * 60 * 60 * 24);

                if (!isNaN(nights) && nights > 0) {
                    nightsDisplay.value = nights;
                } else {
                    nightsDisplay.value = 0;
                }
            }
        }
    if(arrivalDateInput){
        arrivalDateInput.addEventListener("change", calculateNights);
        departureDateInput.addEventListener("change", calculateNights);
    }

    if (submitButton) {
        submitButton.addEventListener('click', function(event) {
            if (adultPersonsInput) {
                validateNegativeValue(adultPersonsInput,"Adult Count");
            }
            if (childInput) {
                validateNegativeValue(childInput,"Child Count");
            }
            if (preferStartDate && preferEndDate) {
                validateTripDates(preferStartDate, preferEndDate);
            }
            if(noOfRoomInput){
                validateNegativeValue(noOfRoomInput,'Room Count')
            }
            if(mobileInput){
                validateMobile(mobileInput)
            }
            if(hotelBudgetMin || hotelBudgetMax){                   // Checks for trip budget
                validateNegativeValue(hotelBudgetMin,'Hotel Budget Minimum')
                validateNegativeValue(hotelBudgetMax,'Hotel Budget Maximum')
                validateBudget(hotelBudgetMin,hotelBudgetMax,'Hotel')
            }

//            event.preventDefault();
        });
    }
    if (submitButtonBooking) {
        submitButtonBooking.addEventListener('click', function(event) {
            if (arrivalDateBooking || departureDateBooking){
                validateTripDates(arrivalDateBooking,departureDateBooking);
            }
            if (numRoomsBooking) {
                validateNegativeValue(numRoomsBooking,"Rooms Count");
            }
            if (adultsBooking) {
                validateNegativeValue(adultsBooking,"Adult Count");
            }
            if (childBooking) {
                validateNegativeValue(childBooking,"Child Count");
            }
            if (infantsBooking) {
                validateNegativeValue(infantsBooking,"Infant Count");
            }
        });
    }
});
