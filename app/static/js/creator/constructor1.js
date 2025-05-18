let widgetCounter = 0;


//....................................РАБОТА С ВИДЖЕТАМ....................................


function addWidget(type) {
    widgetCounter++;
    const widgetsArea = document.getElementById('widgetsArea');
    let widgetHtml = '';
    
    switch(type) {
        case 'answer':
            widgetHtml = `
                <div class="widget-container" id="widget-${widgetCounter}">
                    <h5>Поле ввода для ответа</h5>
                    <div class="mb-3">
                        <label for="correctAnswer-${widgetCounter}" class="form-label">Правильный ответ</label>
                        <input type="text" class="form-control" id="correctAnswer-${widgetCounter}" placeholder="Введите правильный ответ">
                    </div>
                    <button class="btn btn-danger btn-sm mb-2" onclick="removeWidget(${widgetCounter})">Удалить виджет</button>
                </div>
            `;
            break;
            
        case 'text':
            widgetHtml = `
                <div class="widget-container" id="widget-${widgetCounter}">
                    <h5>Поле ввода для текста</h5>
                    <div class="mb-3">
                        <label for="textInput-${widgetCounter}" class="form-label">Новое условие для задания</label>
                        <textarea class="form-control" id="textInput-${widgetCounter}" rows="3" placeholder="Введите новое условие"></textarea>
                    </div>
                    <button class="btn btn-danger btn-sm mb-2" onclick="removeWidget(${widgetCounter})">Удалить виджет</button>
                </div>
            `;
            break;
            
        case 'select':
            widgetHtml = `
                <div class="widget-container" id="widget-${widgetCounter}">
                    <h5>Контейнер создания выбора</h5>
                    <div id="selectOptions-${widgetCounter}">
                        <!-- Варианты будут добавляться сюда -->
                    </div>
                    <button class="btn btn-success btn-sm mb-2" onclick="addSelectOption(${widgetCounter})">Добавить вариант</button>
                    <button class="btn btn-danger btn-sm mb-2" onclick="removeWidget(${widgetCounter})">Удалить виджет</button>
                </div>
            `;
            break;
            
        case 'checkbox':
            widgetHtml = `
                <div class="widget-container" id="widget-${widgetCounter}">
                    <h5>Контейнер вариантов ответа</h5>
                    <div id="checkboxOptions-${widgetCounter}">
                        <!-- Варианты будут добавляться сюда -->
                    </div>
                    <button class="btn btn-success btn-sm mb-2" onclick="addCheckboxOption(${widgetCounter})">Добавить вариант ответа</button>
                    <button class="btn btn-danger btn-sm mb-2" onclick="removeWidget(${widgetCounter})">Удалить виджет</button>
                </div>
            `;
            break;
    }
    
    widgetsArea.insertAdjacentHTML('beforeend', widgetHtml);
    
    // Если это виджет с выбором или чекбоксом, добавляем первый вариант по умолчанию
    if (type === 'select') {
        addSelectOption(widgetCounter);
    } else if (type === 'checkbox') {
        addCheckboxOption(widgetCounter);
    }
    
    // Закрываем модальное окно
    const modal = bootstrap.Modal.getInstance(document.getElementById('widgetModal'));
    modal.hide();
}

function addSelectOption(widgetId) {
    const optionId = Date.now(); // Уникальный ID для варианта
    const optionsContainer = document.getElementById(`selectOptions-${widgetId}`);
    
    const optionHtml = `
        <div class="option-container" id="option-${optionId}">
            <input type="text" class="form-control" placeholder="Введите вариант ответа">
            <div class="form-check ms-2 me-3">
                <input class="form-check-input" type="checkbox" id="correct-${optionId}">
                <label class="form-check-label" for="correct-${optionId}">Правильный</label>
            </div>
            <button class="btn btn-outline-danger remove-btn" onclick="removeOption(${optionId})">Удалить</button>
        </div>
    `;
    
    optionsContainer.insertAdjacentHTML('beforeend', optionHtml);
}

function addCheckboxOption(widgetId) {
    const optionId = Date.now(); // Уникальный ID для варианта
    const optionsContainer = document.getElementById(`checkboxOptions-${widgetId}`);
    
    const optionHtml = `
        <div class="option-container" id="option-${optionId}">
            <input type="text" class="form-control" placeholder="Введите вариант ответа">
            <div class="form-check ms-2 me-3">
                <input class="form-check-input" type="checkbox" id="correct-${optionId}">
                <label class="form-check-label" for="correct-${optionId}">Правильный</label>
            </div>
            <button class="btn btn-outline-danger remove-btn" onclick="removeOption(${optionId})">Удалить</button>
        </div>
    `;
    
    optionsContainer.insertAdjacentHTML('beforeend', optionHtml);
}

function removeOption(optionId) {
    const optionElement = document.getElementById(`option-${optionId}`);
    if (optionElement) {
        optionElement.remove();
    }
}

function removeWidget(widgetId) {
    const widgetElement = document.getElementById(`widget-${widgetId}`);
    if (widgetElement) {
        widgetElement.remove();
    }
}


//....................................ОТПРАВКА НА СЕРВЕР....................................

function collectWidgets() {
    const widgets = [];
    
    document.querySelectorAll('.widget-container').forEach(widget => {
        const widgetType = widget.querySelector('h5').textContent;
        const widgetData = {};
        
        if (widgetType.includes('Поле ввода для текста')) {
            widgets.push({
                type: 'text',
                data: {
                    text: widget.querySelector('textarea').value
                }
            });
        }
        else if (widgetType.includes('Поле ввода для ответа')) {
            widgets.push({
                type: 'answer',
                data: {
                    correct_answer: widget.querySelector('input[type="text"]').value
                }
            });
        }
        else if (widgetType.includes('Контейнер создания выбора')) {
            const options = [];
            widget.querySelectorAll('.option-container').forEach(option => {
                options.push({
                    text: option.querySelector('input[type="text"]').value,
                    is_correct: option.querySelector('input[type="checkbox"]').checked
                });
            });
            
            widgets.push({
                type: 'select',
                data: { options }
            });
        }
        else if (widgetType.includes('Контейнер вариантов ответа')) {
            const options = [];
            widget.querySelectorAll('.option-container').forEach(option => {
                options.push({
                    text: option.querySelector('input[type="text"]').value,
                    is_correct: option.querySelector('input[type="checkbox"]').checked
                });
            });
            
            widgets.push({
                type: 'checkbox',
                data: { options }
            });
        }
    });
    
    return widgets;
}


document.getElementById('submitServer').addEventListener('click', async function(e) {
    e.preventDefault(); // Предотвращаем стандартную отправку формы
    
    const taskTitle = document.getElementById('taskTitle').value;
    const widgets = collectWidgets();
    
    if (!taskTitle) {
        alert('Введите название задания!');
        return;
    }

    if (widgets.length === 0) {
        alert('Добавьте хотя бы один виджет перед отправкой!');
        return;
    }

    // Проверка заполненности всех полей виджетов
    let isValid = true;
    let errorMessage = '';
    
    document.querySelectorAll('.widget-container').forEach(widget => {
        const widgetType = widget.querySelector('h5').textContent;
        
        if (widgetType.includes('Поле ввода для текста')) {
            const text = widget.querySelector('textarea').value.trim();
            if (!text) {
                isValid = false;
                errorMessage = 'Заполните все текстовые поля!';
            }
        }
        else if (widgetType.includes('Поле ввода для ответа')) {
            const answer = widget.querySelector('input[type="text"]').value.trim();
            if (!answer) {
                isValid = false;
                errorMessage = 'Заполните все поля для ответа!';
            }
        }
        else if (widgetType.includes('Контейнер создания выбора')) {
            widget.querySelectorAll('.option-container input[type="text"]').forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    errorMessage = 'Заполните все варианты выбора!';
                }
            });
        }
        else if (widgetType.includes('Контейнер вариантов ответа')) {
            widget.querySelectorAll('.option-container input[type="text"]').forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    errorMessage = 'Заполните все варианты ответа!';
                }
            });
        }
    });
    
    if (!isValid) {
        alert(errorMessage);
        return;
    }

    try {
        const response = await fetch("{{ url_for('routes.get_widgets') }}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                taskTitle: taskTitle,
                widgets: widgets
            })
        });
        
        const result = await response.json();
        console.log('Server response:', result);
        alert('Данные успешно отправлены!');
        
        // Здесь можно добавить обработку ответа от сервера
        // Например, перенаправление на другую страницу или отображение результата
        
    } catch (error) {
        console.error('Error:', error);
        alert('Произошла ошибка при отправке данных');
    }
});