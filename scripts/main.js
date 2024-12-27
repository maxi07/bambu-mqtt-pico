const access_input = document.getElementById('accessCode');
const save_button = document.getElementById('submitForm');

access_input.addEventListener('input', () => {
    save_button.disabled = access_input.value.trim() === '';
});