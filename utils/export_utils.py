import pandas as pd
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def create_pdf_report(transactions_df, customers_df, products_df, filters):
    """
    Genera reporte PDF profesional con gráficos y análisis
    """
    buffer = io.BytesIO()
    
    # Crear documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1E40AF'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1E40AF'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Contenido
    story = []
    
    # Título
    title = Paragraph("Global Ecommerce Analytics Report", title_style)
    story.append(title)
    
    # Fecha
    date_text = Paragraph(
        f"<para align=center>Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}</para>",
        styles['Normal']
    )
    story.append(date_text)
    story.append(Spacer(1, 20))
    
    # KPIs principales
    story.append(Paragraph("Resumen Ejecutivo", heading_style))
    
    total_revenue = transactions_df['total_amount_usd'].sum()
    total_orders = len(transactions_df)
    total_customers = transactions_df['customer_id'].nunique()
    avg_order_value = transactions_df['total_amount_usd'].mean()
    total_profit = transactions_df['profit'].sum()
    
    kpi_data = [
        ['Métrica', 'Valor'],
        ['Total Revenue', f'${total_revenue:,.2f}'],
        ['Total Orders', f'{total_orders:,}'],
        ['Total Customers', f'{total_customers:,}'],
        ['Avg Order Value', f'${avg_order_value:.2f}'],
        ['Gross Profit', f'${total_profit:,.2f}'],
        ['Profit Margin', f'{(total_profit/total_revenue*100):.1f}%']
    ]
    
    kpi_table = Table(kpi_data, colWidths=[3*inch, 3*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(kpi_table)
    story.append(Spacer(1, 20))
    
    # Top 10 países
    story.append(Paragraph("Top 10 Países por Revenue", heading_style))
    
    country_data = transactions_df.groupby('country').agg({
        'total_amount_usd': 'sum',
        'transaction_id': 'count'
    }).reset_index().nlargest(10, 'total_amount_usd')
    
    country_table_data = [['País', 'Revenue', 'Orders']]
    for _, row in country_data.iterrows():
        country_table_data.append([
            row['country'],
            f"${row['total_amount_usd']:,.0f}",
            f"{row['transaction_id']:,}"
        ])
    
    country_table = Table(country_table_data, colWidths=[2*inch, 2*inch, 2*inch])
    country_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    story.append(country_table)
    story.append(Spacer(1, 20))
    
    # Top 10 productos
    story.append(Paragraph("Top 10 Productos por Revenue", heading_style))
    
    product_data = transactions_df.groupby(['product_id', 'product_name', 'category']).agg({
        'total_amount_usd': 'sum',
        'quantity': 'sum'
    }).reset_index().nlargest(10, 'total_amount_usd')
    
    product_table_data = [['Producto', 'Categoría', 'Revenue', 'Units']]
    for _, row in product_data.iterrows():
        product_name = row['product_name'][:30] + '...' if len(row['product_name']) > 30 else row['product_name']
        product_table_data.append([
            product_name,
            row['category'],
            f"${row['total_amount_usd']:,.0f}",
            f"{row['quantity']:,}"
        ])
    
    product_table = Table(product_table_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 0.5*inch])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F59E0B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    story.append(product_table)
    story.append(Spacer(1, 20))
    
    # Análisis de categorías
    story.append(Paragraph("Revenue por Categoría", heading_style))
    
    category_data = transactions_df.groupby('category').agg({
        'total_amount_usd': 'sum',
        'profit': 'sum'
    }).reset_index().sort_values('total_amount_usd', ascending=False)
    
    category_table_data = [['Categoría', 'Revenue', 'Profit', 'Margin %']]
    for _, row in category_data.iterrows():
        margin = (row['profit'] / row['total_amount_usd'] * 100) if row['total_amount_usd'] > 0 else 0
        category_table_data.append([
            row['category'],
            f"${row['total_amount_usd']:,.0f}",
            f"${row['profit']:,.0f}",
            f"{margin:.1f}%"
        ])
    
    category_table = Table(category_table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
    category_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B5CF6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    story.append(category_table)
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer

def create_excel_report(transactions_df, customers_df, products_df, filters):
    """
    Genera reporte Excel con múltiples hojas y análisis
    """
    buffer = io.BytesIO()
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # Hoja 1: Resumen
        summary_data = {
            'Métrica': [
                'Total Revenue',
                'Total Orders',
                'Total Customers',
                'Avg Order Value',
                'Gross Profit',
                'Profit Margin (%)',
                'Total Products',
                'Total Categories'
            ],
            'Valor': [
                f"${transactions_df['total_amount_usd'].sum():,.2f}",
                f"{len(transactions_df):,}",
                f"{transactions_df['customer_id'].nunique():,}",
                f"${transactions_df['total_amount_usd'].mean():.2f}",
                f"${transactions_df['profit'].sum():,.2f}",
                f"{(transactions_df['profit'].sum()/transactions_df['total_amount_usd'].sum()*100):.2f}",
                f"{transactions_df['product_id'].nunique():,}",
                f"{transactions_df['category'].nunique():,}"
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Resumen', index=False)
        
        # Hoja 2: Transacciones (últimas 1000)
        transactions_export = transactions_df[[
            'transaction_id', 'date', 'customer_id', 'country', 'product_name',
            'category', 'quantity', 'unit_price', 'total_amount_usd', 'profit',
            'payment_method', 'device_type'
        ]].head(1000)
        transactions_export.to_excel(writer, sheet_name='Transacciones', index=False)
        
        # Hoja 3: Análisis por país
        country_analysis = transactions_df.groupby('country').agg({
            'total_amount_usd': 'sum',
            'transaction_id': 'count',
            'customer_id': 'nunique',
            'profit': 'sum'
        }).reset_index()
        country_analysis.columns = ['País', 'Revenue', 'Orders', 'Customers', 'Profit']
        country_analysis = country_analysis.sort_values('Revenue', ascending=False)
        country_analysis.to_excel(writer, sheet_name='Por País', index=False)
        
        # Hoja 4: Análisis por categoría
        category_analysis = transactions_df.groupby('category').agg({
            'total_amount_usd': 'sum',
            'transaction_id': 'count',
            'quantity': 'sum',
            'profit': 'sum'
        }).reset_index()
        category_analysis.columns = ['Categoría', 'Revenue', 'Orders', 'Units Sold', 'Profit']
        category_analysis['Profit Margin %'] = (category_analysis['Profit'] / category_analysis['Revenue'] * 100).round(2)
        category_analysis = category_analysis.sort_values('Revenue', ascending=False)
        category_analysis.to_excel(writer, sheet_name='Por Categoría', index=False)
        
        # Hoja 5: Top productos
        product_analysis = transactions_df.groupby(['product_id', 'product_name', 'category']).agg({
            'total_amount_usd': 'sum',
            'quantity': 'sum',
            'transaction_id': 'count',
            'profit': 'sum'
        }).reset_index()
        product_analysis.columns = ['Product ID', 'Product Name', 'Category', 'Revenue', 'Units', 'Orders', 'Profit']
        product_analysis = product_analysis.nlargest(100, 'Revenue')
        product_analysis.to_excel(writer, sheet_name='Top 100 Productos', index=False)
        
        # Hoja 6: Clientes VIP (top 100 por LTV)
        top_customers = customers_df.nlargest(100, 'lifetime_value')[[
            'customer_id', 'country', 'rfm_segment', 'lifetime_value',
            'total_orders', 'avg_order_value', 'churn_probability'
        ]]
        top_customers.to_excel(writer, sheet_name='Clientes VIP', index=False)
        
        # Hoja 7: Segmentación RFM
        rfm_analysis = customers_df.groupby('rfm_segment').agg({
            'customer_id': 'count',
            'lifetime_value': 'mean',
            'total_orders': 'mean',
            'churn_probability': 'mean'
        }).reset_index()
        rfm_analysis.columns = ['Segmento RFM', 'Clientes', 'LTV Promedio', 'Orders Promedio', 'Churn Prob Promedio']
        rfm_analysis = rfm_analysis.sort_values('LTV Promedio', ascending=False)
        rfm_analysis.to_excel(writer, sheet_name='Segmentación RFM', index=False)
        
        # Hoja 8: Time series (últimos 90 días)
        transactions_df['date_only'] = pd.to_datetime(transactions_df['date']).dt.date
        time_series = transactions_df.groupby('date_only').agg({
            'total_amount_usd': 'sum',
            'transaction_id': 'count'
        }).reset_index().tail(90)
        time_series.columns = ['Fecha', 'Revenue', 'Orders']
        time_series.to_excel(writer, sheet_name='Serie Temporal', index=False)
    
    buffer.seek(0)
    return buffer
