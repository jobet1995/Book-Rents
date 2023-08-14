$(document).ready(function () {
    $('.login-form').submit(function (event) {
        event.preventDefault();
        
        const username = $('input[name="username"]').val();
        const password = $('input[name="password"]').val();

        if (username.trim() === '' || password.trim() === '') {
            alert('Please fill in all fields.');
            return;
        }

        $.ajax({
            type: 'POST',
            url: '/login',
          
            data: {
                username: username,
                password: password
            },
            success: function (response) {
                alert('Login successful'); 
              
            },
            error: function () {
                alert('Login failed');
              q
            }
        });
    });
});