$(document).ready(function () {
    $('.register-form').submit(function (event) {
        event.preventDefault();
        
        const username = $('input[name="username"]').val();
        const password = $('input[name="password"]').val();
        const email = $('input[name="email"]').val();

        if (username.trim() === '' || password.trim() === '') {
            alert('Please fill in all fields.');
            return;
        }

        $.ajax({
            type: 'POST',
            url: '/register', 
            data: {
                username: username,
                password: password,
                email: email
            },
            success: function (response) {
                alert('Registration successful'); 
            },
            error: function () {
                alert('Registration failed');
            }
        });
    });
});
