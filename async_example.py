from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.python.org/downloads/")
        await page.screenshot(path="screenshot/downloads.png")
        await browser.close()

asyncio.run(main())