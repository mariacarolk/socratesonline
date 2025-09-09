/**
 * Sistema de Tabelas Responsivas
 * Melhora a experiência mobile das tabelas de listagem
 */

class ResponsiveTables {
    constructor() {
        this.isMobile = window.innerWidth <= 576;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.enhanceExistingTables();
        this.handleResize();
    }

    setupEventListeners() {
        // Listener para redimensionamento da janela
        window.addEventListener('resize', () => {
            clearTimeout(this.resizeTimeout);
            this.resizeTimeout = setTimeout(() => {
                this.handleResize();
            }, 250);
        });

        // Listener para botões de alternância de visualização
        document.addEventListener('click', (e) => {
            if (e.target.matches('.table-view-toggle .btn')) {
                this.handleViewToggle(e.target);
            }
        });
    }

    handleResize() {
        const wasMobile = this.isMobile;
        this.isMobile = window.innerWidth <= 576;
        
        if (wasMobile !== this.isMobile) {
            this.enhanceExistingTables();
        }
    }

    enhanceExistingTables() {
        const tables = document.querySelectorAll('.table-responsive table');
        
        tables.forEach(table => {
            this.enhanceTable(table);
        });
    }

    enhanceTable(table) {
        if (!table) return;

        const tableContainer = table.closest('.card-body');
        if (!tableContainer) return;

        // Adicionar classes para melhor responsividade
        table.classList.add('table-enhanced');
        
        // Melhorar botões de ação
        this.enhanceActionButtons(table);
        
        // Adicionar indicadores de colunas opcionais em mobile
        this.addMobileColumnHints(table);
        
        // Criar alternativa de cards para mobile (opcional)
        if (this.shouldCreateMobileCards(table)) {
            this.createMobileCardsAlternative(table, tableContainer);
        }
    }

    enhanceActionButtons(table) {
        const actionButtons = table.querySelectorAll('.btn-group .btn');
        
        actionButtons.forEach(btn => {
            // Garantir que botões tenham tamanho mínimo para toque
            if (!btn.style.minWidth) {
                btn.style.minWidth = '44px';
            }
            if (!btn.style.minHeight) {
                btn.style.minHeight = '44px';
            }

            // Melhorar feedback visual
            btn.addEventListener('touchstart', function() {
                this.style.transform = 'scale(0.95)';
            });

            btn.addEventListener('touchend', function() {
                this.style.transform = '';
            });
        });
    }

    addMobileColumnHints(table) {
        if (!this.isMobile) return;

        const headers = table.querySelectorAll('thead th');
        const rows = table.querySelectorAll('tbody tr');

        headers.forEach((header, index) => {
            if (header.classList.contains('hide-mobile') || 
                header.classList.contains('no-sort')) return;

            const headerText = header.textContent.trim();
            
            rows.forEach(row => {
                const cell = row.cells[index];
                if (cell && !cell.querySelector('.mobile-label')) {
                    const mobileLabel = document.createElement('span');
                    mobileLabel.className = 'mobile-label d-inline d-sm-none fw-bold me-2';
                    mobileLabel.textContent = headerText + ':';
                    mobileLabel.style.color = 'var(--gray-600)';
                    mobileLabel.style.fontSize = '0.75rem';
                    
                    cell.insertBefore(mobileLabel, cell.firstChild);
                }
            });
        });
    }

    shouldCreateMobileCards(table) {
        // Criar cards alternativos apenas para tabelas com muitas colunas
        const columnCount = table.querySelectorAll('thead th').length;
        return this.isMobile && columnCount > 4;
    }

    createMobileCardsAlternative(table, container) {
        const existingAlternative = container.querySelector('.table-mobile-alternative');
        if (existingAlternative) {
            existingAlternative.remove();
        }

        const existingToggle = container.querySelector('.table-view-toggle');
        if (existingToggle) {
            existingToggle.remove();
        }

        // Criar botões de alternância
        const toggleContainer = document.createElement('div');
        toggleContainer.className = 'table-view-toggle';
        toggleContainer.innerHTML = `
            <button class="btn btn-outline-primary btn-sm active" data-view="table">
                <i class="bi bi-table me-1"></i>Tabela
            </button>
            <button class="btn btn-outline-primary btn-sm" data-view="cards">
                <i class="bi bi-grid-3x2 me-1"></i>Cards
            </button>
        `;

        // Criar versão em cards
        const mobileCards = this.createCardsFromTable(table);
        
        // Inserir elementos
        const tableResponsive = container.querySelector('.table-responsive');
        container.insertBefore(toggleContainer, tableResponsive);
        container.insertBefore(mobileCards, tableResponsive.nextSibling);
    }

    createCardsFromTable(table) {
        const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
        const rows = table.querySelectorAll('tbody tr');
        
        const cardsContainer = document.createElement('div');
        cardsContainer.className = 'table-mobile-alternative';
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            const card = document.createElement('div');
            card.className = 'mobile-card-item';
            
            // Header do card (primeira coluna geralmente é o nome/título)
            const cardHeader = document.createElement('div');
            cardHeader.className = 'mobile-card-header';
            cardHeader.textContent = cells[0]?.textContent.trim() || 'Item';
            card.appendChild(cardHeader);
            
            // Informações do card
            const cardInfo = document.createElement('div');
            cardInfo.className = 'mobile-card-info';
            
            // Pular primeira coluna (já usada no header) e última (ações)
            for (let i = 1; i < cells.length - 1; i++) {
                if (cells[i] && !headers[i]?.includes('Ações')) {
                    const field = document.createElement('div');
                    field.className = 'mobile-card-field';
                    
                    const label = document.createElement('strong');
                    label.textContent = headers[i];
                    
                    const value = document.createElement('span');
                    value.innerHTML = cells[i].innerHTML;
                    
                    field.appendChild(label);
                    field.appendChild(value);
                    cardInfo.appendChild(field);
                }
            }
            
            card.appendChild(cardInfo);
            
            // Ações do card
            const lastCell = cells[cells.length - 1];
            if (lastCell) {
                const cardActions = document.createElement('div');
                cardActions.className = 'mobile-card-actions';
                cardActions.innerHTML = lastCell.innerHTML;
                card.appendChild(cardActions);
            }
            
            cardsContainer.appendChild(card);
        });
        
        return cardsContainer;
    }

    handleViewToggle(button) {
        const view = button.dataset.view;
        const container = button.closest('.card-body');
        const tableResponsive = container.querySelector('.table-responsive');
        const mobileCards = container.querySelector('.table-mobile-alternative');
        const toggleButtons = container.querySelectorAll('.table-view-toggle .btn');
        
        // Atualizar estados dos botões
        toggleButtons.forEach(btn => {
            btn.classList.remove('active');
            if (btn === button) {
                btn.classList.add('active');
            }
        });
        
        // Alternar visualizações
        if (view === 'cards') {
            tableResponsive.style.display = 'none';
            if (mobileCards) {
                mobileCards.style.display = 'block';
                mobileCards.classList.add('active');
            }
        } else {
            tableResponsive.style.display = 'block';
            if (mobileCards) {
                mobileCards.style.display = 'none';
                mobileCards.classList.remove('active');
            }
        }
    }

    // Método para atualizar tabelas dinamicamente
    refreshTable(tableId) {
        const table = document.getElementById(tableId);
        if (table) {
            this.enhanceTable(table);
        }
    }

    // Método para aplicar melhorias a uma tabela específica
    static enhance(tableSelector) {
        const instance = new ResponsiveTables();
        const table = document.querySelector(tableSelector);
        if (table) {
            instance.enhanceTable(table);
        }
        return instance;
    }
}

// Auto-inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se já existe uma instância
    if (!window.responsiveTablesInstance) {
        window.responsiveTablesInstance = new ResponsiveTables();
    }
});

// Exportar para uso global
window.ResponsiveTables = ResponsiveTables;

