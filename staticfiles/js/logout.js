function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function handleLogout() {
    const csrfToken = getCookie('csrftoken');
    const modal = bootstrap.Modal.getInstance(document.getElementById('logoutModal'));
    
    fetch('/logout/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        credentials: 'same-origin'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Logout failed');
    })
    .then(data => {
        if (data.success) {
            if (modal) {
                modal.hide();
            }
            window.location.href = data.redirect_url;
        } else {
            throw new Error(data.message || 'Logout failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (modal) {
            modal.hide();
        }
        showToast('An error occurred during logout. Please try again.', 'error');
    });
}
