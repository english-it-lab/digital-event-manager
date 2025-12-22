from fastapi import APIRouter, Depends, Response, HTTPException, status
from typing import Annotated

from app.adapters.api.dependencies import get_event_program_service
from app.adapters.api.dependencies import get_pdf_generator_service

from app.services.events import EventProgramService
from app.services.pdf_generator import PDFGeneratorService
from app.schemas import EventRead, EventCreate

router = APIRouter(tags=["events"])

@router.get("/", response_model=list[EventRead])
async def list_events(
    service: Annotated[EventProgramService, Depends(get_event_program_service)],
) -> list[EventRead]:
    events = await service.list_events()
    return [
        EventRead.model_validate(events)
        for event in events
    ]


@router.post(
    "/", response_model=EventRead, status_code=status.HTTP_201_CREATED
)
async def create_event(
    payload: EventCreate,
    service: Annotated[EventProgramService, Depends(get_event_program_service)],
) -> EventRead:
    event = await service.create_event(payload)
    return EventRead.model_validate(event)


@router.get("/{event_id}/program/pdf")
async def generate_event_program_pdf(
    event_id: int,
    program_service: Annotated[EventProgramService, Depends(get_event_program_service)],
    pdf_service: Annotated[PDFGeneratorService, Depends(get_pdf_generator_service)],
):
    """
    Генерация PDF программы мероприятия
    """
    try:
        # Получаем данные для программы
        program_data = await program_service.get_event_program_data(event_id)
        
        # Генерируем PDF
        pdf_bytes = pdf_service.generate_event_program(program_data)
        
        # Возвращаем PDF как ответ
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=program_event_{event_id}.pdf"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации PDF: {str(e)}")

@router.get("/{event_id}/program/json")
async def get_event_program_json(
    event_id: int,
    program_service: Annotated[EventProgramService, Depends(get_event_program_service)],
):
    """
    Получение данных программы в формате JSON (для отладки)
    """
    try:
        program_data = await program_service.get_event_program_data(event_id)
        return program_data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))