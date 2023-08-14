$(document).ready(function () {
    $('#loginForm').submit(function (event) {
        event.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        
        if (username === '' || password === '') {
            alert('Username and password are required.');
            return;
        }
        
        $.ajax({
            type: 'POST',
            url: '/login',
          
            data: JSON.stringify({ 'username': username, 'password': password }),
            contentType: 'application/json',
            success: function (response) {
                alert('Login successful: ' + response);
            },
            error: function (xhr, status, error) {
                alert('Login failed: ' + error);
            }
        });
    });
});
