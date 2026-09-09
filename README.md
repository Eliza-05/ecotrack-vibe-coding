# ecotrack-vibe-coding
EcoTrack MVP built with Vibe Coding principles using AI-assisted development to estimate daily carbon footprint from natural-language input.

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`.

## Estructura del proyecto

- `app.py` — interfaz de usuario (Streamlit).
- `carbon_estimator.py` — lógica de detección de actividades y cálculo de CO2e, sin dependencias de UI.
- `requirements.txt` — dependencias del proyecto.

## Desplegar en Replit

1. Crea un nuevo Repl e importa este repositorio.
2. Replit detectará `requirements.txt` e instalará las dependencias automáticamente.
3. Configura el comando de ejecución (`.replit` o "Run command") como:
   ```bash
   streamlit run app.py --server.port 8080 --server.address 0.0.0.0
   ```
