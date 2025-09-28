import asyncio
import signal


def setup_signal_handlers(bot):
    def signal_handler(signum, frame):
        bot.logger.info("Shutdown requested. Closing bot...")
        if bot.loop and not bot.loop.is_closed():
            asyncio.create_task(bot.close())
            bot.loop.call_soon_threadsafe(bot.loop.stop)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
