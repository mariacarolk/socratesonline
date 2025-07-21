/**
 * Modal unificado para adicionar despesas
 * Usado nas telas de eventos e novo evento
 */

// Função para abrir modal de despesa de forma unificada
function abrirModalDespesaUnificado(eventoId, categoriaId = '', nomeDespesa = '', nomeCategoria = '', isFixa = '', valorMedio = '') {
    // Determinar se estamos na tela de eventos ou novo evento
    const isNovoEvento = window.location.pathname.includes('/eventos/novo') || window.location.pathname.includes('/eventos/editar');
    
    // Limpar formulário
    const form = document.querySelector('#modalAdicionarDespesa form');
    form.reset();
    
    // Pré-preencher categoria se fornecida
    if (categoriaId) {
        const selectCategoria = form.querySelector('[name="categoria_despesa"]');
        if (selectCategoria) {
            selectCategoria.value = categoriaId;
            
            // Carregar despesas da categoria dependendo da tela
            if (isNovoEvento) {
                // Na tela novo evento, usar a função específica
                if (typeof carregarDespesasPorCategoriaModal === 'function') {
                    carregarDespesasPorCategoriaModal(categoriaId, nomeDespesa);
                }
            } else {
                // Na tela de eventos, usar a função específica
                if (typeof carregarDespesasPorCategoria === 'function') {
                    carregarDespesasPorCategoria(selectCategoria, eventoId);
                }
            }
        }
        
        // Se há uma despesa específica, pré-selecionar
        if (nomeDespesa) {
            setTimeout(() => {
                const selectDespesa = form.querySelector('[name="despesa_id"]');
                if (selectDespesa) {
                    // Procurar pela opção com o nome da despesa
                    for (let option of selectDespesa.options) {
                        if (option.text.includes(nomeDespesa)) {
                            selectDespesa.value = option.value;
                            break;
                        }
                    }
                }
            }, 500);
        }
    }
    
    // Pré-preencher data atual
    const inputData = form.querySelector('[name="data_vencimento"]');
    if (inputData) {
        const hoje = new Date().toISOString().split('T')[0];
        inputData.value = hoje;
    }
    
    // Pré-preencher valor médio se disponível
    if (valorMedio) {
        const inputValor = form.querySelector('[name="valor"]');
        if (inputValor) {
            inputValor.value = valorMedio.replace('.', ',');
            inputValor.setAttribute('data-valor-medio', valorMedio);
            
            // Aplicar validação de valor médio se existir
            if (typeof validarValorAoDigitarModal === 'function') {
                inputValor.removeEventListener('input', validarValorAoDigitarModal);
                inputValor.addEventListener('input', validarValorAoDigitarModal);
            }
        }
    }
    
    // Atualizar título do modal
    const titulo = document.querySelector('#modalAdicionarDespesa .modal-title');
    if (titulo) {
        if (nomeDespesa) {
            titulo.innerHTML = '<i class="bi bi-credit-card me-2"></i>Cadastrar: ' + nomeDespesa + ' (' + (isFixa === 'true' ? 'Fixa' : 'Variável') + ')';
        } else if (nomeCategoria) {
            titulo.innerHTML = '<i class="bi bi-credit-card me-2"></i>Nova Despesa - ' + nomeCategoria;
        } else {
            titulo.innerHTML = '<i class="bi bi-credit-card me-2"></i>Adicionar Despesa';
        }
    }
    
    // Ajustar form action e onsubmit baseado na tela
    if (isNovoEvento) {
        form.setAttribute('onsubmit', 'adicionarDespesaEvento(event)');
    } else if (eventoId) {
        form.setAttribute('onsubmit', `adicionarDespesaCompleta(event, '${eventoId}')`);
        
        // Configurar onChange para categoria na tela de eventos
        const selectCategoria = form.querySelector('[name="categoria_despesa"]');
        if (selectCategoria) {
            selectCategoria.setAttribute('onchange', `carregarDespesasPorCategoria(this, '${eventoId}')`);
        }
    }
    
    // Abrir modal
    const modal = new bootstrap.Modal(document.getElementById('modalAdicionarDespesa'));
    modal.show();
}

// Função para converter moeda para número (reutilizável)
function converterMoedaParaNumero(valor) {
    if (typeof valor === 'string') {
        return parseFloat(valor.replace(/[^\d,]/g, '').replace(',', '.')) || 0;
    }
    return parseFloat(valor) || 0;
}

// Função para formatar valor como moeda (reutilizável)
function formatarMoeda(valor) {
    return parseFloat(valor).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    });
}

// Função para mostrar notificação (reutilizável)
function mostrarNotificacao(mensagem, tipo = 'info') {
    // Remover notificações existentes
    const existingNotifications = document.querySelectorAll('.notification-toast');
    existingNotifications.forEach(n => n.remove());
    
    // Criar nova notificação
    const notification = document.createElement('div');
    notification.className = `alert alert-${tipo} notification-toast position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <span>${mensagem}</span>
            <button type="button" class="btn-close btn-close-white" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remover após 5 segundos
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Função para aplicar máscara de moeda em campos de valor
function aplicarMascaraMoeda(selector) {
    document.querySelectorAll(selector).forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = (value / 100).toFixed(2);
            value = value.replace('.', ',');
            value = value.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
            e.target.value = value;
        });
    });
}

// Inicializar máscaras quando o documento carregar
document.addEventListener('DOMContentLoaded', function() {
    aplicarMascaraMoeda('input[name="valor"]');
}); 