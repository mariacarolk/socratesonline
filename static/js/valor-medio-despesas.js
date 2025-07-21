/**
 * Funcionalidade de Valor Médio para Despesas
 * 
 * Este script implementa:
 * 1. Busca do valor médio quando uma despesa é selecionada
 * 2. Sugestão do valor médio no campo de valor
 * 3. Validação se o valor digitado está 10% acima/abaixo do valor médio
 * 4. Exibição de alerta quando necessário
 */

// Variável global para armazenar o valor médio atual
let valorMedioAtual = null;
let alertaAtivo = null;

/**
 * Busca o valor médio de uma despesa
 * @param {number} despesaId - ID da despesa
 * @returns {Promise} - Promise com os dados do valor médio
 */
async function buscarValorMedio(despesaId) {
    try {
        const response = await fetch(`/api/despesa-valor-medio/${despesaId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao buscar valor médio:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Aplica o valor médio como sugestão no campo de valor
 * @param {Element} valorInput - Input do valor
 * @param {number} valorMedio - Valor médio formatado
 */
function aplicarSugestaoValorMedio(valorInput, valorMedioFormatado) {
    if (valorMedioFormatado && valorInput) {
        // Se o campo estiver vazio, preenche com o valor médio
        if (!valorInput.value || valorInput.value.trim() === '' || valorInput.value === '0,00') {
            valorInput.value = valorMedioFormatado;
            
            // Adicionar classe visual para indicar sugestão
            valorInput.classList.add('valor-sugerido');
            
            // Aplicar formatação se houver função disponível
            if (valorInput.hasAttribute('oninput')) {
                const onInputAttr = valorInput.getAttribute('oninput');
                if (onInputAttr.includes('formatarMoeda')) {
                    if (window.formatarMoeda && typeof window.formatarMoeda === 'function') {
                        window.formatarMoeda(valorInput);
                    }
                } else if (onInputAttr.includes('formatarMoedaBrasil')) {
                    if (window.formatarMoedaBrasil && typeof window.formatarMoedaBrasil === 'function') {
                        window.formatarMoedaBrasil(valorInput);
                    }
                }
            }
            
            // Mostrar tooltip ou indicação visual
            mostrarIndicacaoValorMedio(valorInput, valorMedioFormatado);
        }
    }
}

/**
 * Mostra indicação visual de que o valor foi sugerido
 * @param {Element} valorInput - Input do valor
 * @param {string} valorMedioFormatado - Valor médio formatado
 */
function mostrarIndicacaoValorMedio(valorInput, valorMedioFormatado) {
    // Remover indicação anterior se existir
    const indicacaoAnterior = valorInput.parentElement.querySelector('.valor-medio-indicacao');
    if (indicacaoAnterior) {
        indicacaoAnterior.remove();
    }
    
    // Criar nova indicação
    const indicacao = document.createElement('small');
    indicacao.className = 'text-info valor-medio-indicacao';
    indicacao.innerHTML = `<i class="bi bi-info-circle me-1"></i>Valor médio sugerido: R$ ${valorMedioFormatado}`;
    
    // Inserir após o input group
    const inputGroup = valorInput.closest('.input-group');
    if (inputGroup) {
        inputGroup.parentNode.insertBefore(indicacao, inputGroup.nextSibling);
    } else {
        valorInput.parentNode.insertBefore(indicacao, valorInput.nextSibling);
    }
}

/**
 * Remove a classe de valor sugerido quando o usuário começa a digitar
 * @param {Element} valorInput - Input do valor
 */
function removerIndicacaoValorSugerido(valorInput) {
    valorInput.classList.remove('valor-sugerido');
    
    const indicacao = valorInput.parentElement.querySelector('.valor-medio-indicacao');
    if (indicacao) {
        indicacao.remove();
    }
}

/**
 * Valida se o valor digitado está dentro da margem de 10% do valor médio
 * @param {number} valorDigitado - Valor digitado pelo usuário
 * @param {number} valorMedio - Valor médio da despesa
 * @returns {Object} - Resultado da validação
 */
function validarVariacaoValorMedio(valorDigitado, valorMedio) {
    if (!valorMedio || valorMedio <= 0) {
        return { isValid: true, percentual: 0, tipo: null };
    }
    
    const diferenca = valorDigitado - valorMedio;
    const percentual = Math.abs(diferenca / valorMedio * 100);
    
    if (percentual > 10) {
        const tipo = diferenca > 0 ? 'maior' : 'menor';
        return { 
            isValid: false, 
            percentual: percentual.toFixed(1), 
            tipo: tipo,
            valorMedio: valorMedio,
            valorDigitado: valorDigitado
        };
    }
    
    return { isValid: true, percentual: percentual.toFixed(1), tipo: null };
}

/**
 * Mostra alerta de variação no valor
 * @param {Object} validacao - Resultado da validação
 * @param {Element} valorInput - Input do valor
 */
function mostrarAlertaVariacao(validacao, valorInput) {
    // Remover alerta anterior
    removerAlertaVariacao(valorInput);
    
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-warning mt-2 valor-medio-alerta';
    alertDiv.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-exclamation-triangle me-2"></i>
            <div>
                <strong>Atenção:</strong> Valor ${validacao.percentual}% ${validacao.tipo} que o médio para esta despesa.
                <br>
                <small>Valor médio: R$ ${validacao.valorMedio.toFixed(2).replace('.', ',')} | 
                Valor digitado: R$ ${validacao.valorDigitado.toFixed(2).replace('.', ',')}</small>
            </div>
        </div>
    `;
    
    // Inserir alerta após o campo de valor
    const container = valorInput.closest('.col-md-6') || valorInput.closest('.col-12') || valorInput.parentElement;
    container.appendChild(alertDiv);
    
    alertaAtivo = alertDiv;
}

/**
 * Remove alerta de variação
 * @param {Element} valorInput - Input do valor
 */
function removerAlertaVariacao(valorInput) {
    const alertaExistente = valorInput.closest('.row').querySelector('.valor-medio-alerta');
    if (alertaExistente) {
        alertaExistente.remove();
    }
    alertaAtivo = null;
}

/**
 * Converte valor formatado brasileiro para número
 * @param {string} valorFormatado - Valor no formato brasileiro (ex: 1.000,50)
 * @returns {number} - Valor numérico
 */
function converterValorBrasileiroParaNumero(valorFormatado) {
    if (!valorFormatado) return 0;
    
    const valorLimpo = valorFormatado.toString().trim();
    
    // Se contém ponto e vírgula, é formato brasileiro (ex: 1.000,50)
    if (valorLimpo.includes('.') && valorLimpo.includes(',')) {
        return parseFloat(valorLimpo.replace(/\./g, '').replace(',', '.'));
    }
    // Se contém apenas vírgula, trocar por ponto
    else if (valorLimpo.includes(',') && !valorLimpo.includes('.')) {
        return parseFloat(valorLimpo.replace(',', '.'));
    }
    // Se já está em formato numérico
    else {
        return parseFloat(valorLimpo);
    }
}

/**
 * Configura os event listeners para um campo de valor de despesa
 * @param {Element} selectDespesa - Select da despesa
 * @param {Element} valorInput - Input do valor
 */
function configurarValidacaoValorMedio(selectDespesa, valorInput) {
    if (!selectDespesa || !valorInput) return;
    
    // REMOVER event listeners anteriores para evitar duplicação
    const oldChangeListener = selectDespesa._valorMedioChangeListener;
    const oldInputListener = valorInput._valorMedioInputListener;
    const oldBlurListener = valorInput._valorMedioBlurListener;
    
    if (oldChangeListener) {
        selectDespesa.removeEventListener('change', oldChangeListener);
    }
    if (oldInputListener) {
        valorInput.removeEventListener('input', oldInputListener);
    }
    if (oldBlurListener) {
        valorInput.removeEventListener('blur', oldBlurListener);
    }
    
    // Event listener para mudança na seleção da despesa
    const changeListener = async function() {
        const despesaId = this.value;
        
        // Limpar valor médio atual e alertas
        valorMedioAtual = null;
        removerAlertaVariacao(valorInput);
        removerIndicacaoValorSugerido(valorInput);
        
        if (despesaId && despesaId !== '' && despesaId !== '0') {
            try {
                const resultado = await buscarValorMedio(despesaId);
                
                if (resultado.success && resultado.has_valor_medio) {
                    valorMedioAtual = resultado.valor_medio;
                    aplicarSugestaoValorMedio(valorInput, resultado.valor_medio_formatado);
                }
            } catch (error) {
                console.error('Erro ao buscar valor médio:', error);
            }
        }
    };
    
        // Event listener para quando usuário digita (apenas remove indicação sugerida)
    const inputListener = function() {
        // Remover indicação de valor sugerido quando usuário digita
        removerIndicacaoValorSugerido(this);
        // Remover alerta anterior enquanto está digitando
        removerAlertaVariacao(this);
    };

    // Event listener para quando o campo perde o foco (validação completa)
    const blurListener = function() {
        if (valorMedioAtual && valorMedioAtual > 0) {
            const valorDigitado = converterValorBrasileiroParaNumero(this.value);
            
            if (valorDigitado > 0) {
                const validacao = validarVariacaoValorMedio(valorDigitado, valorMedioAtual);
                
                if (!validacao.isValid) {
                    mostrarAlertaVariacao(validacao, this);
                } else {
                    removerAlertaVariacao(this);
                }
            } else {
                removerAlertaVariacao(this);
            }
        }
    };
    
    // Adicionar os event listeners e armazenar suas referências
    selectDespesa.addEventListener('change', changeListener);
    valorInput.addEventListener('input', inputListener);
    valorInput.addEventListener('blur', blurListener);
    
    // Armazenar referências para remoção futura
    selectDespesa._valorMedioChangeListener = changeListener;
    valorInput._valorMedioInputListener = inputListener;
    valorInput._valorMedioBlurListener = blurListener;
}

/**
 * Limpa todos os alertas e indicações de valor médio
 */
function limparAlertasValorMedio() {
    // Remover todos os alertas ativos
    document.querySelectorAll('.valor-medio-alerta').forEach(alerta => alerta.remove());
    document.querySelectorAll('.valor-medio-indicacao').forEach(indicacao => indicacao.remove());
    
    // Remover classes de valor sugerido
    document.querySelectorAll('.valor-sugerido').forEach(input => {
        input.classList.remove('valor-sugerido');
    });
    
    // Resetar variável global
    valorMedioAtual = null;
    alertaAtivo = null;
}

/**
 * Inicializa a funcionalidade de valor médio para formulários de despesa
 * Deve ser chamada quando o DOM estiver carregado
 */
function inicializarValidacaoValorMedio() {
    // Para formulários de despesas de evento (página de eventos)
    document.querySelectorAll('form[onsubmit*="adicionarDespesaCompleta"]').forEach(form => {
        const selectDespesa = form.querySelector('select[name="despesa_id"]');
        const valorInput = form.querySelector('input[name="valor"]');
        
        if (selectDespesa && valorInput && !selectDespesa.hasAttribute('data-valor-medio-configurado')) {
            configurarValidacaoValorMedio(selectDespesa, valorInput);
            selectDespesa.setAttribute('data-valor-medio-configurado', 'true');
        }
    });
    
    // Para formulários de despesas da empresa
    const formDespesaEmpresa = document.querySelector('form[action*="despesas"]');
    if (formDespesaEmpresa) {
        const selectDespesa = formDespesaEmpresa.querySelector('select[name="despesa_id"], select[id="despesa_id"]');
        const valorInput = formDespesaEmpresa.querySelector('input[name="valor"], input[id="valor_input"]');
        
        if (selectDespesa && valorInput && !selectDespesa.hasAttribute('data-valor-medio-configurado')) {
            configurarValidacaoValorMedio(selectDespesa, valorInput);
            selectDespesa.setAttribute('data-valor-medio-configurado', 'true');
        }
    }
    
    // Para modal no novo_evento.html
    const modalNovoDespesa = document.querySelector('#modalAdicionarDespesa');
    if (modalNovoDespesa) {
        const selectDespesa = modalNovoDespesa.querySelector('select[name="despesa_id"], select[id*="despesa_item"]');
        const valorInput = modalNovoDespesa.querySelector('input[name="valor"], input[id*="despesa_valor"]');
        
        if (selectDespesa && valorInput && !selectDespesa.hasAttribute('data-valor-medio-configurado')) {
            configurarValidacaoValorMedio(selectDespesa, valorInput);
            selectDespesa.setAttribute('data-valor-medio-configurado', 'true');
        }
    }
    
    // Busca genérica para qualquer formulário não coberto acima
    document.querySelectorAll('form').forEach(form => {
        const selectDespesa = form.querySelector('select[name="despesa_id"], select[id$="despesa_id"], select[id*="despesa"]');
        const valorInput = form.querySelector('input[name="valor"], input[id*="valor"]');
        
        if (selectDespesa && valorInput && !selectDespesa.hasAttribute('data-valor-medio-configurado')) {
            // Verificar se é realmente um campo de despesa (evitar conflitos)
            const despesaOptions = selectDespesa.querySelectorAll('option[value]:not([value=""])');
            if (despesaOptions.length > 0) {
                configurarValidacaoValorMedio(selectDespesa, valorInput);
                selectDespesa.setAttribute('data-valor-medio-configurado', 'true');
            }
        }
    });
    
    // Configurar limpeza quando modais são abertos
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('show.bs.modal', limparAlertasValorMedio);
    });
}

// Auto-inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    inicializarValidacaoValorMedio();
    
    // Também limpar alertas quando a página é carregada
    limparAlertasValorMedio();
});

// Também inicializar quando HTMX ou outros frameworks carregarem conteúdo dinamicamente
document.addEventListener('htmx:afterSwap', inicializarValidacaoValorMedio);

/**
 * Valida variação de valor médio em um input específico
 * @param {Element} valorInput - Input do valor
 * @param {number} valorMedio - Valor médio da despesa
 */
function validarVariacaoValorMedioInput(valorInput, valorMedio) {
    if (!valorInput || !valorMedio) {
        return;
    }
    
    // Obter valor digitado do input (convertendo formato brasileiro)
    let valorDigitadoStr = valorInput.value.trim();
    if (!valorDigitadoStr) {
        return;
    }
    
    // Converter valor do formato brasileiro para número
    let valorDigitado;
    try {
        // Se contém ponto e vírgula, é formato brasileiro (ex: 1.000,50)
        if (valorDigitadoStr.includes('.') && valorDigitadoStr.includes(',')) {
            valorDigitadoStr = valorDigitadoStr.replace(/\./g, '').replace(',', '.');
        }
        // Se contém apenas vírgula, trocar por ponto
        else if (valorDigitadoStr.includes(',') && !valorDigitadoStr.includes('.')) {
            valorDigitadoStr = valorDigitadoStr.replace(',', '.');
        }
        
        valorDigitado = parseFloat(valorDigitadoStr);
        
        if (isNaN(valorDigitado) || valorDigitado <= 0) {
            return;
        }
    } catch (error) {
        console.log('Erro ao converter valor digitado:', error);
        return;
    }
    
    // Executar validação
    const validacao = validarVariacaoValorMedio(valorDigitado, valorMedio);
    
    // Remover alertas anteriores
    removerAlertaVariacao(valorInput);
    
    // Mostrar alerta se necessário
    if (!validacao.isValid) {
        mostrarAlertaVariacao(validacao, valorInput);
    }
}

/**
 * Configura validação para disparar ao sair do campo de valor
 * @param {Element} valorInput - Input do valor
 * @param {number} valorMedio - Valor médio da despesa
 * @returns {Element} - O novo input com listener configurado
 */
function configurarValidacaoTempoReal(valorInput, valorMedio) {
    if (!valorInput || !valorMedio) {
        return valorInput;
    }
    
    // Armazenar valor médio no dataset do input
    valorInput.dataset.valorMedio = valorMedio;
    
    // Aplicar validação inicial
    validarVariacaoValorMedioInput(valorInput, valorMedio);
    
    // Remover listeners anteriores clonando o elemento
    const novoInput = valorInput.cloneNode(true);
    valorInput.parentNode.replaceChild(novoInput, valorInput);
    
    // Adicionar listener para validação quando sair do campo
    novoInput.addEventListener('blur', function() {
        const valorMedioAtual = parseFloat(this.dataset.valorMedio);
        if (valorMedioAtual) {
            validarVariacaoValorMedioInput(this, valorMedioAtual);
        }
    });
    
    console.log('✅ Validação configurada para disparar ao sair do campo');
    return novoInput;
}

// Exportar funções para uso global
window.ValorMedioDespesas = {
    inicializar: inicializarValidacaoValorMedio,
    configurar: configurarValidacaoValorMedio,
    buscarValorMedio: buscarValorMedio,
    validarVariacao: validarVariacaoValorMedio,
    validarVariacaoInput: validarVariacaoValorMedioInput,
    configurarValidacao: configurarValidacaoTempoReal,
    limparAlertas: limparAlertasValorMedio
}; 