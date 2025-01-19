document.addEventListener('DOMContentLoaded', function () {
    // Add event listeners to all collapse buttons
    document.querySelectorAll('.collapse-row-btn').forEach(function (button) {
        button.addEventListener('click', function () {
            const row = button.closest('.inline-related');
            if (row) {
                // Toggle the visibility of all fields in the row except the button
                row.querySelectorAll('.form-row').forEach(function (field) {
                    if (!field.contains(button)) {
                        field.style.display = field.style.display === 'none' ? '' : 'none';
                    }
                });
            }
        });
    });
});
