let widgetCounter = 0;
let fileCounter = 0;
let files = []

function addWidget(type) {
    widgetCounter++;
    const widgetsArea = document.getElementById('widgetsArea');
    let widgetHtml = '';
    
    switch(type) {
        case 'written_answer':
            widgetHtml = `
                <div class="widget-container" id="widget-${widgetCounter}">
                    <h5 class="mb-3">Письменный ответ</h5>
                    <div class="mb-3">
                        <label for="question-${widgetCounter}" class="form-label">Условие задания</label>
                        <textarea class="form-control" id="question-${widgetCounter}" rows="3" placeholder="Введите условие задания"></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Кол-во баллов за правильный ответ</label>
                        <input class="form-control mb-3" type="number" min="0" step="1" id="points" placeholder="Введите кол-во баллов за задание">
                    </div>
                    <div class="form-check mb-3">
                        <input class="form-check-input" type="checkbox" id="serverCheck-${widgetCounter}" onchange="toggleCorrectAnswer(${widgetCounter})">
                        <label class="form-check-label" for="serverCheck-${widgetCounter}">Проверка сервером</label>
                    </div>
                    <div id="correctAnswerContainer-${widgetCounter}" class="mb-3 hidden">
                        <label for="correctAnswer-${widgetCounter}" class="form-label">Правильный ответ</label>
                        <input type="text" class="form-control" id="correctAnswer" placeholder="Введите правильный ответ">
                    </div>
                    <button class="btn btn-danger btn-sm mb-2" onclick="removeWidget(${widgetCounter})">Удалить виджет</button>
                </div>
            `;
            break;
            
        case 'select':
            widgetHtml = `
                <div class="widget-container" id="widget-${widgetCounter}">
                    <h5>Варианты ответов</h5>
                    <div class="mb-3">
                        <label for="question-${widgetCounter}" class="form-label">Условие задания</label>
                        <textarea class="form-control" id="question-${widgetCounter}" rows="3" placeholder="Введите условие задания"></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Кол-во баллов за правильный ответ</label>
                        <input class="form-control mb-3" type="number" min="0" step="1" id="points" placeholder="Введите кол-во баллов за задание">
                    </div>
                    <div id="selectOptions-${widgetCounter}"></div>
                    <button class="btn btn-success btn-sm mb-2" onclick="addSelectOption(${widgetCounter})">Добавить вариант</button>
                    <button class="btn btn-danger btn-sm mb-2" onclick="removeWidget(${widgetCounter})">Удалить виджет</button>
                </div>
            `;
            break;
            
        case 'checkbox':
            widgetHtml = `
                <div class="widget-container" id="widget-${widgetCounter}">
                    <h5>Чекбоксы</h5>
                    <div class="mb-3">
                        <label for="question-${widgetCounter}" class="form-label">Условие задания</label>
                        <textarea class="form-control" id="question-${widgetCounter}" rows="3" placeholder="Введите условие задания"></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Кол-во баллов за правильный ответ</label>
                        <input class="form-control mb-3" type="number" min="0" step="1" id="points" placeholder="Введите кол-во баллов за задание">
                    </div>
                    <div id="checkboxOptions-${widgetCounter}"></div>
                    <button class="btn btn-success btn-sm mb-2" onclick="addCheckboxOption(${widgetCounter})">Добавить вариант ответа</button>
                    <button class="btn btn-danger btn-sm mb-2" onclick="removeWidget(${widgetCounter})">Удалить виджет</button>
                </div>
            `;
            break;
            
        case 'file':
            widgetHtml = `
                <div class="widget-container" id="widget-${widgetCounter}">
                    <h5>Загрузка файлов</h5>
                    <div class="mb-3">
                        <label for="question-${widgetCounter}" class="form-label">Условие задания</label>
                        <textarea class="form-control" id="question-${widgetCounter}" rows="3" placeholder="Введите условие задания"></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Кол-во баллов за правильный ответ</label>
                        <input class="form-control mb-3" type="number" min="0" step="1" id="points" placeholder="Введите кол-во баллов за задание">
                    </div>
                    <div class="file-upload-container mb-3">
                        <label class="form-label">Файл 1</label>
                        <div class="d-flex align-items-center mb-2">
                            <span class="file-name me-2">Файл не выбран</span>
                            <button type="button" class="btn btn-sm btn-primary" onclick="document.getElementById('fileInput-${widgetCounter}-0').click()">Выбрать файл</button>
                            <input type="file" id="fileInput-${widgetCounter}-0" class="d-none" onchange="handleFileSelect(${widgetCounter}, 0, this)">
                        </div>
                        <div class="file-answers-container"></div>
                        <button class="btn btn-success btn-sm mb-2" onclick="addFileAnswerOption(${widgetCounter}, 0)">Добавить вариант ответа</button>
                    </div>
                    <button class="btn btn-success btn-sm mb-2" onclick="addFileUpload(${widgetCounter})">Добавить ещё файл</button>
                    <button class="btn btn-danger btn-sm mb-2" onclick="removeWidget(${widgetCounter})">Удалить виджет</button>
                </div>
            `;
            fileCounter = 1;
            break;
    }
    
    widgetsArea.insertAdjacentHTML('beforeend', widgetHtml);
    
    if (type === 'select') {
        addSelectOption(widgetCounter);
    }
    if (type === 'checkbox') {
        addCheckboxOption(widgetCounter);
    }
    if (type === 'file') {
        addFileAnswerOption(widgetCounter, 0);
    }
    
    const modal = bootstrap.Modal.getInstance(document.getElementById('widgetModal'));
    modal.hide();
}
    
function toggleCorrectAnswer(widgetId) {
    const checkbox = document.getElementById(`serverCheck-${widgetId}`);
    const container = document.getElementById(`correctAnswerContainer-${widgetId}`);
    
    if (checkbox.checked) {
        container.classList.remove('hidden');
    } else {
        container.classList.add('hidden');
    }
}

function addSelectOption(widgetId) {
    const optionId = Date.now();
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
    const optionId = Date.now();
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

function addFileAnswerOption(widgetId, fileIndex) {
    const optionId = Date.now();
    const widget = document.getElementById(`widget-${widgetId}`);
    const answersContainers = widget.querySelectorAll('.file-answers-container');
    const answersContainer = answersContainers[fileIndex];
    
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
    
    
    answersContainer.insertAdjacentHTML('beforeend', optionHtml);
}

function addFileUpload(widgetId) {
    const widget = document.getElementById(`widget-${widgetId}`);
    const fileIndex = widget.querySelectorAll('.file-upload-container').length;
    
    const fileHtml = `
        <div class="file-upload-container">
            <label class="form-label">Файл ${fileIndex + 1}</label>
            <div class="d-flex align-items-center mb-2">
                <span class="file-name me-2">Файл не выбран</span>
                <button type="button" class="btn btn-sm btn-primary" onclick="document.getElementById('fileInput-${widgetId}-${fileIndex}').click()">Выбрать файл</button>
                <input type="file" id="fileInput-${widgetId}-${fileIndex}" class="d-none" onchange="handleFileSelect(${widgetId}, ${fileIndex}, this)">
            </div>
            <div class="file-answers-container"></div>
            <button class="btn btn-success btn-sm mb-2" onclick="addFileAnswerOption(${widgetId}, ${fileIndex})">Добавить вариант ответа</button>
        </div>
    `;
    
    const addFileButton = widget.querySelector('button[onclick^="addFileUpload"]');
    addFileButton.insertAdjacentHTML('beforebegin', fileHtml);
    addFileAnswerOption(widgetCounter, fileIndex)
}
        
function handleFileSelect(widgetId, fileIndex, input) {
    const widget = document.getElementById(`widget-${widgetId}`);
    const fileContainers = widget.querySelectorAll('.file-upload-container');
    const fileContainer = fileContainers[fileIndex];

    if (input.files.length > 0) {
        const file = input.files[0];
        console.log(file);
        fileContainer.querySelector('.file-name').textContent = file.name;
    }
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

// Функция для сбора данных виджетов перед отправкой
function collectWidgets() {
    const widgets = [];
    
    document.querySelectorAll('.widget-container').forEach(widget => {
        const widgetType = widget.querySelector('h5').textContent;
        const widgetData = {};
        
        if (widgetType.includes('Письменный ответ')) {
            widgetData.type = 'written_answer';
            widgetData.points = widget.querySelector('input[type="number"]').value;
            widgetData.data = {
                question: widget.querySelector('textarea').value,
                server_check: widget.querySelector('input[type="checkbox"]').checked
            };
            
            if (widgetData.data.server_check) {
                widgetData.data.correct_answer = widget.querySelector('#correctAnswer').value;
            }
        }
        else if (widgetType.includes('Варианты ответов')) {
            widgetData.type = 'select';
            widgetData.points = widget.querySelector('input[type="number"]').value;
            widgetData.data = {
                question: widget.querySelector('textarea').value,
                options: []
            };
            
            widget.querySelectorAll('.option-container').forEach(option => {
                widgetData.data.options.push({
                    text: option.querySelector('input[type="text"]').value,
                    is_correct: option.querySelector('input[type="checkbox"]').checked
                });
            });
        }
        else if (widgetType.includes('Чекбоксы')) {
            widgetData.type = 'checkbox';
            widgetData.points = widget.querySelector('input[type="number"]').value;
            widgetData.data = {
                question: widget.querySelector('textarea').value,
                options: []
            };
            
            widget.querySelectorAll('.option-container').forEach(option => {
                widgetData.data.options.push({
                    text: option.querySelector('input[type="text"]').value,
                    is_correct: option.querySelector('input[type="checkbox"]').checked
                });
            });
        }
        else if (widgetType.includes('Загрузка файлов')) {
            widgetData.type = 'file';
            widgetData.points = widget.querySelector('input[type="number"]').value;
            widgetData.data = {
                question: widget.querySelector('textarea').value,
                files: []
            };
            
            widget.querySelectorAll('input[type="file"]').forEach((input, index) => {
                const fileData = {
                    name: input.files[0].name,
                    file: input.id,
                    options: []
                };
                
                const answersContainer = widget.querySelectorAll('.file-answers-container')[index];
                answersContainer.querySelectorAll('.option-container').forEach(option => {
                    fileData.options.push({
                        text: option.querySelector('input[type="text"]').value,
                        is_correct: option.querySelector('input[type="checkbox"]').checked
                    });
                });
                
                widgetData.data.files.push(fileData);
            });
        }
        
        widgets.push(widgetData);
    });
    
    return widgets;
}

document.getElementById('submitServer').addEventListener('click', async function(e) {
    e.preventDefault();
    
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
        
        if (widgetType.includes('Письменный ответ')) {
            const question = widget.querySelector('textarea').value.trim();
            if (!question) {
                isValid = false;
                errorMessage = 'Заполните условие задания для письменного ответа!';
            }
            
            if (widget.querySelector('input[type="checkbox"]').checked) {
                const answer = widget.querySelector('#correctAnswer').value.trim();
                if (!answer) {
                    isValid = false;
                    errorMessage = 'Заполните правильный ответ для письменного ответа!';
                }
            }
        }
        else if (widgetType.includes('Варианты ответов') || widgetType.includes('Чекбоксы')) {
            const question = widget.querySelector('textarea').value.trim();
            if (!question) {
                isValid = false;
                errorMessage = 'Заполните условие задания!';
            }
            
            const options = widget.querySelectorAll('.option-container input[type="text"]');
            if (options.length === 0) {
                isValid = false;
                errorMessage = 'Добавьте хотя бы один вариант ответа!';
            }
            
            options.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    errorMessage = 'Заполните все варианты ответов!';
                }
            });
            
            // Проверка, что выбран хотя бы один правильный вариант
            if (widgetType.includes('Варианты ответов')) {
                const checkedOptions = widget.querySelectorAll('.option-container input[type="checkbox"]:checked');
                if (checkedOptions.length === 0) {
                    isValid = false;
                    errorMessage = 'Выберите хотя бы один правильный вариант ответа!';
                }
            }
        }
        else if (widgetType.includes('Загрузка файлов')) {
            const question = widget.querySelector('textarea').value.trim();
            if (!question) {
                isValid = false;
                errorMessage = 'Заполните условие задания для загрузки файлов!';
            }
            
            const fileContainers = widget.querySelectorAll('.file-upload-container');
            if (fileContainers.length === 0) {
                isValid = false;
                errorMessage = 'Добавьте хотя бы один файл!';
            }
            
            fileContainers.forEach(container => {
                const fileName = container.querySelector('.file-name').textContent;
                if (fileName === 'Файл не выбран') {
                    isValid = false;
                    errorMessage = 'Выберите все файлы!';
                }
                
                const answersContainer = container.querySelector('.file-answers-container');
                console.log(answersContainer);
                if (answersContainer) {
                    const options = answersContainer.querySelectorAll('.option-container input[type="text"]');
                    console.log('true');
                    if (options.length === 0) {
                        isValid = false;
                        errorMessage = 'Добавьте хотя бы один вариант ответа для каждого файла!';
                    }
                    
                    options.forEach(input => {
                        if (!input.value.trim()) {
                            isValid = false;
                            errorMessage = 'Заполните все варианты ответов для файлов!';
                        }
                    });
                }
                else {
                    console.log("False")
                };
            });
        }
    });
    
    if (!isValid) {
        alert(errorMessage);
        return;
    }

    try {


        const response = await fetch(getWidgetsUrl, {
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
        
        //window.location.href = back
        
    } catch (error) {
        console.error('Error:', error);
        alert('Произошла ошибка при отправке данных');
    }
});