# Testowanie UriPoint

## Testy jednostkowe

### Uruchomienie testów
```bash
# Instalacja zależności deweloperskich
pip install -r requirements-dev.txt

# Uruchomienie wszystkich testów
pytest

# Uruchomienie testów z pokryciem kodu
pytest --cov=uripoint

# Uruchomienie konkretnego testu
pytest tests/test_video_processing.py
```

## Struktura testów

```
tests/
├── test_video_processing.py
├── test_docker_integration.py
├── test_endpoint_management.py
├── test_uri_parsing.py
└── test_stream_handling.py
```

## Przypadki testowe

### Przetwarzanie wideo
- Walidacja plików wideo
- Obsługa różnych formatów
- Przetwarzanie strumieni

### Integracja Docker
- Uruchamianie kontenerów
- Zarządzanie zasobami
- Obsługa błędów

### Zarządzanie endpointami
- Routing
- Bezpieczeństwo
- Wydajność

## Testy integracyjne

### Przygotowanie środowiska
```bash
# Uruchomienie kontenerów testowych
docker compose -f docker-compose.test.yml up -d

# Sprawdzenie statusu
docker compose ps
```

### Scenariusze testowe
1. Przetwarzanie wideo w Docker
2. Uruchamianie endpointów
3. Monitorowanie zasobów
4. Obsługa wielu strumieni

## Testy wydajnościowe

### Metryki
- Wykorzystanie CPU
- Wykorzystanie pamięci
- Czas przetwarzania wideo
- Przepustowość strumieni

### Narzędzia
```bash
# Monitoring zasobów
docker stats

# Testy obciążeniowe
python -m performance_tests
```

## Testy bezpieczeństwa

### Obszary testów
1. Walidacja wejścia
2. Kontrola dostępu
3. Bezpieczeństwo sieci
4. Obsługa błędów

### Narzędzia
- OWASP ZAP
- Nmap
- Wireshark

## Continuous Integration

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest
```

## Raportowanie błędów

### Format zgłoszenia
```
Tytuł: [Komponent] Krótki opis problemu

Środowisko:
- OS: Ubuntu 20.04
- Python: 3.8
- Docker: 20.10

Kroki do reprodukcji:
1. ...
2. ...
3. ...

Oczekiwane zachowanie:
...

Aktualne zachowanie:
...

Logi:
...
