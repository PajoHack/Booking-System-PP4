$(function () {
    $('#datetimepicker').timepicker({
        'timeFormat': 'h:mm p',
        'minTime': '12:00pm',
        'maxTime': '9:00pm',
        'step': 30
    });

    const dateInput = document.querySelector('#date');
    const timeInput = document.querySelector('#datetimepicker');
    const message = document.querySelector('#message');
    const submitButton = document.querySelector('#submitButton');
    const tableCheckboxes = document.getElementsByName('tables');
    const form = document.querySelector('#res-form');

    form.addEventListener('submit', function (e) {
        const timeParts = timeInput.value.split(" ");
        let [hours, minutes] = timeParts[0].split(":");
        if (timeParts[1].toLowerCase() === "pm" && hours != "12") {
            hours = parseInt(hours, 10) + 12;
        } else if (timeParts[1].toLowerCase() === "am" && hours == "12") {
            hours = "00";
        }
        const time = `${hours}:${minutes}:00`;

        timeInput.value = time; // set the time input to the new formatted time.
    });

    function checkAvailability() {
        message.textContent = '';
        submitButton.disabled = false;

        let checks = [];
        for (let i = 0; i < tableCheckboxes.length; i++) {
            if (tableCheckboxes[i].checked) {
                const tableId = tableCheckboxes[i].value;
                const date = dateInput.value;

                // Convert 12-hour time format to 24-hour time format
                const timeParts = timeInput.value.split(" ");
                let [hours, minutes] = timeParts[0].split(":");
                if (timeParts[1].toLowerCase() === "pm" && hours != "12") {
                    hours = parseInt(hours, 10) + 12;
                } else if (timeParts[1].toLowerCase() === "am" && hours == "12") {
                    hours = "00";
                }
                const time = `${hours}:${minutes}:00`; // Add seconds to match Django's TimeField format

                checks.push(
                    fetch(`/check_availability?table_id=${tableId}&date=${date}&time=${time}`)
                        .then(response => response.json())
                        .then(data => {
                            if (!data.available) {
                                message.textContent += `Table ${tableId} is not available for the chosen date & time. `;
                                return false; 
                            }
                            return true; 
                        })
                );
            }
        }

        Promise.all(checks).then(results => {
            if (results.every(val => val === true) && results.length > 0) {
                message.textContent = "All selected tables are available!";
            } else {
                submitButton.disabled = true;
            }
        });
    }

    for (let i = 0; i < tableCheckboxes.length; i++) {
        tableCheckboxes[i].addEventListener('change', checkAvailability);
    }
    dateInput.addEventListener('input', checkAvailability);
    timeInput.addEventListener('input', checkAvailability);

    // Poll every 5 seconds
    setInterval(checkAvailability, 3000);
});