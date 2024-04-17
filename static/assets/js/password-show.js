$(document).ready(function() {
    const password = $('#id_password');
    const hidePassword = $('#hidePassword');
    const showPassword = $('#showPassword');

    function togglePasswordVisibility() {
        const passwordType = password.attr('type');
        if (passwordType === 'password') {
            password.attr('type', 'text');
            hidePassword.addClass('hidden');
            showPassword.removeClass('hidden');
        } else {
            password.attr('type', 'password');
            showPassword.addClass('hidden');
            hidePassword.removeClass('hidden');
        }
    }

    hidePassword.on('click', togglePasswordVisibility);
    showPassword.on('click', togglePasswordVisibility);
});