/**
 * Sistema de Formulários Mobile Otimizados
 * Melhora a experiência de preenchimento de formulários em dispositivos móveis
 */

class MobileForms {
    constructor() {
        this.isMobile = window.innerWidth <= 768;
        this.isSmallMobile = window.innerWidth <= 576;
        this.init();
    }

    init() {
        this.enhanceFormInputs();
        this.improveValidation();
        this.addMobileKeyboards();
        this.enhanceFileInputs();
        this.improveSelectElements();
        this.addFormNavigation();
        this.setupEventListeners();
    }

    enhanceFormInputs() {
        const inputs = document.querySelectorAll('.form-control, .form-select');
        
        inputs.forEach(input => {
            // Melhorar área de toque
            if (this.isMobile) {
                input.style.minHeight = '50px';
                input.style.fontSize = '16px'; // Previne zoom no iOS
                input.style.borderRadius = '12px';
                input.style.padding = '1rem';
            }

            // Adicionar indicadores visuais de foco
            input.addEventListener('focus', function() {
                this.style.transform = 'scale(1.02)';
                this.style.boxShadow = '0 0 0 3px var(--accent-100)';
                this.style.borderColor = 'var(--accent)';
                
                // Scroll suave para o campo em foco
                if (window.innerWidth <= 768) {
                    setTimeout(() => {
                        this.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'center',
                            inline: 'nearest'
                        });
                    }, 100);
                }
            });

            input.addEventListener('blur', function() {
                this.style.transform = '';
                this.style.boxShadow = '';
                this.style.borderColor = '';
            });

            // Melhorar feedback visual para campos obrigatórios
            if (input.hasAttribute('required')) {
                const label = document.querySelector(`label[for="${input.id}"]`) || 
                             input.closest('.form-group')?.querySelector('label');
                
                if (label && !label.querySelector('.required-indicator')) {
                    const indicator = document.createElement('span');
                    indicator.className = 'required-indicator text-danger ms-1';
                    indicator.innerHTML = '*';
                    indicator.style.fontSize = '1.2em';
                    label.appendChild(indicator);
                }
            }
        });
    }

    addMobileKeyboards() {
        // Otimizar teclados móveis para diferentes tipos de entrada
        const inputMappings = {
            'email': 'email',
            'tel': 'tel',
            'url': 'url',
            'number': 'numeric',
            'search': 'search'
        };

        document.querySelectorAll('input').forEach(input => {
            const type = input.type;
            
            if (inputMappings[type]) {
                input.setAttribute('inputmode', inputMappings[type]);
            }

            // Campos específicos por nome/id
            if (input.name?.includes('phone') || input.name?.includes('telefone')) {
                input.setAttribute('inputmode', 'tel');
                input.setAttribute('pattern', '[0-9]*');
            }

            if (input.name?.includes('cep') || input.name?.includes('zip')) {
                input.setAttribute('inputmode', 'numeric');
                input.setAttribute('pattern', '[0-9]*');
            }

            if (input.name?.includes('cpf') || input.name?.includes('cnpj')) {
                input.setAttribute('inputmode', 'numeric');
            }
        });
    }

    improveValidation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            // Validação em tempo real mais suave
            const inputs = form.querySelectorAll('.form-control, .form-select');
            
            inputs.forEach(input => {
                // Remover validação visual agressiva
                input.addEventListener('invalid', function(e) {
                    e.preventDefault();
                    this.classList.add('is-invalid-soft');
                    this.classList.remove('is-valid');
                });

                input.addEventListener('input', function() {
                    if (this.validity.valid) {
                        this.classList.remove('is-invalid-soft');
                        this.classList.add('is-valid-soft');
                    }
                });

                // Validação mais amigável no blur
                input.addEventListener('blur', function() {
                    if (this.value && !this.validity.valid) {
                        this.classList.add('is-invalid-soft');
                        this.classList.remove('is-valid-soft');
                        this.showCustomValidationMessage();
                    }
                });
            });

            // Melhorar mensagens de erro
            form.addEventListener('submit', function(e) {
                const invalidInputs = form.querySelectorAll(':invalid');
                
                if (invalidInputs.length > 0) {
                    e.preventDefault();
                    
                    // Focar no primeiro campo inválido
                    const firstInvalid = invalidInputs[0];
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'center' 
                    });

                    // Mostrar toast com erro geral
                    this.showFormErrorToast('Por favor, corrija os campos destacados');
                }
            });
        });
    }

    enhanceFileInputs() {
        const fileInputs = document.querySelectorAll('input[type="file"]');
        
        fileInputs.forEach(input => {
            // Criar área de drop mais amigável para mobile
            const wrapper = document.createElement('div');
            wrapper.className = 'file-input-wrapper mobile-friendly';
            wrapper.style.cssText = `
                border: 2px dashed var(--gray-300);
                border-radius: 12px;
                padding: 2rem 1rem;
                text-align: center;
                background: var(--gray-50);
                transition: all 0.3s ease;
                cursor: pointer;
                min-height: 120px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 1rem;
            `;

            const icon = document.createElement('i');
            icon.className = 'bi bi-cloud-upload fs-1 text-primary';
            
            const text = document.createElement('p');
            text.className = 'mb-0 text-muted';
            text.innerHTML = 'Toque para selecionar<br><small>ou arraste o arquivo aqui</small>';

            wrapper.appendChild(icon);
            wrapper.appendChild(text);

            input.style.display = 'none';
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);

            wrapper.addEventListener('click', () => input.click());

            // Feedback visual para drag & drop
            wrapper.addEventListener('dragover', function(e) {
                e.preventDefault();
                this.style.borderColor = 'var(--accent)';
                this.style.background = 'var(--accent-50)';
            });

            wrapper.addEventListener('dragleave', function() {
                this.style.borderColor = 'var(--gray-300)';
                this.style.background = 'var(--gray-50)';
            });

            wrapper.addEventListener('drop', function(e) {
                e.preventDefault();
                this.style.borderColor = 'var(--gray-300)';
                this.style.background = 'var(--gray-50)';
                
                if (e.dataTransfer.files.length > 0) {
                    input.files = e.dataTransfer.files;
                    this.updateFileDisplay();
                }
            });

            input.addEventListener('change', function() {
                wrapper.updateFileDisplay();
            });

            wrapper.updateFileDisplay = function() {
                if (input.files.length > 0) {
                    const fileName = input.files[0].name;
                    text.innerHTML = `<strong>${fileName}</strong><br><small>Arquivo selecionado</small>`;
                    icon.className = 'bi bi-check-circle fs-1 text-success';
                    this.style.borderColor = 'var(--success)';
                    this.style.background = 'var(--success-light)';
                }
            };
        });
    }

    improveSelectElements() {
        const selects = document.querySelectorAll('.form-select');
        
        selects.forEach(select => {
            if (this.isMobile) {
                // Melhorar aparência visual
                select.style.minHeight = '50px';
                select.style.fontSize = '16px';
                select.style.borderRadius = '12px';
                select.style.padding = '1rem';
                
                // Adicionar ícone customizado
                const wrapper = document.createElement('div');
                wrapper.className = 'select-wrapper position-relative';
                select.parentNode.insertBefore(wrapper, select);
                wrapper.appendChild(select);
                
                const icon = document.createElement('i');
                icon.className = 'bi bi-chevron-down position-absolute';
                icon.style.cssText = `
                    right: 1rem;
                    top: 50%;
                    transform: translateY(-50%);
                    pointer-events: none;
                    color: var(--gray-500);
                    font-size: 0.9rem;
                `;
                wrapper.appendChild(icon);
                
                select.style.appearance = 'none';
                select.style.paddingRight = '3rem';
            }
        });
    }

    addFormNavigation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('.form-control, .form-select');
            
            if (inputs.length > 3 && this.isMobile) {
                // Adicionar navegação entre campos
                inputs.forEach((input, index) => {
                    // Adicionar botão "próximo" no teclado móvel
                    if (index < inputs.length - 1) {
                        input.addEventListener('keydown', function(e) {
                            if (e.key === 'Enter' && this.type !== 'textarea') {
                                e.preventDefault();
                                inputs[index + 1].focus();
                            }
                        });
                    }
                });

                // Adicionar indicador de progresso
                this.addFormProgress(form, inputs);
            }
        });
    }

    addFormProgress(form, inputs) {
        const progressBar = document.createElement('div');
        progressBar.className = 'form-progress mb-3';
        progressBar.style.cssText = `
            height: 4px;
            background: var(--gray-200);
            border-radius: 2px;
            overflow: hidden;
        `;

        const progressFill = document.createElement('div');
        progressFill.className = 'form-progress-fill';
        progressFill.style.cssText = `
            height: 100%;
            background: linear-gradient(90deg, var(--accent), var(--accent-light));
            width: 0%;
            transition: width 0.3s ease;
            border-radius: 2px;
        `;

        progressBar.appendChild(progressFill);
        form.insertBefore(progressBar, form.firstChild);

        // Atualizar progresso
        function updateProgress() {
            const filledInputs = Array.from(inputs).filter(input => {
                return input.value.trim() !== '' || input.type === 'checkbox' && input.checked;
            });
            
            const progress = (filledInputs.length / inputs.length) * 100;
            progressFill.style.width = progress + '%';
        }

        inputs.forEach(input => {
            input.addEventListener('input', updateProgress);
            input.addEventListener('change', updateProgress);
        });

        updateProgress();
    }

    setupEventListeners() {
        // Redimensionamento da janela
        window.addEventListener('resize', () => {
            this.isMobile = window.innerWidth <= 768;
            this.isSmallMobile = window.innerWidth <= 576;
        });

        // Melhorar experiência com teclado virtual
        if ('visualViewport' in window) {
            window.visualViewport.addEventListener('resize', () => {
                const viewport = window.visualViewport;
                const activeElement = document.activeElement;
                
                if (activeElement && activeElement.matches('.form-control, .form-select')) {
                    // Ajustar layout quando teclado virtual aparece
                    document.body.style.paddingBottom = (window.innerHeight - viewport.height) + 'px';
                }
            });
        }
    }

    showFormErrorToast(message) {
        // Criar toast de erro amigável
        const toast = document.createElement('div');
        toast.className = 'mobile-toast error show';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--danger);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-size: 0.9rem;
            font-weight: 500;
            z-index: 9999;
            box-shadow: var(--shadow-lg);
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Método estático para inicialização manual
    static init() {
        return new MobileForms();
    }
}

// Adicionar extensão para inputs com validação customizada
HTMLInputElement.prototype.showCustomValidationMessage = function() {
    const messages = {
        valueMissing: 'Este campo é obrigatório',
        typeMismatch: {
            email: 'Por favor, insira um email válido',
            url: 'Por favor, insira uma URL válida'
        },
        patternMismatch: 'O formato inserido não é válido',
        tooShort: `Mínimo de ${this.minLength} caracteres`,
        tooLong: `Máximo de ${this.maxLength} caracteres`,
        rangeUnderflow: `Valor mínimo: ${this.min}`,
        rangeOverflow: `Valor máximo: ${this.max}`,
        stepMismatch: 'Valor não permitido',
        badInput: 'Entrada inválida'
    };

    let message = 'Campo inválido';
    
    for (let error in messages) {
        if (this.validity[error]) {
            if (typeof messages[error] === 'object') {
                message = messages[error][this.type] || message;
            } else {
                message = messages[error];
            }
            break;
        }
    }

    // Mostrar mensagem próxima ao campo
    let errorElement = this.parentElement.querySelector('.custom-error-message');
    
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'custom-error-message invalid-feedback d-block';
        errorElement.style.cssText = `
            font-size: 0.8rem;
            color: var(--danger);
            margin-top: 0.25rem;
            animation: fadeIn 0.3s ease;
        `;
        this.parentElement.appendChild(errorElement);
    }
    
    errorElement.textContent = message;
    
    // Remover mensagem quando campo se tornar válido
    const removeMessage = () => {
        if (errorElement && this.validity.valid) {
            errorElement.remove();
        }
    };
    
    this.addEventListener('input', removeMessage);
    this.addEventListener('blur', removeMessage);
};

// Auto-inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    if (!window.mobileFormsInstance) {
        window.mobileFormsInstance = new MobileForms();
    }
});

// Exportar para uso global
window.MobileForms = MobileForms;
