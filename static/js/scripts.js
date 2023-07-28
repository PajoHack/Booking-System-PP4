$(function () {
    // Initialize timepicker with specific format and restrictions
    $('#datetimepicker').timepicker({
        'timeFormat': 'HH:mm:ss',
        'minTime': '12:00pm',
        'maxTime': '9:00pm',
        'step': 30
    });

    // Grab relevant DOM elements
    const dateInput = document.querySelector('#date');
    const timeInput = document.querySelector('#datetimepicker');
    const message = document.querySelector('#message');
    const submitButton = document.querySelector('#submitButton');
    const tableCheckboxes = document.getElementsByName('tables');
    const bookingId = document.querySelector('#editMode').value;

    // Function to check the availability of selected tables
    function checkAvailability() {
        message.textContent = '';
        submitButton.disabled = false;
    
        const editMode = document.querySelector('#editMode').value !== '0';
        const bookingId = editMode ? document.querySelector('#editMode').value : null;
    
        let checks = [];
        for (let i = 0; i < tableCheckboxes.length; i++) {
            if (tableCheckboxes[i].checked) {
                const tableId = tableCheckboxes[i].value;
                const date = dateInput.value;
                const time = timeInput.value;
                
                // Fetch availability data from server and add to checks array
                checks.push(
                    fetch(`/check_availability?table_id=${tableId}&date=${date}&time=${time}&booking_id=${bookingId}`)
                        .then(response => response.json())
                        .then(data => {
                            if (!data.available) {
                                if (data.booked_by_current_user) {
                                    message.textContent += `You have already booked Table ${tableId} for the chosen date & time. `;
                                } else {
                                    message.textContent += `Table ${tableId} is not available for the chosen date & time. `;
                                }
                                return false; 
                            }
                            return true; 
                        })
                );
            }
        }

        // Once all checks are complete, update message and submit button status
        Promise.all(checks).then(results => {
            if (results.every(val => val === true) && results.length > 0) {
                message.textContent = "All selected tables are available!";
            } else {
                submitButton.disabled = true;
            }
        });
    }    

    // Add event listeners to trigger checkAvailability function
    for (let i = 0; i < tableCheckboxes.length; i++) {
        tableCheckboxes[i].addEventListener('change', checkAvailability);
    }
    dateInput.addEventListener('input', checkAvailability);
    timeInput.addEventListener('input', checkAvailability);

    // Poll every 5 seconds to keep availability data up-to-date
    setInterval(checkAvailability, 5000);
});
