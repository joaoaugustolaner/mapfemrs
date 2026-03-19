#!/bin/env python3

"""
Raspador do site da SSPRS


Esse é um raspador web com objetivo de extrair links do site da secretaria
de segurança pública. Os links contém um arquivo em formato .xlsx (Excel)
com informações sobre violências cometidas contra às mulheres desde 2012.


Como usar: python3 ssprs.py


AVISO: Esse código é rodado automaticamente seguindo a expressão CRON abaixo.

"""

from bs4 import BeautifulSoup

bs = BeautifulSoup()
start_url = "https://www.ssp.rs.gov.br/indicadores-da-violencia-contra-a-mulher"

def parser(start_url):
    return 0
