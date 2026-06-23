# Szyfrowanie PNG (RSA)

Program szyfruje i deszyfruje dane obrazu PNG algorytmem RSA w trybach ECB i CBC.

## Uruchomienie

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python main.py demo sample.png
```

## Biblioteki zewnętrzne

- `sympy` - generowanie liczb pierwszych
- `pycryptodome` - gotowa implementacja RSA do porównaina
