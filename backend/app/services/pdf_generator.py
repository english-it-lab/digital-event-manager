# app/services/pdf_generator.py
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

class PDFGeneratorService:
    def generate_event_program(self, program_data: dict) -> bytes:
        buffer = BytesIO()
        
        # Создаем документ
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Стиль для заголовка
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # center
        )
        
        # 1. Заголовок мероприятия
        event = program_data["event"]
        story.append(Paragraph(f"ПРОГРАММА МЕРОПРИЯТИЯ", title_style))
        story.append(Paragraph(f"«{event['name']}»", title_style))
        story.append(Spacer(1, 20))
        
        # 2. Информация о мероприятии
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6
        )
        
        story.append(Paragraph(f"Дата: {event['date']}", info_style))
        if event['venue']:
            venue = event['venue']
            story.append(Paragraph(f"Место: {venue['city']}, {venue['street']}, {venue['building']}", info_style))
        if event['organizer']:
            org = event['organizer']
            story.append(Paragraph(f"Организатор: {org['full_name']}, тел.: {org['contact']}", info_style))
        
        story.append(Spacer(1, 30))
        
        # 3. Секции и участники
        for section in program_data["sections"]:
            # Заголовок секции
            section_style = ParagraphStyle(
                'SectionTitle',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=10,
                textColor=colors.HexColor('#2C3E50')
            )
            
            story.append(Paragraph(f"Секция: {section['name']}", section_style))
            story.append(Paragraph(f"Аудитория: {section['lecture_hall']} | Время: {section['time']}", info_style))
            story.append(Spacer(1, 10))
            
            # Таблица участников
            if section['participants']:
                table_data = [["№", "ФИО участника", "Университет", "Факультет", "Тема доклада"]]
                
                for idx, participant in enumerate(section['participants'], 1):
                    poster_mark = " (постер)" if participant['is_poster'] else ""
                    table_data.append([
                        str(idx),
                        participant['full_name'] + poster_mark,
                        participant['university'],
                        participant['faculty'],
                        participant['presentation_topic'] or ""
                    ])
                
                # Создаем таблицу
                table = Table(table_data, colWidths=[1*cm, 4*cm, 4*cm, 3*cm, 5*cm])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                
                story.append(table)
            
            story.append(Spacer(1, 30))
        
        # Собираем документ
        doc.build(story)
        
        # Возвращаем PDF как bytes
        buffer.seek(0)
        return buffer.getvalue()