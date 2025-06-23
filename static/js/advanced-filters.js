/**
 * Sistema de Filtros Avançados
 * Permite filtrar tabelas por cada campo individual
 */

class AdvancedFilters {
    constructor(tableId, config = {}) {
        this.tableId = tableId;
        this.table = document.getElementById(tableId);
        this.config = {
            containerClass: 'advanced-filters-container',
            toggleButtonClass: 'btn btn-sm btn-outline-secondary',
            filterInputClass: 'form-control form-control-sm',
            clearButtonClass: 'btn btn-sm btn-outline-danger',
            exportButtonClass: 'btn btn-sm btn-outline-success',
            ...config
        };
        
        this.filters = {};
        this.originalRows = [];
        this.init();
    }
    
    init() {
        if (!this.table) {
            console.error(`Tabela com ID ${this.tableId} não encontrada`);
            return;
        }
        
        this.storeOriginalRows();
        this.createFilterContainer();
        this.setupEventListeners();
    }
    
    storeOriginalRows() {
        const tbody = this.table.getElementsByTagName('tbody')[0];
        if (tbody) {
            this.originalRows = Array.from(tbody.getElementsByTagName('tr'));
        }
    }
    
    createFilterContainer() {
        // Buscar por .card-body primeiro, depois por .card como fallback
        let container = this.table.closest('.card-body');
        if (!container) {
            container = this.table.closest('.card');
            if (!container) return;
        }
        
        const searchRow = container.querySelector('.row.mb-3');
        if (!searchRow) return;
        
        // Criar container para filtros avançados
        const filtersContainer = document.createElement('div');
        filtersContainer.className = this.config.containerClass;
        filtersContainer.innerHTML = `
            <div class="row mb-3">
                <div class="col-12">
                    <button type="button" class="${this.config.toggleButtonClass}" id="toggleFilters">
                        <i class="bi bi-funnel me-1"></i>Filtros Avançados
                    </button>
                    <button type="button" class="${this.config.clearButtonClass} ms-2" id="clearFilters">
                        <i class="bi bi-x-circle me-1"></i>Limpar Filtros
                    </button>
                </div>
            </div>
            <div class="row mb-3 d-none" id="filtersRow">
                ${this.createColumnFilters()}
            </div>
        `;
        
        searchRow.after(filtersContainer);
    }
    
    createColumnFilters() {
        const thead = this.table.getElementsByTagName('thead')[0];
        if (!thead) return '';
        
        const headers = Array.from(thead.getElementsByTagName('th'));
        let filtersHTML = '';
        
        headers.forEach((header, index) => {
            // Pular coluna de ações
            if (header.classList.contains('no-sort') || header.textContent.toLowerCase().includes('ações')) {
                return;
            }
            
            const fieldName = this.getFieldName(header.textContent, index);
            const colSize = headers.length <= 4 ? 'col-md-3' : 'col-md-2';
            
            filtersHTML += `
                <div class="${colSize} mb-2">
                    <label class="form-label">${header.textContent}</label>
                    <input type="text" 
                           class="${this.config.filterInputClass}" 
                           id="filter_${fieldName}" 
                           placeholder="Filtrar por ${header.textContent.toLowerCase()}..."
                           data-column="${index}">
                </div>
            `;
        });
        
        return filtersHTML;
    }
    
    getFieldName(headerText, index) {
        return headerText.toLowerCase()
            .replace(/\s+/g, '_')
            .replace(/[^a-z0-9_]/g, '')
            .replace(/_{2,}/g, '_')
            .replace(/^_|_$/g, '') || `col_${index}`;
    }
    
    setupEventListeners() {
        // Toggle filtros
        const toggleBtn = document.getElementById('toggleFilters');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                const filtersRow = document.getElementById('filtersRow');
                if (filtersRow) {
                    filtersRow.classList.toggle('d-none');
                    const icon = toggleBtn.querySelector('i');
                    if (filtersRow.classList.contains('d-none')) {
                        icon.className = 'bi bi-funnel me-1';
                    } else {
                        icon.className = 'bi bi-funnel-fill me-1';
                    }
                }
            });
        }
        
        // Limpar filtros
        const clearBtn = document.getElementById('clearFilters');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                this.clearAllFilters();
            });
        }
        
        // Eventos dos filtros individuais
        setTimeout(() => {
            const filterInputs = document.querySelectorAll(`[id^="filter_"]`);
            filterInputs.forEach(input => {
                input.addEventListener('input', (e) => {
                    this.applyFilters();
                });
            });
        }, 100);
    }
    
    applyFilters() {
        const tbody = this.table.getElementsByTagName('tbody')[0];
        if (!tbody) return;
        
        const filterInputs = document.querySelectorAll(`[id^="filter_"]`);
        const filters = {};
        
        filterInputs.forEach(input => {
            const column = parseInt(input.dataset.column);
            const value = input.value.toLowerCase().trim();
            if (value) {
                filters[column] = value;
            }
        });
        
        this.originalRows.forEach(row => {
            let shouldShow = true;
            
            for (const [column, filterValue] of Object.entries(filters)) {
                const cell = row.getElementsByTagName('td')[column];
                if (cell) {
                    const cellText = cell.textContent || cell.innerText;
                    if (cellText.toLowerCase().indexOf(filterValue) === -1) {
                        shouldShow = false;
                        break;
                    }
                }
            }
            
            row.style.display = shouldShow ? '' : 'none';
        });
        
        this.updateRowCount();
    }
    
    clearAllFilters() {
        const filterInputs = document.querySelectorAll(`[id^="filter_"]`);
        filterInputs.forEach(input => {
            input.value = '';
        });
        
        // Mostrar todas as linhas
        this.originalRows.forEach(row => {
            row.style.display = '';
        });
        
        this.updateRowCount();
    }
    
    updateRowCount() {
        const visibleRows = this.originalRows.filter(row => row.style.display !== 'none');
        const countElement = document.getElementById('rowCount');
        if (countElement) {
            countElement.textContent = `${visibleRows.length} de ${this.originalRows.length} registros`;
        }
    }
    
    // Método para exportar dados filtrados
    getFilteredData() {
        const thead = this.table.getElementsByTagName('thead')[0];
        const headers = Array.from(thead.getElementsByTagName('th'))
            .filter(th => !th.classList.contains('no-sort'))
            .map(th => th.textContent.trim());
        
        const visibleRows = this.originalRows.filter(row => row.style.display !== 'none');
        const data = visibleRows.map(row => {
            const cells = Array.from(row.getElementsByTagName('td'));
            return cells.slice(0, headers.length).map(cell => {
                // Limpar texto de badges e outros elementos HTML
                const clonedCell = cell.cloneNode(true);
                const badges = clonedCell.querySelectorAll('.badge');
                badges.forEach(badge => {
                    const text = badge.textContent + ' ';
                    badge.replaceWith(text);
                });
                return clonedCell.textContent.trim();
            });
        });
        
        return { headers, data };
    }
}

// Função para inicializar filtros em uma página
function initializeAdvancedFilters(tableId, tableName) {
    const advancedFilters = new AdvancedFilters(tableId);
    
    // Configurar botão de exportação geral se existir
    const btnExportar = document.getElementById('btnExportar');
    if (btnExportar) {
        btnExportar.addEventListener('click', () => {
            showExportModal(tableName, advancedFilters);
        });
    }
    
    return advancedFilters;
}

// Modal de exportação
function showExportModal(tableName, advancedFilters) {
    const modalHTML = `
        <div class="modal fade" id="exportModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Exportar ${tableName}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Escolha o formato para exportação:</p>
                        <div class="d-grid gap-2">
                            <button class="btn btn-success" onclick="exportToExcel('${tableName}')">
                                <i class="bi bi-file-earmark-excel me-2"></i>Exportar para Excel (.xlsx)
                            </button>
                            <button class="btn btn-danger" onclick="exportToPDF('${tableName}')">
                                <i class="bi bi-file-earmark-pdf me-2"></i>Exportar para PDF
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remover modal anterior se existir
    const existingModal = document.getElementById('exportModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Adicionar modal ao body
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('exportModal'));
    window.currentAdvancedFilters = advancedFilters;
    modal.show();
}

// Funções de exportação
function exportToExcel(tableName) {
    const filteredData = window.currentAdvancedFilters.getFilteredData();
    const url = `/exportar/${tableName.toLowerCase().replace(/\s+/g, '_')}/excel`;
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(filteredData)
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${tableName}_${new Date().toISOString().split('T')[0]}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    });
    
    // Fechar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('exportModal'));
    modal.hide();
}

function exportToPDF(tableName) {
    const filteredData = window.currentAdvancedFilters.getFilteredData();
    const url = `/exportar/${tableName.toLowerCase().replace(/\s+/g, '_')}/pdf`;
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(filteredData)
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${tableName}_${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    });
    
    // Fechar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('exportModal'));
    modal.hide();
} 