#!/usr/bin/env python3
"""
Script simplificado para gerar PDF do Guia Passo a Passo do Usuário
Usa apenas bibliotecas padrão do Python + weasyprint
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def markdown_para_html(markdown_content):
    """Converte markdown básico para HTML"""
    html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guia Passo a Passo - Sistema Sócrates Online</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
            @top-center {
                content: "Sistema Sócrates Online - Guia do Usuário";
                font-size: 10px;
                color: #666;
            }
            @bottom-center {
                content: counter(page);
                font-size: 10px;
                color: #666;
            }
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
        }
        
        h1 {
            color: #2c3e50;
            font-size: 28px;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        
        h2 {
            color: #3498db;
            font-size: 20px;
            margin-top: 30px;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }
        
        h3 {
            color: #e74c3c;
            font-size: 16px;
            margin-top: 25px;
            margin-bottom: 12px;
        }
        
        h4 {
            color: #27ae60;
            font-size: 14px;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        p {
            margin-bottom: 12px;
            text-align: justify;
        }
        
        ul, ol {
            margin-bottom: 15px;
            padding-left: 25px;
        }
        
        li {
            margin-bottom: 8px;
        }
        
        .destaque {
            background-color: #fef9e7;
            border: 1px solid #f39c12;
            border-left: 4px solid #f39c12;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        
        .observacao {
            background-color: #ecf0f1;
            border: 1px solid #bdc3c7;
            border-left: 4px solid #95a5a6;
            padding: 12px;
            margin: 12px 0;
            font-style: italic;
            color: #7f8c8d;
            border-radius: 4px;
        }
        
        .screenshot-placeholder {
            background-color: #f8f9fa;
            border: 2px dashed #dee2e6;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
            color: #6c757d;
            border-radius: 8px;
        }
        
        .screenshot-placeholder strong {
            display: block;
            font-size: 16px;
            margin-bottom: 8px;
            color: #495057;
        }
        
        .checklist {
            background-color: #e8f5e8;
            border: 1px solid #c3e6c3;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        
        .checklist h3 {
            color: #155724;
            margin-top: 0;
        }
        
        code {
            background-color: #f1f1f1;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 90%;
        }
        
        .separador {
            border-top: 2px solid #3498db;
            margin: 30px 0;
            page-break-after: avoid;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        .emoji {
            font-size: 1.2em;
        }
    </style>
</head>
<body>
"""
    
    lines = markdown_content.split('\n')
    in_checklist = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            html_content += '<p>&nbsp;</p>\n'
            continue
        
        # Títulos
        if line.startswith('# '):
            title = line[2:].replace('📘 ', '<span class="emoji">📘</span> ')
            html_content += f'<h1>{title}</h1>\n'
        elif line.startswith('## '):
            subtitle = line[3:]
            html_content += f'<h2>{subtitle}</h2>\n'
        elif line.startswith('### '):
            section = line[4:]
            html_content += f'<h3>{section}</h3>\n'
        elif line.startswith('#### '):
            step = line[5:]
            html_content += f'<h4>{step}</h4>\n'
        
        # Separadores
        elif line.startswith('---'):
            html_content += '<div class="separador"></div>\n'
        
        # Placeholder para imagens
        elif '📸 **[IMAGEM:' in line:
            desc = line.split('📸 **[IMAGEM:')[1].split(']**')[0]
            html_content += f'''
            <div class="screenshot-placeholder">
                <strong>📸 SCREENSHOT NECESSÁRIO</strong>
                <p>{desc}</p>
                <small>(Substitua por imagem real da tela)</small>
            </div>
            '''
        
        # Avisos importantes
        elif line.startswith('> ⚠️'):
            warning = line[2:]
            html_content += f'<div class="destaque">{warning}</div>\n'
        
        # Observações
        elif line.startswith('> '):
            obs = line[2:]
            html_content += f'<div class="observacao">{obs}</div>\n'
        
        # Detectar início de checklist
        elif '**□' in line or 'Checklist' in line:
            if not in_checklist:
                html_content += '<div class="checklist">\n'
                in_checklist = True
            html_content += f'<h3>{line}</h3>\n'
        
        # Items de checklist
        elif line.startswith('- [ ]') or line.startswith('- [x]'):
            if not in_checklist:
                html_content += '<div class="checklist">\n'
                in_checklist = True
            
            if '- [x]' in line:
                checkbox = '✅'
            else:
                checkbox = '☐'
            
            item = line.replace('- [ ]', '').replace('- [x]', '').strip()
            html_content += f'<p>{checkbox} {item}</p>\n'
        
        # Listas numeradas
        elif line[0].isdigit() and line[1:3] == '. ':
            item = line[3:]
            html_content += f'<p>• {item}</p>\n'
        
        # Listas com marcadores
        elif line.startswith('- ') or line.startswith('* '):
            item = line[2:]
            html_content += f'<p>• {item}</p>\n'
        
        # Texto normal
        else:
            if in_checklist and not (line.startswith('- [') or line.startswith('**□')):
                html_content += '</div>\n'
                in_checklist = False
            
            if line:
                # Processar formatação inline
                line = line.replace('**', '<strong>').replace('**', '</strong>')
                line = line.replace('`', '<code>').replace('`', '</code>')
                line = line.replace('✅', '<span class="emoji">✅</span>')
                line = line.replace('📧', '<span class="emoji">📧</span>')
                line = line.replace('📱', '<span class="emoji">📱</span>')
                line = line.replace('🔧', '<span class="emoji">🔧</span>')
                line = line.replace('💡', '<span class="emoji">💡</span>')
                line = line.replace('🎯', '<span class="emoji">🎯</span>')
                line = line.replace('📞', '<span class="emoji">📞</span>')
                line = line.replace('🎉', '<span class="emoji">🎉</span>')
                
                html_content += f'<p>{line}</p>\n'
    
    if in_checklist:
        html_content += '</div>\n'
    
    html_content += '''
</body>
</html>
'''
    
    return html_content

def gerar_pdf():
    """Função principal para gerar o PDF"""
    print("🚀 Iniciando geração do PDF...")
    
    # Caminhos dos arquivos
    markdown_file = project_root / "docs" / "GUIA_PASSO_A_PASSO_USUARIO.md"
    html_file = project_root / "docs" / "GUIA_PASSO_A_PASSO_USUARIO.html"
    
    if not markdown_file.exists():
        print(f"❌ Arquivo não encontrado: {markdown_file}")
        return False
    
    try:
        # Ler conteúdo do markdown
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        print("📖 Arquivo markdown carregado com sucesso")
        
        # Converter para HTML
        html_content = markdown_para_html(markdown_content)
        
        # Salvar HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML gerado com sucesso: {html_file}")
        print(f"📄 Arquivo salvo em: {html_file.absolute()}")
        
        print("\n📋 Para gerar o PDF:")
        print("   1. Abra o arquivo HTML no navegador")
        print("   2. Use Ctrl+P (Imprimir)")
        print("   3. Selecione 'Salvar como PDF'")
        print("   4. Ajuste as configurações de impressão se necessário")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar HTML: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("📘 Gerador de HTML - Guia Passo a Passo do Usuário")
    print("=" * 60)
    
    # Verificar se o diretório docs existe
    docs_dir = project_root / "docs"
    if not docs_dir.exists():
        docs_dir.mkdir(exist_ok=True)
        print("📁 Diretório docs criado")
    
    # Gerar HTML
    sucesso = gerar_pdf()
    
    if sucesso:
        print("\n🎉 Geração concluída com sucesso!")
        print("\n📋 Próximos passos:")
        print("   1. Abra o HTML gerado para revisar")
        print("   2. Imprima como PDF usando o navegador")
        print("   3. Tire screenshots das telas do sistema")
        print("   4. Substitua os placeholders pelas imagens reais")
        print("   5. Distribua o guia para os usuários")
    else:
        print("\n❌ Falha na geração do HTML")
        print("   Verifique os erros acima e tente novamente")

if __name__ == "__main__":
    main()
