from fastapi import APIRouter
import requests
import base64
import re
import asyncio


router = APIRouter(
    prefix = '/sideFunctionalities',
    tags = ['sideFunctionalities']
)

@router.get('/currencyRate')
async def currencyRate():
   
#    url = 'https://www.xe.com/_next/static/chunks/130.26b00c4b6d14e4f0d0d1.js'
#    response = requests.get(url)
#    content = response.text
  
#    first = ''
#    second = ''
#    # lodestar:a5LhSwW57tcaMeL1l0HbHk7zv12m7mOY - vrijednosti iz 06/07/2023
#    if len(content) > 0:
#       text_short = content.split('.concat(btoa("".concat("')[1].split('"))));')[0]
#       first = text_short.split('"')[0]
#       second = text_short.split('.concat("')[1]

#    input_string = f"{first}:{second}"
#    encoded_string = base64.b64encode(input_string.encode()).decode()

#    #bG9kZXN0YXI6YTVMaFN3VzU3dGNhTWVMMWwwSGJIazd6djEybTdtT1k=' 06/07/2023
#    url = 'https://www.xe.com/api/protected/midmarket-converter/'
#    headers = {
#       'authorization': f'Basic {encoded_string}'
#    }

#    response = await make_request(url, headers)
   
#    if response.status_code == 200:
#       data = response.json()
#       return data
#    else:
#       return print('Request failed with status code', response.status_code)

# async def make_request(url, headers):
#     loop = asyncio.get_event_loop()
#     response = await loop.run_in_executor(None, lambda: requests.get(url, headers=headers))
#     return response
# @router.get('/currencyRate')
# def currencyRate():
   # url = 'https://www.xe.com/_next/static/chunks/130.26b00c4b6d14e4f0d0d1.js'
   # response = requests.get(url)
   # content = response.text
  
   # first = ''
   # second = ''
   # # lodestar:a5LhSwW57tcaMeL1l0HbHk7zv12m7mOY - vrijednosti iz 06/07/2023

   # if len(content) > 0:
   #    text_short = content.split('.concat(btoa("".concat("')[1].split('"))));')[0]
   #    # print(text_short)
   #    first = text_short.split('"')[0]
   #    second = text_short.split('.concat("')[1]

   # # print(first)
   # # print(second)
   # input_string = f"{first}:{second}"
   # # print(input_string)
   # encoded_string = base64.b64encode(input_string.encode()).decode()
   # # print(encoded_string)


   #URL OF CURRENCY WEBSITE
   #https://www.xe.com/currencyconverter/
   url = 'https://www.xe.com/api/protected/midmarket-converter/'
   headers = {
      'authorization': f'Basic bG9kZXN0YXI6Z1NlYkxFd0ZnOTlWVWNQT1p1WW0zOHVydkxzNFhrV1U='#bG9kZXN0YXI6YTVMaFN3VzU3dGNhTWVMMWwwSGJIazd6djEybTdtT1k=' 06/07/2023
   }

   response = requests.get(url, headers=headers)

   if response.status_code == 200:
      data = response.json()
      # Process the response data as needed
      # print(data)
      return data
   else:
      return print('Request failed with status code', response.status_code)
   