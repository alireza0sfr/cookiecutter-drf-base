document.addEventListener("DOMContentLoaded", function () {
    // Select all input fields that should have comma formatting
    const priceFields = document.querySelectorAll('.input-money');

    priceFields.forEach(function (field) {
        // Convert the input type to text for proper formatting with commas
        field.setAttribute('type', 'text');
        
        // Format the field with commas on load
        field.value = formatNumberWithCommas(field.value);

        // Listen for input changes and format as the user types
        field.addEventListener('input', function (event) {
            let value = event.target.value.replace(/,/g, ''); // Remove existing commas

            // If valid number, format it with commas
            if (isValidNumber(value)) {
                field.value = formatNumberWithCommas(value); // Add commas
            } else {
                // Remove the last invalid character but keep the first valid dot
                let validValue = value.slice(0, -1);
                if (isValidNumber(validValue)) {
                    field.value = formatNumberWithCommas(validValue); // Restore to the last valid state
                }
            }
        });
    });

    // Helper function to format numbers with commas
    function formatNumberWithCommas(value) {
        if (value === "") return value; // Prevent formatting on empty value

        // Split the value into integer and decimal parts (if any)
        const parts = value.split('.');
        const integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        
        // Return formatted number with decimal part if it exists
        return parts.length > 1 ? integerPart + '.' + parts[1] : integerPart;
    }

    // Helper function to check if input is a valid number
    function isValidNumber(value) {
        // Regular expression to allow only digits and a single dot for decimal
        const validNumberRegex = /^[0-9]*\.?[0-9]*$/;
        const dotCount = (value.match(/\./g) || []).length;

        // Ensure only one dot and numbers are allowed
        return validNumberRegex.test(value) && dotCount <= 1;
    }
});
