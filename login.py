import os
import asyncio
from pyppeteer import launch
import requests

LOGIN_URL = "https://ctrl.lunes.host/"

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
    browser = await launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )

    page = await browser.newPage()

    try:
        await page.goto(LOGIN_URL, {"waitUntil": "networkidle2", "timeout": 60000})

        await page.type('input[type="text"]', os.getenv("LUNES_USERNAME"))
        await page.type('input[type="password"]', os.getenv("LUNES_PASSWORD"))

        await page.click('button[type="submit"]')
        await page.waitForNavigation({"waitUntil": "networkidle2"})

        content = await page.content()

        if "Dashboard" in content or "Logout" in content:
            await send_tg(
                f"✅ Lunes 登录成功\n"
                f"SERVER_ID: {os.getenv('SERVER_ID')}\n"
                f"SERVER_UUID: {os.getenv('SERVER_UUID')}\n"
                f"NODE_HOST: {os.getenv('NODE_HOST')}"
            )
        else:
            raise Exception("登录验证失败")

    except Exception as e:
        await send_tg(f"❌ 登录失败: {str(e)}")

    finally:
        await browser.close()

asyncio.get_event_loop().run_until_complete(main())
