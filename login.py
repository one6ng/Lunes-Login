import os
import asyncio
from pyppeteer import launch
import requests

async def send_tg(msg):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not token or not chat_id:
        return
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": msg}
    )

async def main():
    browser = await launch(headless=True, args=["--no-sandbox"])
    page = await browser.newPage()

    try:
        await page.goto("https://ctrl.lunes.host/")
        await page.type('input[type="text"]', os.getenv("LUNES_USERNAME"))
        await page.type('input[type="password"]', os.getenv("LUNES_PASSWORD"))

        await page.click('button[type="submit"]')
        await page.waitForNavigation()

        content = await page.content()

        if "Dashboard" in content or "Logout" in content:
            await send_tg("✅ Lunes.Host 登录成功")
        else:
            raise Exception("登录验证失败")

    except Exception as e:
        await send_tg(f"❌ 登录失败: {str(e)}")

    finally:
        await browser.close()

asyncio.get_event_loop().run_until_complete(main())
