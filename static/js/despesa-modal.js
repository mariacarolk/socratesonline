/**
 * Modal unificado para adicionar despesas
 * Usado nas telas de eventos e novo evento
 */

// Função para abrir modal de despesa de forma unificada
function abrirModalDespesaUnificado(eventoIdOuDespesaId, categoriaId = '', nomeDespesa = '', nomeCategoria = '', isFixa = '', valorMedio = '') {
    // Determinar se estamos na tela de eventos ou novo evento
    const isNovoEvento = window.location.pathname.includes('/eventos/novo') || window.location.pathname.includes('/eventos/editar');

    // Na tela de novo/editar evento, o primeiro parâmetro historicamente é DESPESA_ID.
    // Na tela de listagem de eventos, o primeiro parâmetro é EVENTO_ID.
    const eventoIdPagina = (isNovoEvento && typeof obterEventoId === 'function') ? obterEventoId() : null;
    const eventoId = isNovoEvento ? (eventoIdPagina ? parseInt(eventoIdPagina) : null) : (eventoIdOuDespesaId ? parseInt(eventoIdOuDespesaId) : null);
    const despesaIdPreSelecionada = isNovoEvento ? (eventoIdOuDespesaId ? parseInt(eventoIdOuDespesaId) : null) : null;
    
    // Limpar formulário
    const form = document.querySelector('#modalAdicionarDespesa form');
    form.reset();

    // Informar contexto/IDs para a classe unificada
    if (typeof modalDespesaUnificado !== 'undefined' && modalDespesaUnificado) {
        modalDespesaUnificado.contexto = isNovoEvento ? 'novo_evento' : 'eventos';
        modalDespesaUnificado.eventoId = eventoId;
        modalDespesaUnificado.isEdicao = false;
        modalDespesaUnificado.despesaId = null;
    }
    
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
        
        // Se há uma despesa específica, pré-selecionar por nome ou ID
        if (nomeDespesa || despesaIdPreSelecionada) {
            setTimeout(() => {
                const selectDespesa = form.querySelector('[name="despesa_id"]');
                if (selectDespesa) {
                    if (despesaIdPreSelecionada) {
                        selectDespesa.value = String(despesaIdPreSelecionada);
                    } else if (nomeDespesa) {
                        for (let option of selectDespesa.options) {
                            if (option.text.includes(nomeDespesa)) {
                                selectDespesa.value = option.value;
                                break;
                            }
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
    
    // Aplicar máscara de moeda no campo valor pago Sócrates Online
    const inputValorPagoSocrates = form.querySelector('[name="valor_pago_socrates"]');
    if (inputValorPagoSocrates) {
        inputValorPagoSocrates.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value === '') {
                e.target.value = '';
                return;
            }
            value = (value / 100).toFixed(2);
            value = value.replace('.', ',');
            value = value.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
            e.target.value = value;
        });
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
    
    // Não usar onsubmit inline; deixar o controlador unificado tratar o submit
    form.removeAttribute('onsubmit');
    
    // Configurar onChange para categoria na tela de eventos (sempre que houver eventoId)
    if (eventoId && !isNovoEvento) {
        const selectCategoria = form.querySelector('[name="categoria_despesa"]');
        if (selectCategoria) {
            // Remover evento anterior se existir
            selectCategoria.removeAttribute('onchange');
            
            // NÃO configurar onchange HTML - deixar o modal-despesa-unificado.js lidar com isso
            // O modalDespesaUnificado já tem addEventListener para 'change' configurado
            
            console.log('🔧 Evento onChange NÃO configurado - deixando modalDespesaUnificado lidar com isso');
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
    aplicarMascaraMoeda('input[name="valor_pago_socrates"]');
}); 