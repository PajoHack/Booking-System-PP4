$(function () {
    $('#datetimepicker').timepicker({
        'timeFormat': 'HH:mm:ss',
        'minTime': '12:00pm',
        'maxTime': '9:00pm',
        'step': 30
    });

    const dateInput = document.querySelector('#date');
    const timeInput = document.querySelector('#datetimepicker');
    const message = document.querySelector('#message');
    const submitButton = document.querySelector('#submitButton');
    const tableCheckboxes = document.getElementsByName('tables');

    function checkAvailability() {
        message.textContent = '';
        submitButton.disabled = false;

        let checks = [];
        for (let i = 0; i < tableCheckboxes.length; i++) {
            if (tableCheckboxes[i].checked) {
                const tableId = tableCheckboxes[i].value;
                const date = dateInput.value;
                const time = timeInput.value;

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