$(document).ready(function() {
    // 調用彈窗
    function loadModal(message) {
        // 檢查彈窗是否存在
        if ($('#myModal').length === 0) {
            $.get('/static/html/login_modal.html', function(data) {
                $('body').append(data);
                bindModalEvents();
                $('#modalMessage').html(message);
                $('#myModal').removeClass('hidden');
            });
        } else {
            $('#modalMessage').html(message);
            $('#myModal').removeClass('hidden');
        }
    }
    // console.log('login.js loaded');
    function bindModalEvents() {
        $('#closeModal').on('click', function() {
            $('#myModal').addClass('hidden');
            $('#username').val('admin');
            $('#password').val('password');
        });
    }

    // 是否顯示密碼
    $('#togglePassword').on('click', function() {
        const passwordField = $('#password');
        const eyeOffIcon = $(this).find('.eye-off');
        const eyeIcon = $(this).find('.eye');
        
        if (passwordField.attr('type') === 'password') {
            passwordField.attr('type', 'text');
            eyeOffIcon.addClass('hidden');
            eyeIcon.removeClass('hidden');
        } else {
            passwordField.attr('type', 'password');
            eyeIcon.addClass('hidden');
            eyeOffIcon.removeClass('hidden');
        }
    });

    // 登入
    $('#loginForm').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: '/login',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                username: $('#username').val(),
                password: $('#password').val()
            }),
            success: function(response) {
                if (response.success) {
                    // 存储token到cookie
                    document.cookie = "token=" + response.token + "; path=/";
                    window.location.href = '/agent_chat';
                } else {
                    $('#message').text(response.message).show();
                    loadModal(response.message);
                    setTimeout(function() {
                        $('#message').fadeOut();
                    }, 3000); // 显示3秒后隐藏
                }
                // Clear username and password fields
                $('#username').val('');
                $('#password').val('');
            },
            error: function(xhr) {
                $('#message').text(xhr.responseJSON.message).show();
                let Message = xhr.responseJSON.message + " , the correct account password has been automatically filled in for you";
                loadModal(Message);
                setTimeout(function() {
                    $('#message').fadeOut();
                }, 3000); // 显示3秒后隐藏
            }
        });
    });
});
