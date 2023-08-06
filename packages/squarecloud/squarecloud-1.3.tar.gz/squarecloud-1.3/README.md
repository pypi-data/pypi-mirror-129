## (PT-BR) Informações / (EN) Informations
(PT-BR) Este módulo foi desenvolvido com o intuito de auxiliar as pessoas de coletar informações relacionadas as suas aplicações hospedadas na https://squarecloud.app!<br>
(EN) This library was developed in order to help people collect information related to their applications hosted on https://squarecloud.app!

## (PT-BR) Instalação / (EN) Installation 
```
pip install squarecloud
```

## (PT-BR) Forma de uso padrão em Python / (EN) How to use the basic with Python

```python
from squarecloud import Square

print(Square.ram())  # 23/100MB
print(Square.used_ram())  # 23
print(Square.total_ram())  # 100

# (PT-BR) Retorna a quantidade de SSD ocupada pelo seu bot
# (EN) Returns the amount of SSD occupied by your bot
print(Square.ssd())
```

## (PT-BR) Forma de uso avançado em Python / (EN) How to use the advanced with Python

```python
from squarecloud import Square

# (PT-BR) Com conversão de MB(MegaBytes) para GB(GigaBytes) e com unidade de medida.
# (EN) With MB to GB conversion
print(Square.ram(formatted=True))  # 1.23GB/2.50GB
print(Square.used_ram(formatted=True))  # 1.23GB
print(Square.total_ram(formatted=True))  # 2.50GB

# (PT-BR) Sem conversão de B(Bytes) para MB(MegaBytes) e sem unidade de medida.
# (EN) Without Bytes conversion
print(Square.used_ram(raw=True))  # 1320702443.52
print(Square.total_ram(raw=True))  # 2684354560

# (PT-BR) Obs: O status do SSD é o mesmo jeito do básico
# (EN) Note: The SSD status is the same way of the basic.
```

## LICENSE
(PT-BR) Este projeto está licenciado sob a Licença Apache License 2.0
(EN) This project is licensed under Apache License 2.0
