/**
 * Sistema de Modal para Listar Eventos
 * Utilizado em páginas de Colaboradores, Fornecedores e Elenco
 */

class EventosModal {
    constructor() {
        this.modal = null;
        this.inicializarModal();
    }

    inicializarModal() {
        // Criar modal HTML
        const modalHTML = `
            <div class="modal fade" id="eventosModal" tabindex="-1" aria-labelledby="eventosModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="eventosModalLabel">Eventos</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div id="eventosModalLoading" class="text-center">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Carregando...</span>
                                </div>
                                <p class="mt-2">Carregando eventos...</p>
                            </div>
                            <div id="eventosModalContent" class="d-none">
                                <div class="alert alert-info" id="eventosModalInfo">
                                    <strong id="entidadeNome"></strong> participou de <strong id="totalEventos">0</strong> evento(s)
                                </div>
                                <div class="table-responsive">
                                    <table class="table table-striped">
                                        <thead>
                                            <tr>
                                                <th>Evento</th>
                                                <th>Circo</th>
                                                <th>Data Início</th>
                                                <th>Data Fim</th>
                                                <th>Local</th>
                                                <th id="extraColumn" class="d-none">Extra</th>
                                            </tr>
                                        </thead>
                                        <tbody id="eventosTableBody">
                                        </tbody>
                                    </table>
                                </div>
                                <div id="eventosModalEmpty" class="text-center text-muted d-none">
                                    <p>Nenhum evento encontrado para esta pessoa.</p>
                                </div>
                            </div>
                            <div id="eventosModalError" class="d-none">
                                <div class="alert alert-danger">
                                    <strong>Erro:</strong> <span id="errorMessage"></span>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Adicionar modal ao body se não existir
        if (!document.getElementById('eventosModal')) {
            document.body.insertAdjacentHTML('beforeend', modalHTML);
        }

        // Inicializar bootstrap modal
        const modalElement = document.getElementById('eventosModal');
        this.modal = new bootstrap.Modal(modalElement);
    }

    async mostrarEventosColaborador(colaboradorId, colaboradorNome) {
        this.configurarModal(colaboradorNome, 'Função');
        this.modal.show();
        
        try {
            const response = await fetch(`/api/colaborador/${colaboradorId}/eventos`);
            const data = await response.json();
            
            if (data.success) {
                this.renderizarEventos(data.eventos, data.total, data.colaborador, 'colaborador');
            } else {
                this.mostrarErro(data.message || 'Erro ao carregar eventos');
            }
        } catch (error) {
            this.mostrarErro('Erro de conexão: ' + error.message);
        }
    }

    async mostrarEventosFornecedor(fornecedorId, fornecedorNome) {
        this.configurarModal(fornecedorNome, 'Valor Total');
        this.modal.show();
        
        try {
            const response = await fetch(`/api/fornecedor/${fornecedorId}/eventos`);
            const data = await response.json();
            
            if (data.success) {
                this.renderizarEventos(data.eventos, data.total, data.fornecedor, 'fornecedor');
            } else {
                this.mostrarErro(data.message || 'Erro ao carregar eventos');
            }
        } catch (error) {
            this.mostrarErro('Erro de conexão: ' + error.message);
        }
    }

    async mostrarEventosElenco(elencoId, elencoNome) {
        this.configurarModal(elencoNome, 'Observações');
        this.modal.show();
        
        try {
            const response = await fetch(`/api/elenco/${elencoId}/eventos`);
            const data = await response.json();
            
            if (data.success) {
                this.renderizarEventos(data.eventos, data.total, data.membro_elenco, 'elenco');
            } else {
                this.mostrarErro(data.message || 'Erro ao carregar eventos');
            }
        } catch (error) {
            this.mostrarErro('Erro de conexão: ' + error.message);
        }
    }

    configurarModal(nome, extraColumnTitle) {
        // Resetar modal
        this.resetarModal();
        
        // Configurar título
        document.getElementById('eventosModalLabel').textContent = `Eventos - ${nome}`;
        
        // Configurar coluna extra
        const extraColumn = document.getElementById('extraColumn');
        if (extraColumnTitle) {
            extraColumn.textContent = extraColumnTitle;
            extraColumn.classList.remove('d-none');
        } else {
            extraColumn.classList.add('d-none');
        }
    }

    renderizarEventos(eventos, total, nomeEntidade, tipo) {
        const loading = document.getElementById('eventosModalLoading');
        const content = document.getElementById('eventosModalContent');
        const empty = document.getElementById('eventosModalEmpty');
        const tableBody = document.getElementById('eventosTableBody');
        
        // Ocultar loading
        loading.classList.add('d-none');
        
        // Atualizar informações
        document.getElementById('entidadeNome').textContent = nomeEntidade;
        document.getElementById('totalEventos').textContent = total;
        
        if (eventos.length === 0) {
            empty.classList.remove('d-none');
        } else {
            // Renderizar tabela
            tableBody.innerHTML = '';
            eventos.forEach(evento => {
                const row = this.criarLinhaEvento(evento, tipo);
                tableBody.appendChild(row);
            });
        }
        
        content.classList.remove('d-none');
    }

    criarLinhaEvento(evento, tipo) {
        const row = document.createElement('tr');
        
        const local = [evento.cidade, evento.estado].filter(Boolean).join(', ') || 'Não informado';
        const dataFim = evento.data_fim || 'Em andamento';
        
        let extraCell = '';
        const extraColumn = document.getElementById('extraColumn');
        
        if (!extraColumn.classList.contains('d-none')) {
            if (tipo === 'colaborador') {
                extraCell = `<td>${evento.funcao || 'Não informado'}</td>`;
            } else if (tipo === 'fornecedor') {
                const valor = parseFloat(evento.valor_total || 0).toLocaleString('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                });
                extraCell = `<td>${valor}</td>`;
            } else if (tipo === 'elenco') {
                extraCell = `<td>${evento.observacoes || 'Sem observações'}</td>`;
            }
        }
        
        row.innerHTML = `
            <td><strong>${evento.nome}</strong></td>
            <td>${evento.circo}</td>
            <td>${evento.data_inicio}</td>
            <td>${dataFim}</td>
            <td>${local}</td>
            ${extraCell}
        `;
        
        return row;
    }

    mostrarErro(mensagem) {
        const loading = document.getElementById('eventosModalLoading');
        const error = document.getElementById('eventosModalError');
        const errorMessage = document.getElementById('errorMessage');
        
        loading.classList.add('d-none');
        errorMessage.textContent = mensagem;
        error.classList.remove('d-none');
    }

    resetarModal() {
        // Ocultar todos os elementos
        document.getElementById('eventosModalLoading').classList.remove('d-none');
        document.getElementById('eventosModalContent').classList.add('d-none');
        document.getElementById('eventosModalError').classList.add('d-none');
        document.getElementById('eventosModalEmpty').classList.add('d-none');
        
        // Limpar conteúdo
        document.getElementById('eventosTableBody').innerHTML = '';
        document.getElementById('entidadeNome').textContent = '';
        document.getElementById('totalEventos').textContent = '0';
    }
}

// Instância global
let eventosModal;

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    eventosModal = new EventosModal();
});

// Funções globais para uso nos templates
function mostrarEventosColaborador(id, nome) {
    if (eventosModal) {
        eventosModal.mostrarEventosColaborador(id, nome);
    }
}

function mostrarEventosFornecedor(id, nome) {
    if (eventosModal) {
        eventosModal.mostrarEventosFornecedor(id, nome);
    }
}

function mostrarEventosElenco(id, nome) {
    if (eventosModal) {
        eventosModal.mostrarEventosElenco(id, nome);
    }
} 