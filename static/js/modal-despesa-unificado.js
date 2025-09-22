/**
 * Modal Unificado de Despesas
 * Gerencia a criação e edição de despesas em diferentes contextos
 */

class ModalDespesaUnificado {
    constructor() {
        this.modal = null;
        this.form = null;
        this.contexto = null; // 'eventos' ou 'novo_evento'
        this.eventoId = null;
        this.despesaId = null; // Para edição
        this.isEdicao = false;
        this.fornecedores = [];
        
        this.init();
    }
    
    init() {
        this.modal = document.getElementById('modalAdicionarDespesa');
        this.form = this.modal ? this.modal.querySelector('form') : null;
        
        if (!this.modal || !this.form) {
            console.error('Modal ou formulário não encontrado');
            return;
        }
        
        this.setupEventListeners();
        this.aplicarMascaras();
    }
    
    setupEventListeners() {
        // Submit do formulário
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Mudança de categoria
        document.getElementById('modal_despesa_categoria').addEventListener('change', (e) => {
            this.carregarDespesas(e.target.value);
        });
        
        // Mudança de despesa (para mostrar campos específicos)
        document.getElementById('modal_despesa_item').addEventListener('change', (e) => {
            this.verificarCamposEspecificos(e.target.value);
        });
        
        // Reset do modal ao fechar
        this.modal.addEventListener('hidden.bs.modal', () => {
            this.resetModal();
        });
    }
    
    aplicarMascaras() {
        // Máscara de moeda para os campos de valor
        const camposValor = ['modal_despesa_valor', 'modal_despesa_valor_pago_socrates'];
        
        camposValor.forEach(campoId => {
            const campo = document.getElementById(campoId);
            if (campo) {
                campo.addEventListener('input', function(e) {
                    let value = e.target.value;
                    
                    // Remove tudo que não é dígito
                    value = value.replace(/\D/g, '');
                    
                    if (value === '') {
                        e.target.value = '';
                        return;
                    }
                    
                    // Converte para centavos
                    value = (value / 100).toFixed(2);
                    
                    // Substitui ponto por vírgula
                    value = value.replace('.', ',');
                    
                    // Adiciona separador de milhares
                    value = value.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
                    
                    e.target.value = value;
                });
            }
        });
    }
    
    /**
     * Abre o modal para adicionar nova despesa
     * @param {string} contexto - 'eventos' ou 'novo_evento'
     * @param {number} eventoId - ID do evento
     * @param {Array} fornecedores - Lista de fornecedores
     */
    abrirParaAdicionar(contexto, eventoId = null, fornecedores = []) {
        this.contexto = contexto;
        this.eventoId = eventoId;
        this.fornecedores = fornecedores;
        this.isEdicao = false;
        this.despesaId = null;
        
        // Configurar título e botão
        document.getElementById('modal-title-text').textContent = 'Adicionar Despesa';
        document.getElementById('btn-text').textContent = 'Adicionar Despesa';
        
        // Configurar fornecedor baseado no contexto
        this.configurarFornecedor();
        
        // Mostrar modal
        const bsModal = new bootstrap.Modal(this.modal);
        bsModal.show();
    }
    
    /**
     * Abre o modal para editar despesa existente
     * @param {string} contexto - 'eventos' ou 'novo_evento'
     * @param {number} eventoId - ID do evento
     * @param {number} despesaId - ID da despesa
     * @param {Object} dados - Dados da despesa
     * @param {Array} fornecedores - Lista de fornecedores
     */
    abrirParaEditar(contexto, eventoId, despesaId, dados, fornecedores = []) {
        this.contexto = contexto;
        this.eventoId = eventoId;
        this.despesaId = despesaId;
        this.fornecedores = fornecedores;
        this.isEdicao = true;
        
        // Configurar título e botão
        document.getElementById('modal-title-text').textContent = 'Editar Despesa';
        document.getElementById('btn-text').textContent = 'Salvar Alterações';
        
        // Configurar fornecedor baseado no contexto
        this.configurarFornecedor();
        
        // Preencher dados
        this.preencherDados(dados);
        
        // Mostrar modal
        const bsModal = new bootstrap.Modal(this.modal);
        bsModal.show();
    }
    
    configurarFornecedor() {
        const container = document.getElementById('fornecedor_container_unificado');
        
        if (this.contexto === 'novo_evento') {
            // Usar busca de fornecedor com input + botão
            container.innerHTML = `
                <input type="text" class="form-control" id="fornecedor_nome_unificado" 
                       placeholder="Clique para buscar fornecedor..." readonly>
                <input type="hidden" name="id_fornecedor" id="fornecedor_id_unificado">
                <button type="button" class="btn btn-outline-secondary" onclick="modalDespesaUnificado.abrirBuscaFornecedor()">
                    <i class="bi bi-search"></i>
                </button>
                <button type="button" class="btn btn-outline-danger" onclick="modalDespesaUnificado.limparFornecedor()" title="Limpar seleção">
                    <i class="bi bi-x"></i>
                </button>
            `;
        } else {
            // Usar select simples
            let options = '<option value="">Selecione um fornecedor...</option>';
            this.fornecedores.forEach(fornecedor => {
                options += `<option value="${fornecedor.id_fornecedor}">${fornecedor.nome}</option>`;
            });
            
            container.innerHTML = `
                <select name="fornecedor_id" class="form-select" id="fornecedor_select_unificado">
                    ${options}
                </select>
            `;
        }
    }
    
    async carregarDespesas(categoriaId) {
        if (!categoriaId) {
            document.getElementById('modal_despesa_item').innerHTML = '<option value="">Primeiro selecione a categoria...</option>';
            return;
        }
        
        try {
            console.log('🔍 Carregando despesas para categoria:', categoriaId);
            const response = await fetch(`/api/despesas-por-categoria/${categoriaId}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const despesas = await response.json();
            console.log('📋 Despesas recebidas:', despesas);
            
            if (despesas.error) {
                throw new Error(despesas.error);
            }
            
            let options = '<option value="">Selecione uma despesa...</option>';
            
            if (despesas.length === 0) {
                options = '<option value="">Nenhuma despesa encontrada para esta categoria</option>';
            } else {
                despesas.forEach(despesa => {
                    const option = `<option value="${despesa.id_despesa}" ${despesa.valor_medio ? `data-valor-medio="${despesa.valor_medio.toFixed(2).replace('.', ',')}"` : ''}>${despesa.nome}</option>`;
                    options += option;
                });
            }
            
            document.getElementById('modal_despesa_item').innerHTML = options;
        } catch (error) {
            console.error('❌ Erro ao carregar despesas:', error);
            document.getElementById('modal_despesa_item').innerHTML = '<option value="">Erro ao carregar despesas</option>';
        }
    }
    
    verificarCamposEspecificos(despesaId) {
        // Verificar se é despesa de alimentação (lógica específica do sistema)
        const qtdDiasContainer = document.getElementById('qtd_dias_container');
        const qtdPessoasContainer = document.getElementById('qtd_pessoas_container');
        
        // Por enquanto, ocultar sempre. Pode ser implementado baseado na despesa selecionada
        qtdDiasContainer.style.display = 'none';
        qtdPessoasContainer.style.display = 'none';
    }
    
    preencherDados(dados) {
        // Preencher campos do formulário
        document.getElementById('modal_despesa_categoria').value = dados.categoria_id || '';
        document.getElementById('modal_despesa_data_vencimento').value = dados.data_vencimento || '';
        document.getElementById('modal_despesa_data_pagamento').value = dados.data_pagamento || '';
        document.getElementById('modal_despesa_valor').value = dados.valor ? dados.valor.replace('.', ',') : '';
        document.getElementById('modal_despesa_valor_pago_socrates').value = dados.valor_pago_socrates ? dados.valor_pago_socrates.replace('.', ',') : '';
        document.getElementById('modal_despesa_status').value = dados.status_pagamento || 'pendente';
        document.getElementById('modal_despesa_forma').value = dados.forma_pagamento || 'débito';
        document.getElementById('modal_despesa_pago_por').value = dados.pago_por || '';
        document.getElementById('modal_despesa_obs').value = dados.observacoes || '';
        document.getElementById('despesa_cabeca_novo_evento').checked = dados.despesa_cabeca || false;
        
        // Carregar despesas da categoria se necessário
        if (dados.categoria_id) {
            this.carregarDespesas(dados.categoria_id).then(() => {
                document.getElementById('modal_despesa_item').value = dados.despesa_id || '';
            });
        }
        
        // Preencher fornecedor baseado no contexto
        if (this.contexto === 'novo_evento') {
            document.getElementById('fornecedor_nome_unificado').value = dados.fornecedor_nome || '';
            document.getElementById('fornecedor_id_unificado').value = dados.fornecedor_id || '';
        } else {
            const fornecedorSelect = document.getElementById('fornecedor_select_unificado');
            if (fornecedorSelect) {
                fornecedorSelect.value = dados.fornecedor_id || '';
            }
        }
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        const submitBtn = this.form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        // Desabilitar botão e mostrar loading
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="bi bi-clock me-2"></i>Salvando...';
        
        try {
            const formData = new FormData(this.form);
            
            let url;
            if (this.contexto === 'novo_evento') {
                // Para novo evento, usar a função existente
                await this.salvarEventoSeNecessario();
                url = `/eventos/${this.eventoId}/salvar-despesa`;
            } else {
                // Para eventos existentes
                url = `/eventos/${this.eventoId}/despesas`;
                if (this.isEdicao && this.despesaId) {
                    url += `/${this.despesaId}`;
                    formData.append('_method', 'PUT');
                }
            }
            
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Fechar modal
                const bsModal = bootstrap.Modal.getInstance(this.modal);
                bsModal.hide();
                
                // Mostrar mensagem de sucesso
                this.mostrarMensagem('Despesa salva com sucesso!', 'success');
                
                // Recarregar dados na página
                if (typeof atualizarTabelaDespesas === 'function') {
                    atualizarTabelaDespesas();
                }
                
                if (typeof carregarDespesasEvento === 'function') {
                    carregarDespesasEvento();
                }
                
            } else {
                throw new Error(result.message || 'Erro ao salvar despesa');
            }
            
        } catch (error) {
            console.error('Erro:', error);
            this.mostrarMensagem(error.message || 'Erro ao salvar despesa', 'error');
        } finally {
            // Restaurar botão
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    }
    
    async salvarEventoSeNecessario() {
        // Implementar lógica para salvar evento se necessário (contexto novo_evento)
        if (this.contexto === 'novo_evento' && !this.eventoId) {
            // Lógica específica para salvar evento antes da despesa
            // Esta função deve ser implementada conforme a lógica existente
            return await window.salvarEventoSeNecessario();
        }
        return this.eventoId;
    }
    
    resetModal() {
        this.form.reset();
        this.contexto = null;
        this.eventoId = null;
        this.despesaId = null;
        this.isEdicao = false;
        this.fornecedores = [];
        
        // Resetar campos específicos
        document.getElementById('modal_despesa_item').innerHTML = '<option value="">Primeiro selecione a categoria...</option>';
        document.getElementById('qtd_dias_container').style.display = 'none';
        document.getElementById('qtd_pessoas_container').style.display = 'none';
    }
    
    mostrarMensagem(mensagem, tipo) {
        // Implementar sistema de notificação
        if (typeof mostrarToast === 'function') {
            mostrarToast(mensagem, tipo);
        } else {
            alert(mensagem);
        }
    }
    
    // Métodos para busca de fornecedor (contexto novo_evento)
    abrirBuscaFornecedor() {
        // Implementar abertura do modal de busca de fornecedor
        if (typeof abrirBuscaFornecedor === 'function') {
            abrirBuscaFornecedor();
        }
    }
    
    limparFornecedor() {
        document.getElementById('fornecedor_nome_unificado').value = '';
        document.getElementById('fornecedor_id_unificado').value = '';
    }
}

// Instanciar o modal globalmente
let modalDespesaUnificado;

document.addEventListener('DOMContentLoaded', function() {
    modalDespesaUnificado = new ModalDespesaUnificado();
});

// Funções globais para compatibilidade
function abrirModalDespesa(contexto, eventoId = null, fornecedores = []) {
    if (modalDespesaUnificado) {
        modalDespesaUnificado.abrirParaAdicionar(contexto, eventoId, fornecedores);
    }
}

function editarModalDespesa(contexto, eventoId, despesaId, dados, fornecedores = []) {
    if (modalDespesaUnificado) {
        modalDespesaUnificado.abrirParaEditar(contexto, eventoId, despesaId, dados, fornecedores);
    }
}
