"""Middleware для обработки InaccessibleMessage"""
import logging
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.types import InaccessibleMessage

logger = logging.getLogger(__name__)


class InaccessibleMessageMiddleware(BaseMiddleware):
    """
    Middleware, которая автоматически обрабатывает InaccessibleMessage.
    
    Если сообщение стало недоступным, middleware перехватывает ошибку
    и отправляет новое сообщение вместо редактирования.
    """
    
    async def __call__(
        self,
        handler,
        event: CallbackQuery,
        data: dict
    ):
        """
        Обработчик callback с проверкой доступности сообщения.
        
        Args:
            handler: Обработчик события
            event: CallbackQuery событие
            data: Данные dispatcher
            
        Returns:
            Результат выполнения handler или None, если сообщение недоступно
        """
        # Проверяем, доступно ли сообщение
        if isinstance(event.message, InaccessibleMessage):
            logger.warning(
                f"Сообщение callback недоступно для пользователя {event.from_user.id}, "
                f"callback: {event.data}"
            )
            # Отправляем уведомление, что сообщение устарело
            await event.answer(
                "⚠️ Сообщение устарело. Отправляю новое...",
                show_alert=True
            )
            # Отправляем новое сообщение в чат
            try:
                await event.message.answer(
                    "⚠️ Это сообщение устарело. Пожалуйста, отправьте команду заново."
                )
            except Exception as e:
                logger.error(f"Не удалось отправить новое сообщение: {e}")
            
            # Прерываем обработку
            return None
        
        # Вызываем следующий handler
        return await handler(event, data)
