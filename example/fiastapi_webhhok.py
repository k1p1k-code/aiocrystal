from fastapi import FastAPI

from aiocrystal.v3.async_crystal import CrystalPay
from aiocrystal.utils.types import CallbackInvoice, InvoiceState
from aiocrystal.webhook import FastApiManager

import uvicorn
import asyncio

host=''

app = FastAPI()

cp=CrystalPay(auth_login='name',
     auth_secret='Secret',
     salt='Salt',
     webhook_manager=FastApiManager(
        app_fastapi=app,
        end_point_invoice='/pay/crystalpay'
     )
     )

async def AntiUnavailableIsPayed(invoice: CallbackInvoice):
    return invoice.state == InvoiceState.payed

@cp.callback_invoice(AntiUnavailableIsPayed) #<- вохможность добавлять несколько фильтров
async def pay_cp(invoice: CallbackInvoice):
    print(f'Пришло: {invoice.rub_amount}')

async def main():
    invoice=await cp.invoice.create(100, callback_url=f'{host}/pay/crystalpay')
    print(invoice.url)


asyncio.run(main())

uvicorn.run(app, host="localhost", port=5000)