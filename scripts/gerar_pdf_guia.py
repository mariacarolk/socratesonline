#!/usr/bin/env python3
"""
Script para gerar PDF do Guia Passo a Passo do Usuário
Converte o markdown para PDF com formatação profissional
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, black, blue, red, green
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    from reportlab.platypus import Image as ReportLabImage
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
except ImportError:
    print("❌ Erro: Bibliotecas necessárias não encontradas.")
    print("📦 Instale as dependências com: pip install reportlab")
    sys.exit(1)

def criar_cabecalho_rodape(canvas, doc):
    """Adiciona cabeçalho e rodapé personalizados"""
    canvas.saveState()
    
    # Cabeçalho
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(HexColor("#2c3e50"))
    canvas.drawString(50, A4[1] - 30, "Sistema Sócrates Online - Guia do Usuário")
    
    # Linha do cabeçalho
    canvas.setStrokeColor(HexColor("#3498db"))
    canvas.setLineWidth(2)
    canvas.line(50, A4[1] - 40, A4[0] - 50, A4[1] - 40)
    
    # Rodapé
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(50, 30, f"Página {doc.page}")
    canvas.drawRightString(A4[0] - 50, 30, "© 2025 Sócrates Online - Todos os direitos reservados")
    
    canvas.restoreState()

def criar_estilos():
    """Cria estilos personalizados para o PDF"""
    styles = getSampleStyleSheet()
    
    # Estilo para título principal
    styles.add(ParagraphStyle(
        name='TituloPrincipal',
        parent=styles['Title'],
        fontSize=24,
        textColor=HexColor("#2c3e50"),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Estilo para subtítulos
    styles.add(ParagraphStyle(
        name='Subtitulo',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=HexColor("#3498db"),
        spaceAfter=20,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    ))
    
    # Estilo para seções
    styles.add(ParagraphStyle(
        name='Secao',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor("#e74c3c"),
        spaceAfter=15,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    ))
    
    # Estilo para passos
    styles.add(ParagraphStyle(
        name='Passo',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=HexColor("#27ae60"),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    ))
    
    # Estilo para texto normal
    styles.add(ParagraphStyle(
        name='Texto',
        parent=styles['Normal'],
        fontSize=10,
        textColor=black,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    ))
    
    # Estilo para destaque
    styles.add(ParagraphStyle(
        name='Destaque',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor("#e67e22"),
        spaceAfter=8,
        fontName='Helvetica-Bold',
        backColor=HexColor("#fef9e7"),
        borderColor=HexColor("#f39c12"),
        borderWidth=1,
        borderPadding=5
    ))
    
    # Estilo para observações
    styles.add(ParagraphStyle(
        name='Observacao',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor("#7f8c8d"),
        spaceAfter=8,
        fontName='Helvetica-Oblique',
        leftIndent=20,
        backColor=HexColor("#ecf0f1"),
        borderColor=HexColor("#bdc3c7"),
        borderWidth=1,
        borderPadding=8
    ))
    
    return styles

def processar_markdown_para_pdf(markdown_content, styles):
    """Converte conteúdo markdown para elementos PDF"""
    elements = []
    linhas = markdown_content.split('\n')
    
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()
        
        if not linha:
            elements.append(Spacer(1, 6))
            i += 1
            continue
        
        # Título principal
        if linha.startswith('# '):
            titulo = linha[2:].replace('📘 ', '📘 ')
            elements.append(Paragraph(titulo, styles['TituloPrincipal']))
            elements.append(Spacer(1, 20))
        
        # Subtítulos
        elif linha.startswith('## '):
            subtitulo = linha[3:]
            elements.append(Paragraph(subtitulo, styles['Subtitulo']))
            elements.append(Spacer(1, 15))
        
        # Seções
        elif linha.startswith('### '):
            secao = linha[4:]
            elements.append(Paragraph(secao, styles['Secao']))
            elements.append(Spacer(1, 10))
        
        # Passos
        elif linha.startswith('#### '):
            passo = linha[5:]
            elements.append(Paragraph(passo, styles['Passo']))
            elements.append(Spacer(1, 8))
        
        # Linhas horizontais
        elif linha.startswith('---'):
            elements.append(Spacer(1, 10))
            # Adicionar linha visual
            table = Table([['']],  colWidths=[7*inch])
            table.setStyle(TableStyle([
                ('LINEBELOW', (0,0), (-1,-1), 2, HexColor("#3498db")),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 10))
        
        # Placeholder para imagens
        elif '📸 **[IMAGEM:' in linha:
            descricao = linha.split('📸 **[IMAGEM:')[1].split(']**')[0]
            # Criar placeholder visual para imagem
            placeholder_table = Table([
                ['📸 PLACEHOLDER PARA SCREENSHOT'],
                [f'Descrição: {descricao}'],
                ['(Substitua por screenshot real)']
            ], colWidths=[6*inch])
            
            placeholder_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor("#f8f9fa")),
                ('TEXTCOLOR', (0, 0), (-1, -1), HexColor("#6c757d")),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, HexColor("#dee2e6")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            elements.append(Spacer(1, 10))
            elements.append(placeholder_table)
            elements.append(Spacer(1, 10))
        
        # Avisos importantes
        elif linha.startswith('> ⚠️'):
            aviso = linha[2:]
            elements.append(Paragraph(aviso, styles['Destaque']))
        
        # Observações
        elif linha.startswith('> 📸') or linha.startswith('>'):
            obs = linha[1:].strip()
            elements.append(Paragraph(obs, styles['Observacao']))
        
        # Listas numeradas
        elif linha[0].isdigit() and linha[1:3] == '. ':
            item = linha[3:]
            elements.append(Paragraph(f"• {item}", styles['Texto']))
        
        # Listas com marcadores
        elif linha.startswith('- ') or linha.startswith('* '):
            item = linha[2:]
            elements.append(Paragraph(f"• {item}", styles['Texto']))
        
        # Checkboxes
        elif '- [ ]' in linha or '- [x]' in linha or '[ ]' in linha or '[x]' in linha:
            if '- [x]' in linha or '[x]' in linha:
                checkbox = '✅'
            else:
                checkbox = '☐'
            item = linha.replace('- [ ]', '').replace('- [x]', '').replace('[ ]', '').replace('[x]', '').strip()
            elements.append(Paragraph(f"{checkbox} {item}", styles['Texto']))
        
        # Texto normal
        else:
            if linha:
                # Processar formatação inline
                linha = linha.replace('**', '<b>').replace('**', '</b>')
                linha = linha.replace('`', '<font name="Courier">')
                linha = linha.replace('`', '</font>')
                elements.append(Paragraph(linha, styles['Texto']))
        
        i += 1
    
    return elements

def gerar_pdf():
    """Função principal para gerar o PDF"""
    print("🚀 Iniciando geração do PDF...")
    
    # Caminhos dos arquivos
    markdown_file = project_root / "docs" / "GUIA_PASSO_A_PASSO_USUARIO.md"
    pdf_file = project_root / "docs" / "GUIA_PASSO_A_PASSO_USUARIO.pdf"
    
    if not markdown_file.exists():
        print(f"❌ Arquivo não encontrado: {markdown_file}")
        return False
    
    try:
        # Ler conteúdo do markdown
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        print("📖 Arquivo markdown carregado com sucesso")
        
        # Criar documento PDF
        doc = SimpleDocTemplate(
            str(pdf_file),
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=60,
            bottomMargin=60
        )
        
        # Criar estilos
        styles = criar_estilos()
        print("🎨 Estilos criados")
        
        # Processar conteúdo
        elements = processar_markdown_para_pdf(markdown_content, styles)
        print(f"📝 Processados {len(elements)} elementos")
        
        # Gerar PDF
        doc.build(elements, onFirstPage=criar_cabecalho_rodape, onLaterPages=criar_cabecalho_rodape)
        
        print(f"✅ PDF gerado com sucesso: {pdf_file}")
        print(f"📄 Arquivo salvo em: {pdf_file.absolute()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("📘 Gerador de PDF - Guia Passo a Passo do Usuário")
    print("=" * 60)
    
    # Verificar se o diretório docs existe
    docs_dir = project_root / "docs"
    if not docs_dir.exists():
        docs_dir.mkdir(exist_ok=True)
        print("📁 Diretório docs criado")
    
    # Gerar PDF
    sucesso = gerar_pdf()
    
    if sucesso:
        print("\n🎉 Geração concluída com sucesso!")
        print("\n📋 Próximos passos:")
        print("   1. Abra o PDF gerado para revisar")
        print("   2. Substitua os placeholders por screenshots reais")
        print("   3. Ajuste formatação se necessário")
        print("   4. Distribua o guia para os usuários")
    else:
        print("\n❌ Falha na geração do PDF")
        print("   Verifique os erros acima e tente novamente")

if __name__ == "__main__":
    main()
