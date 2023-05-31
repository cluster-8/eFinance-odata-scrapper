import csv
from .database import *
from .populate import *

def populate_tariffs_historic():
  with open('./csvs/202205TARINST.CSV', newline='', encoding='latin-1') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', )

    headersIndex = 0

    for row in reader:
      if headersIndex < 5:
        if headersIndex == 1:
          createdAt = row[0].replace('Data:', '').replace(';', '').replace(' ', '')

          print(createdAt)

        headersIndex += 1
        continue

      headersIndex += 1
    
      print(headersIndex)
  
      values = []

      for value in row:
        values.extend(value.replace('  ', '').split(';'))

      instituicao = get_financial_instituition_id_by_cnpj(values[0])

      if not instituicao:
        print('instituicao not found, cnpj:', values[0])
        continue

      servico = get_service_id_by_code(values[2].replace('.', '').replace(' ', ''), values[7].replace(' ', ''))

      if not servico:
        print('servico not found, servicoCode:', values[2].replace('.', ''), ' ', values[7].replace(' ', ''))
        continue

      insert_tariff(instituicao, servico[0], values, createdAt)
      


