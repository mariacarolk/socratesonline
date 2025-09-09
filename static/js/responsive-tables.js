/**
 * Sistema de Tabelas Responsivas Aprimorado
 * Melhora significativamente a experiência mobile das tabelas de listagem
 * Com suporte a gestos, acessibilidade e performance otimizada
 */

class ResponsiveTables {
    constructor() {
        this.isMobile = window.innerWidth <= 768;
        this.isSmallMobile = window.innerWidth <= 576;
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.isScrolling = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.enhanceExistingTables();
        this.handleResize();
        this.addSwipeGestures();
        this.improveAccessibility();
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
        
        tables.forEach((table, index) => {
            this.enhanceTable(table, index);
        });
        
        // Adicionar indicadores de scroll horizontal
        this.addScrollIndicators();
    }

    enhanceTable(table, index = 0) {
        if (!table) return;

        const tableContainer = table.closest('.card-body') || table.closest('.table-responsive').parentElement;
        if (!tableContainer) return;

        // Adicionar classes e atributos para melhor responsividade
        table.classList.add('table-enhanced');
        table.setAttribute('data-table-id', `table-${index}`);
        
        // Melhorar botões de ação
        this.enhanceActionButtons(table);
        
        // Adicionar indicadores de colunas em mobile
        this.addMobileColumnHints(table);
        
        // Melhorar cabeçalhos sticky
        this.addStickyHeaders(table);
        
        // Adicionar tooltips informativos
        this.addColumnTooltips(table);
        
        // Criar alternativa de cards para mobile se necessário
        if (this.shouldCreateMobileCards(table)) {
            this.createMobileCardsAlternative(table, tableContainer);
        }
        
        // Melhorar scroll horizontal
        this.enhanceHorizontalScroll(table);
    }

    enhanceActionButtons(table) {
        const actionButtons = table.querySelectorAll('.btn-group .btn, .table .btn');
        
        actionButtons.forEach(btn => {
            // Garantir que botões tenham tamanho mínimo para toque
            if (this.isMobile) {
                btn.style.minWidth = '48px';
                btn.style.minHeight = '48px';
                btn.style.fontSize = '0.9rem';
            }

            // Melhorar feedback visual e tátil
            btn.addEventListener('touchstart', function(e) {
                this.style.transform = 'scale(0.95)';
                this.style.opacity = '0.8';
                
                // Feedback tátil se disponível
                if (navigator.vibrate) {
                    navigator.vibrate(25);
                }
            }, { passive: true });

            btn.addEventListener('touchend', function(e) {
                setTimeout(() => {
                    this.style.transform = '';
                    this.style.opacity = '';
                }, 100);
            }, { passive: true });
            
            // Prevenir duplo clique acidental
            let lastTap = 0;
            btn.addEventListener('click', function(e) {
                const currentTime = new Date().getTime();
                const tapLength = currentTime - lastTap;
                if (tapLength < 300 && tapLength > 0) {
                    e.preventDefault();
                    return false;
                }
                lastTap = currentTime;
            });
        });
    }

    addMobileColumnHints(table) {
        if (!this.isMobile) return;

        // Verificar se já foi processada para evitar duplicações
        if (table.classList.contains('mobile-labels-added')) return;
        table.classList.add('mobile-labels-added');

        const headers = table.querySelectorAll('thead th');
        const rows = table.querySelectorAll('tbody tr');

        headers.forEach((header, index) => {
            if (header.classList.contains('hide-mobile') || 
                header.classList.contains('no-sort')) return;

            const headerText = header.textContent.trim();
            if (!headerText || headerText === 'Ações') return;
            
            rows.forEach(row => {
                const cell = row.cells[index];
                if (cell && !cell.querySelector('.mobile-label')) {
                    const mobileLabel = document.createElement('span');
                    mobileLabel.className = 'mobile-label d-inline d-md-none fw-bold me-2';
                    mobileLabel.textContent = headerText + ': ';
                    mobileLabel.style.cssText = `
                        color: var(--gray-600);
                        font-size: 0.75rem;
                        display: inline-block;
                        margin-right: 0.5rem;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        font-weight: 600;
                    `;
                    
                    // Inserir label antes do conteúdo
                    cell.style.padding = '0.75rem 0.5rem';
                    cell.insertBefore(mobileLabel, cell.firstChild);
                }
            });
        });
    }

    shouldCreateMobileCards(table) {
        // Criar cards alternativos para tabelas complexas em mobile
        const columnCount = table.querySelectorAll('thead th').length;
        const hasComplexContent = table.querySelectorAll('td .btn-group, td .badge, td .dropdown').length > 0;
        return this.isSmallMobile && (columnCount > 3 || hasComplexContent);
    }

    createMobileCardsAlternative(table, container) {
        // Verificar se já foi criada para evitar duplicações
        if (container.querySelector('.table-view-toggle')) {
            return;
        }

        // Criar botões de alternância
        const toggleContainer = document.createElement('div');
        toggleContainer.className = 'table-view-toggle mb-3 d-flex gap-2';
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
        mobileCards.style.display = 'none'; // Iniciar oculto
        
        // Inserir elementos
        const tableResponsive = container.querySelector('.table-responsive');
        if (tableResponsive) {
            container.insertBefore(toggleContainer, tableResponsive);
            container.insertBefore(mobileCards, tableResponsive.nextSibling);
        }
    }

    createCardsFromTable(table) {
        const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
        const rows = table.querySelectorAll('tbody tr');
        
        const cardsContainer = document.createElement('div');
        cardsContainer.className = 'table-mobile-alternative row g-3';
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            const cardWrapper = document.createElement('div');
            cardWrapper.className = 'col-12';
            
            const card = document.createElement('div');
            card.className = 'card mobile-card-item h-100';
            
            // Header do card (primeira coluna geralmente é o nome/título)
            const cardHeader = document.createElement('div');
            cardHeader.className = 'card-header mobile-card-header bg-primary text-white';
            // Remover labels mobile do conteúdo do header
            const headerContent = cells[0]?.cloneNode(true);
            if (headerContent) {
                const mobileLabels = headerContent.querySelectorAll('.mobile-label');
                mobileLabels.forEach(label => label.remove());
                cardHeader.innerHTML = headerContent.innerHTML || 'Item';
            }
            card.appendChild(cardHeader);
            
            // Body do card com informações
            const cardBody = document.createElement('div');
            cardBody.className = 'card-body mobile-card-info';
            
            // Pular primeira coluna (já usada no header) e última (ações)
            for (let i = 1; i < cells.length - 1; i++) {
                if (cells[i] && !headers[i]?.includes('Ações')) {
                    const field = document.createElement('div');
                    field.className = 'mobile-card-field mb-2';
                    
                    const label = document.createElement('small');
                    label.className = 'text-muted d-block';
                    label.textContent = headers[i];
                    
                    const value = document.createElement('div');
                    // Clonar conteúdo e remover labels mobile
                    const cellContent = cells[i].cloneNode(true);
                    const mobileLabels = cellContent.querySelectorAll('.mobile-label');
                    mobileLabels.forEach(label => label.remove());
                    value.innerHTML = cellContent.innerHTML;
                    
                    field.appendChild(label);
                    field.appendChild(value);
                    cardBody.appendChild(field);
                }
            }
            
            card.appendChild(cardBody);
            
            // Footer do card com ações
            const lastCell = cells[cells.length - 1];
            if (lastCell && lastCell.innerHTML.trim()) {
                const cardFooter = document.createElement('div');
                cardFooter.className = 'card-footer mobile-card-actions bg-light';
                // Clonar conteúdo e remover labels mobile
                const actionsContent = lastCell.cloneNode(true);
                const mobileLabels = actionsContent.querySelectorAll('.mobile-label');
                mobileLabels.forEach(label => label.remove());
                cardFooter.innerHTML = actionsContent.innerHTML;
                card.appendChild(cardFooter);
            }
            
            cardWrapper.appendChild(card);
            cardsContainer.appendChild(cardWrapper);
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

    // Novos métodos para melhor experiência mobile
    addStickyHeaders(table) {
        if (!this.isMobile) return;
        
        const tableResponsive = table.closest('.table-responsive');
        if (tableResponsive) {
            tableResponsive.style.position = 'relative';
            
            const thead = table.querySelector('thead');
            if (thead) {
                thead.style.position = 'sticky';
                thead.style.top = '0';
                thead.style.zIndex = '10';
                thead.style.backgroundColor = 'var(--gray-50)';
                thead.style.backdropFilter = 'blur(10px)';
            }
        }
    }
    
    addColumnTooltips(table) {
        const headers = table.querySelectorAll('thead th[title]');
        headers.forEach(header => {
            header.style.cursor = 'help';
            header.setAttribute('data-bs-toggle', 'tooltip');
            header.setAttribute('data-bs-placement', 'top');
        });
    }
    
    enhanceHorizontalScroll(table) {
        const tableResponsive = table.closest('.table-responsive');
        if (!tableResponsive) return;
        
        // Adicionar indicadores de scroll
        const scrollIndicator = document.createElement('div');
        scrollIndicator.className = 'scroll-indicator';
        scrollIndicator.innerHTML = '<i class="bi bi-arrow-left-right"></i> Deslize para ver mais';
        scrollIndicator.style.cssText = `
            position: absolute;
            bottom: 10px;
            right: 10px;
            background: var(--primary-800);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.75rem;
            opacity: 0.8;
            z-index: 5;
            transition: opacity 0.3s ease;
        `;
        
        if (this.isMobile && table.scrollWidth > table.clientWidth) {
            tableResponsive.style.position = 'relative';
            tableResponsive.appendChild(scrollIndicator);
            
            // Esconder indicador após scroll
            tableResponsive.addEventListener('scroll', function() {
                scrollIndicator.style.opacity = '0.3';
                setTimeout(() => {
                    if (scrollIndicator.parentElement) {
                        scrollIndicator.style.opacity = '0.8';
                    }
                }, 1000);
            });
        }
    }
    
    addScrollIndicators() {
        const tableResponsives = document.querySelectorAll('.table-responsive');
        tableResponsives.forEach(container => {
            if (container.scrollWidth > container.clientWidth) {
                container.classList.add('has-horizontal-scroll');
            }
        });
    }
    
    addSwipeGestures() {
        if (!('ontouchstart' in window)) return;
        
        const tables = document.querySelectorAll('.table-responsive');
        tables.forEach(table => {
            let startX = 0;
            let scrollLeft = 0;
            
            table.addEventListener('touchstart', (e) => {
                startX = e.touches[0].pageX - table.offsetLeft;
                scrollLeft = table.scrollLeft;
            }, { passive: true });
            
            table.addEventListener('touchmove', (e) => {
                if (!startX) return;
                
                const x = e.touches[0].pageX - table.offsetLeft;
                const walk = (x - startX) * 2;
                table.scrollLeft = scrollLeft - walk;
            }, { passive: true });
            
            table.addEventListener('touchend', () => {
                startX = 0;
            }, { passive: true });
        });
    }
    
    improveAccessibility() {
        const tables = document.querySelectorAll('.table-enhanced');
        tables.forEach(table => {
            // Adicionar atributos ARIA
            table.setAttribute('role', 'table');
            table.setAttribute('aria-label', 'Tabela de dados');
            
            // Melhorar navegação por teclado
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach((row, index) => {
                row.setAttribute('tabindex', '0');
                row.setAttribute('role', 'row');
                row.setAttribute('aria-rowindex', index + 2); // +2 porque header é 1
                
                row.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        const firstButton = row.querySelector('button, a');
                        if (firstButton) {
                            firstButton.click();
                        }
                    }
                });
            });
        });
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

