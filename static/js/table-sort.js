/**
 * Sistema de Ordenação de Tabelas
 * Adiciona funcionalidade de ordenação clicável aos cabeçalhos de tabelas
 */

class TableSorter {
    constructor(tableId) {
        this.table = document.getElementById(tableId);
        if (!this.table) {
            console.warn(`Tabela com ID '${tableId}' não encontrada`);
            return;
        }
        
        this.tbody = this.table.querySelector('tbody');
        this.headers = this.table.querySelectorAll('thead th');
        this.sortStates = {}; // armazena estado da ordenação para cada coluna
        
        this.init();
    }
    
    init() {
        // Adicionar ícones e eventos de clique aos cabeçalhos
        this.headers.forEach((header, index) => {
            // Não adicionar ordenação à coluna de ações (última coluna geralmente)
            if (header.textContent.toLowerCase().includes('ações') || 
                header.textContent.toLowerCase().includes('ação') ||
                header.classList.contains('no-sort')) {
                return;
            }
            
            // Tornar o cabeçalho clicável
            header.style.cursor = 'pointer';
            header.style.userSelect = 'none';
            header.classList.add('sortable');
            
            // Adicionar ícone de ordenação
            const originalText = header.textContent.trim();
            header.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <span>${originalText}</span>
                    <i class="bi bi-arrow-down-up text-muted sort-icon" style="font-size: 0.8em;"></i>
                </div>
            `;
            
            // Adicionar evento de clique
            header.addEventListener('click', () => this.sortTable(index));
            
            // Inicializar estado da ordenação
            this.sortStates[index] = 'none'; // 'none', 'asc', 'desc'
        });
    }
    
    sortTable(columnIndex) {
        const currentState = this.sortStates[columnIndex];
        const newState = currentState === 'asc' ? 'desc' : 'asc';
        
        // Reset todos os outros estados
        Object.keys(this.sortStates).forEach(key => {
            if (key != columnIndex) {
                this.sortStates[key] = 'none';
                this.updateSortIcon(key, 'none');
            }
        });
        
        // Atualizar estado atual
        this.sortStates[columnIndex] = newState;
        this.updateSortIcon(columnIndex, newState);
        
        // Ordenar linhas
        this.sortRows(columnIndex, newState);
    }
    
    updateSortIcon(columnIndex, state) {
        const header = this.headers[columnIndex];
        const icon = header.querySelector('.sort-icon');
        
        if (!icon) return;
        
        // Remover classes anteriores
        icon.classList.remove('bi-arrow-down-up', 'bi-arrow-up', 'bi-arrow-down', 'text-muted', 'text-primary');
        
        switch (state) {
            case 'asc':
                icon.classList.add('bi-arrow-up', 'text-primary');
                break;
            case 'desc':
                icon.classList.add('bi-arrow-down', 'text-primary');
                break;
            default:
                icon.classList.add('bi-arrow-down-up', 'text-muted');
        }
    }
    
    sortRows(columnIndex, direction) {
        const rows = Array.from(this.tbody.querySelectorAll('tr'));
        
        rows.sort((rowA, rowB) => {
            const cellA = rowA.cells[columnIndex];
            const cellB = rowB.cells[columnIndex];
            
            if (!cellA || !cellB) return 0;
            
            let valueA = this.getCellValue(cellA);
            let valueB = this.getCellValue(cellB);
            
            // Detectar tipo de dados e ordenar adequadamente
            const comparison = this.compareValues(valueA, valueB);
            
            return direction === 'asc' ? comparison : -comparison;
        });
        
        // Reorganizar as linhas na tabela
        rows.forEach(row => this.tbody.appendChild(row));
        
        // Aplicar animação sutil
        this.tbody.style.opacity = '0.7';
        setTimeout(() => {
            this.tbody.style.opacity = '1';
        }, 150);
    }
    
    getCellValue(cell) {
        // Obter o valor da célula, removendo HTML e caracteres especiais
        let value = cell.textContent || cell.innerText || '';
        
        // Limpar valor
        value = value.trim();
        
        // Remover caracteres especiais para valores monetários
        if (value.includes('R$')) {
            value = value.replace(/R\$\s*/g, '').replace(/\./g, '').replace(',', '.');
        }
        
        return value;
    }
    
    compareValues(a, b) {
        // Se ambos são vazios ou "—"
        if ((a === '' || a === '—') && (b === '' || b === '—')) return 0;
        if (a === '' || a === '—') return 1;
        if (b === '' || b === '—') return -1;
        
        // Tentar converter para números
        const numA = parseFloat(a);
        const numB = parseFloat(b);
        
        if (!isNaN(numA) && !isNaN(numB)) {
            return numA - numB;
        }
        
        // Tentar converter para datas (formato DD/MM/YYYY)
        const dateA = this.parseDate(a);
        const dateB = this.parseDate(b);
        
        if (dateA && dateB) {
            return dateA - dateB;
        }
        
        // Comparação de strings (case insensitive)
        return a.toLowerCase().localeCompare(b.toLowerCase());
    }
    
    parseDate(dateStr) {
        // Tentar parsear data no formato DD/MM/YYYY
        const match = dateStr.match(/(\d{1,2})\/(\d{1,2})\/(\d{4})/);
        if (match) {
            const [, day, month, year] = match;
            return new Date(year, month - 1, day);
        }
        
        // Tentar parsear data no formato YYYY-MM-DD
        const isoMatch = dateStr.match(/(\d{4})-(\d{1,2})-(\d{1,2})/);
        if (isoMatch) {
            return new Date(dateStr);
        }
        
        return null;
    }
}

// Função de conveniência para inicializar rapidamente
function initTableSort(tableId) {
    return new TableSorter(tableId);
}

// Auto-inicializar tabelas com classe 'sortable-table'
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.sortable-table').forEach(table => {
        new TableSorter(table.id);
    });
});

// Exportar para uso global
window.TableSorter = TableSorter;
window.initTableSort = initTableSort; 