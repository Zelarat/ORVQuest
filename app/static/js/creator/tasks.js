document.addEventListener('DOMContentLoaded', function() {
    // Обработчик для кнопки просмотра
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const taskId = this.getAttribute('data-task-id');
            window.location.href = `/admin/tasks/${taskId}/view`;
        });
    });

    // Обработчик для кнопки редактирования
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const taskId = this.getAttribute('data-task-id');
            window.location.href = `/admin/tasks/${taskId}/edit`;
        });
    });

    // Обработчик для кнопки удаления (с подтверждением)
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const taskId = this.getAttribute('data-task-id');
            if (confirm('Вы уверены, что хотите удалить это задание?')) {
                fetch(`/admin/tasks/${taskId}/delete`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrf_token]').value
                    }
                }).then(response => {
                    if (response.ok) {
                        window.location.reload();
                    }
                });
            }
        });
    });
});

function openModal() {
    var myModal = new bootstrap.Modal(document.getElementById('myModal'));
    myModal.show();
}

function closeModal() {
    var myModal = bootstrap.Modal.getInstance(document.getElementById('myModal'));
    myModal.hide();
}
