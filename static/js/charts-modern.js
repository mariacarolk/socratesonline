/**
 * SÓCRATES ONLINE - Sistema de Gráficos Modernos
 * Configurações padronizadas para Chart.js
 */

// Paleta de cores moderna e acessível
const ChartColors = {
  primary: '#0ea5e9',     // Azul accent
  primaryLight: '#38bdf8',
  primaryDark: '#0284c7',
  
  secondary: '#1e293b',   // Azul escuro
  secondaryLight: '#334155',
  secondaryDark: '#0f172a',
  
  success: '#10b981',
  successLight: '#34d399',
  successDark: '#059669',
  
  danger: '#ef4444',
  dangerLight: '#f87171',
  dangerDark: '#dc2626',
  
  warning: '#f59e0b',
  warningLight: '#fbbf24',
  warningDark: '#d97706',
  
  info: '#3b82f6',
  infoLight: '#60a5fa',
  infoDark: '#2563eb',
  
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827'
  }
};

// Paleta de cores para gráficos com múltiplas séries
const ChartPalette = [
  '#0ea5e9', // Primary/Accent
  '#10b981', // Success
  '#f59e0b', // Warning
  '#8b5cf6', // Purple
  '#ec4899', // Pink
  '#14b8a6', // Teal
  '#f97316', // Orange
  '#06b6d4', // Cyan
  '#84cc16', // Lime
  '#6366f1'  // Indigo
];

// Configuração base para todos os gráficos
const BaseChartConfig = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false
  },
  plugins: {
    legend: {
      display: true,
      position: 'top',
      align: 'end',
      labels: {
        usePointStyle: true,
        padding: 20,
        font: {
          family: 'Inter',
          size: 12,
          weight: '500'
        },
        color: ChartColors.gray[700]
      }
    },
    tooltip: {
      enabled: true,
      backgroundColor: 'rgba(30, 41, 59, 0.95)', // secondary color
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: ChartColors.gray[700],
      borderWidth: 1,
      padding: 12,
      boxPadding: 6,
      usePointStyle: true,
      callbacks: {
        labelTextColor: () => '#fff'
      },
      titleFont: {
        family: 'Inter',
        size: 14,
        weight: '600'
      },
      bodyFont: {
        family: 'Inter',
        size: 13
      },
      cornerRadius: 8
    }
  }
};

// Configuração padrão para gráficos de linha
function getLineChartConfig(customConfig = {}) {
  return {
    ...BaseChartConfig,
    type: 'line',
    options: {
      ...BaseChartConfig,
      elements: {
        line: {
          borderWidth: 3,
          borderCapStyle: 'round',
          borderJoinStyle: 'round',
          tension: 0.4
        },
        point: {
          radius: 0,
          hitRadius: 30,
          hoverRadius: 6,
          hoverBorderWidth: 3,
          backgroundColor: '#fff'
        }
      },
      scales: {
        x: {
          grid: {
            display: false,
            drawBorder: false
          },
          ticks: {
            font: {
              family: 'Inter',
              size: 12
            },
            color: ChartColors.gray[600],
            padding: 10
          }
        },
        y: {
          grid: {
            color: ChartColors.gray[200],
            drawBorder: false,
            borderDash: [5, 5]
          },
          ticks: {
            font: {
              family: 'Inter',
              size: 12
            },
            color: ChartColors.gray[600],
            padding: 10,
            callback: function(value) {
              if (typeof value === 'number') {
                return 'R$ ' + value.toLocaleString('pt-BR', {
                  minimumFractionDigits: 0,
                  maximumFractionDigits: 0
                });
              }
              return value;
            }
          }
        }
      },
      ...customConfig
    }
  };
}

// Configuração padrão para gráficos de barra
function getBarChartConfig(customConfig = {}) {
  return {
    ...BaseChartConfig,
    type: 'bar',
    options: {
      ...BaseChartConfig,
      elements: {
        bar: {
          borderRadius: 8,
          borderSkipped: false
        }
      },
      scales: {
        x: {
          grid: {
            display: false,
            drawBorder: false
          },
          ticks: {
            font: {
              family: 'Inter',
              size: 12
            },
            color: ChartColors.gray[600],
            padding: 10
          }
        },
        y: {
          grid: {
            color: ChartColors.gray[200],
            drawBorder: false,
            borderDash: [5, 5]
          },
          ticks: {
            font: {
              family: 'Inter',
              size: 12
            },
            color: ChartColors.gray[600],
            padding: 10,
            callback: function(value) {
              if (typeof value === 'number') {
                return 'R$ ' + value.toLocaleString('pt-BR', {
                  minimumFractionDigits: 0,
                  maximumFractionDigits: 0
                });
              }
              return value;
            }
          }
        }
      },
      ...customConfig
    }
  };
}

// Configuração padrão para gráficos de pizza/donut
function getPieChartConfig(customConfig = {}) {
  return {
    ...BaseChartConfig,
    type: 'doughnut',
    options: {
      ...BaseChartConfig,
      cutout: '65%',
      plugins: {
        ...BaseChartConfig.plugins,
        legend: {
          ...BaseChartConfig.plugins.legend,
          position: 'bottom',
          align: 'center'
        }
      },
      ...customConfig
    }
  };
}

// Função para criar gradientes
function createGradient(ctx, color1, color2) {
  const gradient = ctx.createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, color1);
  gradient.addColorStop(1, color2);
  return gradient;
}

// Função para aplicar tema escuro a um gráfico
function applyDarkTheme(chartConfig) {
  if (chartConfig.options.plugins.legend) {
    chartConfig.options.plugins.legend.labels.color = '#fff';
  }
  
  if (chartConfig.options.scales) {
    if (chartConfig.options.scales.x) {
      chartConfig.options.scales.x.ticks.color = '#fff';
      chartConfig.options.scales.x.grid.color = 'rgba(255, 255, 255, 0.1)';
    }
    if (chartConfig.options.scales.y) {
      chartConfig.options.scales.y.ticks.color = '#fff';
      chartConfig.options.scales.y.grid.color = 'rgba(255, 255, 255, 0.1)';
    }
  }
  
  return chartConfig;
}

// Função utilitária para formatar valores monetários
function formatCurrency(value) {
  return 'R$ ' + value.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

// Função para criar animações customizadas
function addChartAnimation(chart) {
  chart.options.animation = {
    duration: 1000,
    easing: 'easeInOutQuart',
    onProgress: function(animation) {
      // Animação suave
    },
    onComplete: function(animation) {
      // Callback quando a animação termina
    }
  };
}

// Exportar configurações e funções
window.ChartModern = {
  colors: ChartColors,
  palette: ChartPalette,
  configs: {
    line: getLineChartConfig,
    bar: getBarChartConfig,
    pie: getPieChartConfig
  },
  utils: {
    createGradient,
    applyDarkTheme,
    formatCurrency,
    addChartAnimation
  }
}; 