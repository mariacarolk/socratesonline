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
        
        // Reset do modal ao fechar
        this.modal.addEventListener('hidden.bs.modal', () => {
            this.resetModal();
        });
        
        // Event listeners para categoria e despesa serão configurados no abrirParaAdicionar
        // para evitar conflitos com outros scripts
    }
    
    configurarEventListeners() {
        console.log('🔧 === CONFIGURANDO EVENT LISTENERS ===');
        console.log('Contexto atual:', this.contexto);
        console.log('Evento ID atual:', this.eventoId);
        
        // Mudança de categoria
        const selectCategoria = document.getElementById('modal_despesa_categoria');
        console.log('Select categoria encontrado para configurar:', !!selectCategoria);
        
        if (selectCategoria) {
            console.log('Select categoria antes da configuração:');
            console.log('- Value:', selectCategoria.value);
            console.log('- Has onchange attr:', selectCategoria.hasAttribute('onchange'));
            console.log('- Onchange attr value:', selectCategoria.getAttribute('onchange'));
            
            // Remover todos os event listeners existentes clonando o elemento
            const novoSelectCategoria = selectCategoria.cloneNode(true);
            selectCategoria.parentNode.replaceChild(novoSelectCategoria, selectCategoria);
            console.log('🔄 Select categoria clonado para limpar event listeners');
            
            // Remover atributo onchange se existir (para evitar conflitos)
            novoSelectCategoria.removeAttribute('onchange');
            console.log('🧹 Atributo onchange removido');
            
            // Adicionar nosso event listener
            const eventHandler = (e) => {
                console.log('🔄 === EVENTO CHANGE CATEGORIA DISPARADO ===');
                console.log('Valor selecionado:', e.target.value);
                console.log('Tipo do valor:', typeof e.target.value);
                console.log('Target element:', e.target);
                console.log('Event object:', e);
                console.log('Contexto do modal:', this.contexto);
                console.log('ID do evento:', this.eventoId);
                
                if (e.target.value) {
                    console.log('✅ Valor válido encontrado, carregando despesas...');
                    this.carregarDespesas(e.target.value);
                } else {
                    console.log('⚠️ Valor vazio, não carregando despesas');
                }
            };
            
            novoSelectCategoria.addEventListener('change', eventHandler);
            
            // Marcar como configurado
            novoSelectCategoria.setAttribute('data-listeners-configured', 'true');
            
            console.log('✅ Event listener adicionado ao select categoria');
            console.log('Event handler function:', eventHandler);
            
            // Testar se o event listener foi adicionado corretamente
            setTimeout(() => {
                console.log('🧪 Testando se event listener foi configurado...');
                const testeEvent = new Event('change', { bubbles: true });
                novoSelectCategoria.dispatchEvent(testeEvent);
            }, 100);
            
        } else {
            console.error('❌ Select categoria não encontrado para configuração');
        }
        
        // Mudança de despesa (para mostrar campos específicos)
        const selectDespesa = document.getElementById('modal_despesa_item');
        console.log('Select despesa encontrado:', !!selectDespesa);
        
        if (selectDespesa) {
            selectDespesa.addEventListener('change', (e) => {
                console.log('🔄 Evento change disparado na despesa:', e.target.value);
                this.verificarCamposEspecificos(e.target.value);
            });
            console.log('✅ Event listener configurado para select despesa');
        } else {
            console.error('❌ Select despesa não encontrado');
        }
        
        console.log('🔧 === CONFIGURAÇÃO EVENT LISTENERS CONCLUÍDA ===');
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
        console.log('📂 Abrindo modal para adicionar - Contexto:', contexto, 'Evento ID:', eventoId);
        
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
        
        // Configurar event listeners ANTES de mostrar o modal
        console.log('📂 Configurando event listeners ANTES de mostrar modal...');
        setTimeout(() => {
            this.configurarEventListeners();
        }, 50);
        
        // Também tentar configurar DEPOIS de mostrar
        this.modal.addEventListener('shown.bs.modal', () => {
            console.log('📂 Modal shown.bs.modal event disparado');
            setTimeout(() => {
                console.log('📂 Configurando event listeners APÓS modal visível (backup)...');
                // Verificar se já foi configurado
                const selectCategoria = document.getElementById('modal_despesa_categoria');
                if (selectCategoria && !selectCategoria.hasAttribute('data-listeners-configured')) {
                    console.log('📂 Event listeners não configurados ainda, configurando agora...');
                    this.configurarEventListeners();
                }
                
                // ✅ VERIFICAÇÃO AUTOMÁTICA SE DESPESA JÁ ESTÁ SELECIONADA
                const selectDespesa = document.getElementById('modal_despesa_item');
                if (selectDespesa && selectDespesa.value) {
                    console.log('🔍 Modal unificado: despesa pré-selecionada detectada:', selectDespesa.value);
                    console.log('🔄 Executando verificação automática de campos específicos...');
                    this.verificarCamposEspecificos(selectDespesa.value);
                }
            }, 100);
        }, { once: true });
        
        console.log('📂 Mostrando modal...');
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
        console.log('🔍 === CARREGAR DESPESAS INICIADO ===');
        console.log('Categoria ID recebida:', categoriaId);
        console.log('Tipo da categoria ID:', typeof categoriaId);
        
        const selectDespesa = document.getElementById('modal_despesa_item');
        console.log('Select despesa encontrado:', !!selectDespesa);
        
        if (!selectDespesa) {
            console.error('❌ Select despesa não encontrado!');
            return;
        }
        
        if (!categoriaId) {
            console.log('⚠️ Categoria ID vazia, resetando select');
            selectDespesa.innerHTML = '<option value="">Primeiro selecione a categoria...</option>';
            return;
        }
        
        // Mostrar estado de carregamento
        selectDespesa.innerHTML = '<option value="">Carregando despesas...</option>';
        console.log('📝 Estado de carregamento definido');
        
        try {
            console.log('🔍 Iniciando fetch para categoria:', categoriaId);
            const url = `/api/despesas-por-categoria/${categoriaId}`;
            console.log('📡 URL da requisição:', url);
            
            const response = await fetch(url);
            console.log('📡 Resposta recebida - Status:', response.status);
            console.log('📡 Resposta OK:', response.ok);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const despesas = await response.json();
            console.log('📋 Dados JSON recebidos:', despesas);
            console.log('📋 Tipo dos dados:', typeof despesas);
            console.log('📋 É array:', Array.isArray(despesas));
            
            if (despesas.error) {
                console.error('❌ Erro retornado pela API:', despesas.error);
                throw new Error(despesas.error);
            }
            
            let options = '<option value="">Selecione uma despesa...</option>';
            
            if (!Array.isArray(despesas) || despesas.length === 0) {
                console.log('⚠️ Nenhuma despesa encontrada');
                options = '<option value="">Nenhuma despesa encontrada para esta categoria</option>';
            } else {
                console.log('✅ Processando', despesas.length, 'despesas');
                despesas.forEach((despesa, index) => {
                    console.log(`  ${index + 1}. ${despesa.nome} (ID: ${despesa.id_despesa})`);
                    const valorMedio = despesa.valor_medio ? `data-valor-medio="${despesa.valor_medio.toFixed(2).replace('.', ',')}"` : '';
                    const option = `<option value="${despesa.id_despesa}" ${valorMedio}>${despesa.nome}</option>`;
                    options += option;
                });
            }
            
            selectDespesa.innerHTML = options;
            console.log('✅ Options atualizadas no select');
            console.log('✅ Carregamento de despesas concluído');
            
        } catch (error) {
            console.error('❌ Erro ao carregar despesas:', error);
            console.error('❌ Stack trace:', error.stack);
            selectDespesa.innerHTML = '<option value="">Erro ao carregar despesas</option>';
            
            // Mostrar alerta para o usuário
            if (typeof mostrarNotificacao === 'function') {
                mostrarNotificacao(`Erro ao carregar despesas: ${error.message}`, 'danger');
            }
        }
    }
    
    verificarCamposEspecificos(despesaId) {
        console.log('🍽️ Verificando campos específicos para despesa ID:', despesaId);
        
        const qtdDiasContainer = document.getElementById('qtd_dias_container');
        const qtdPessoasContainer = document.getElementById('qtd_pessoas_container');
        const qtdDiasInput = document.getElementById('modal_qtd_dias');
        const qtdPessoasInput = document.getElementById('modal_qtd_pessoas');
        
        if (!despesaId) {
            console.log('⚠️ Nenhuma despesa selecionada, ocultando campos');
            qtdDiasContainer.style.display = 'none';
            qtdPessoasContainer.style.display = 'none';
            if (qtdDiasInput) qtdDiasInput.removeAttribute('required');
            if (qtdPessoasInput) qtdPessoasInput.removeAttribute('required');
            return;
        }
        
        // Buscar detalhes da despesa para verificar se é de alimentação
        fetch(`/api/despesa-detalhes/${despesaId}`)
            .then(response => response.json())
            .then(data => {
                console.log('📊 Dados da despesa recebidos:', data);
                
                if (data.flag_alimentacao) {
                    console.log('✅ É despesa de alimentação - mostrando campos');
                    qtdDiasContainer.style.display = 'block';
                    qtdPessoasContainer.style.display = 'block';
                    if (qtdDiasInput) qtdDiasInput.setAttribute('required', 'required');
                    if (qtdPessoasInput) qtdPessoasInput.setAttribute('required', 'required');
                } else {
                    console.log('❌ Não é despesa de alimentação - ocultando campos');
                    qtdDiasContainer.style.display = 'none';
                    qtdPessoasContainer.style.display = 'none';
                    if (qtdDiasInput) {
                        qtdDiasInput.removeAttribute('required');
                        qtdDiasInput.value = '';
                    }
                    if (qtdPessoasInput) {
                        qtdPessoasInput.removeAttribute('required');
                        qtdPessoasInput.value = '';
                    }
                }
            })
            .catch(error => {
                console.error('❌ Erro ao verificar despesa:', error);
                // Em caso de erro, ocultar campos
                qtdDiasContainer.style.display = 'none';
                qtdPessoasContainer.style.display = 'none';
                if (qtdDiasInput) qtdDiasInput.removeAttribute('required');
                if (qtdPessoasInput) qtdPessoasInput.removeAttribute('required');
            });
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
                // Verificar campos específicos após selecionar a despesa
                if (dados.despesa_id) {
                    console.log('🔍 Verificação inicial de alimentação na edição (modal unificado)');
                    this.verificarCamposEspecificos(dados.despesa_id);
                }
            });
        }
        
        // Se não há categoria mas há despesa_id, verificar diretamente
        else if (dados.despesa_id) {
            console.log('🔍 Verificação direta de alimentação na edição (modal unificado)');
            this.verificarCamposEspecificos(dados.despesa_id);
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
        
        // Evitar submissão duplicada quando existe um handler legacy inline (telas de novo/editar evento)
        if (this.form && (this.form.hasAttribute('onsubmit') || this.form.getAttribute('data-editing') === 'true')) {
            // Deixar o handler legacy (adicionarDespesaEvento/editarDespesaEvento) cuidar do fluxo
            return;
        }
        
        const submitBtn = this.form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        // Desabilitar botão e mostrar loading
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="bi bi-clock me-2"></i>Salvando...';
        
        try {
            const formData = new FormData(this.form);
            
            let url;
            let metodo = 'POST';
            if (this.contexto === 'novo_evento') {
                // Para novo evento, garantir que temos o ID (pode ser criado agora)
                const ensuredId = await this.salvarEventoSeNecessario();
                this.eventoId = ensuredId;
                url = `/eventos/${this.eventoId}/salvar-despesa`;
            } else {
                // Para eventos existentes
                if (this.isEdicao && this.despesaId) {
                    // Endpoint específico de edição
                    url = `/eventos/${this.eventoId}/editar-despesa/${this.despesaId}`;
                    metodo = 'PUT';
                } else {
                    // Criação de nova despesa
                    url = `/eventos/${this.eventoId}/salvar-despesa`;
                }
            }
            
            const response = await fetch(url, {
                method: metodo,
                body: formData
            });
            
            // Garantir que a resposta seja JSON para evitar erros de parse de HTML
            const contentType = response.headers.get('content-type') || '';
            if (!contentType.includes('application/json')) {
                const texto = await response.text();
                throw new Error('Resposta do servidor não é JSON: ' + texto.substring(0, 120));
            }
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
                
                // Fallback: se não houver funções de atualização na página de edição/novo, recarregar a página
                const hasRefreshHooks = (typeof atualizarTabelaDespesas === 'function') || (typeof carregarDespesasEvento === 'function');
                const isEditarOuNovo = window.location && (window.location.pathname.includes('/eventos/editar') || window.location.pathname.includes('/eventos/novo'));
                if (!hasRefreshHooks && isEditarOuNovo) {
                    window.location.reload();
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
