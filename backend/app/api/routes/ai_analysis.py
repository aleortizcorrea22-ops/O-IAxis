"""
AI Analysis route — usa Claude (Anthropic) o Groq como fallback.
Prioridad: env ANTHROPIC_API_KEY → env GROQ_API_KEY → key manual del request
"""

import os
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1/ai", tags=["AI Analysis"])

CLAUDE_URL = "https://api.anthropic.com/v1/messages"
GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"
TIMEOUT    = 30.0


class AIRequest(BaseModel):
    context: dict          # datos financieros a analizar
    prompt: str            # pregunta o tipo de análisis
    provider: Optional[str] = None      # "claude" | "groq" | None = auto
    api_key: Optional[str] = None       # key manual del usuario


async def _call_claude(api_key: str, system: str, user: str) -> str:
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1024,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.post(CLAUDE_URL, headers=headers, json=body)
        if r.status_code != 200:
            raise ValueError(f"Claude error {r.status_code}: {r.text[:200]}")
        return r.json()["content"][0]["text"]


async def _call_groq(api_key: str, system: str, user: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "content-type": "application/json",
    }
    body = {
        "model": "llama-3.1-8b-instant",
        "max_tokens": 1024,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.post(GROQ_URL, headers=headers, json=body)
        if r.status_code != 200:
            raise ValueError(f"Groq error {r.status_code}: {r.text[:200]}")
        return r.json()["choices"][0]["message"]["content"]


@router.post("/analyze")
async def analyze(req: AIRequest):
    system = (
        "Sos un analista financiero experto. Analizás datos de una plataforma financiera empresarial "
        "llamada O-IAxis. Respondés en español, de forma clara y concisa. "
        "Identificás riesgos, oportunidades y recomendaciones accionables. "
        "Usás formato con bullets y secciones cuando es útil."
    )
    user = f"{req.prompt}\n\nDatos financieros:\n{req.context}"

    # Determinar qué keys hay disponibles
    env_claude = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    env_groq   = os.environ.get("GROQ_API_KEY", "").strip()
    manual_key = (req.api_key or "").strip()

    errors = []

    # Auto: Claude env → Groq env → key manual (detecta proveedor por prefijo)
    if req.provider == "claude" or (not req.provider and env_claude):
        key = env_claude or (manual_key if req.provider == "claude" else "")
        if key:
            try:
                text = await _call_claude(key, system, user)
                return {"provider": "claude", "response": text}
            except Exception as e:
                errors.append(f"Claude: {e}")

    if req.provider == "groq" or (not req.provider and env_groq):
        key = env_groq or (manual_key if req.provider == "groq" else "")
        if key:
            try:
                text = await _call_groq(key, system, user)
                return {"provider": "groq", "response": text}
            except Exception as e:
                errors.append(f"Groq: {e}")

    # Fallback: key manual sin proveedor especificado — intentar detectar
    if manual_key and not req.provider:
        if manual_key.startswith("sk-ant-"):
            try:
                text = await _call_claude(manual_key, system, user)
                return {"provider": "claude", "response": text}
            except Exception as e:
                errors.append(f"Claude (manual): {e}")
        else:
            try:
                text = await _call_groq(manual_key, system, user)
                return {"provider": "groq", "response": text}
            except Exception as e:
                errors.append(f"Groq (manual): {e}")

    raise HTTPException(
        status_code=400,
        detail=f"No hay API key configurada o falló. Errores: {'; '.join(errors) or 'Sin key disponible'}"
    )


@router.get("/status")
async def ai_status():
    """Verifica qué proveedores están configurados"""
    return {
        "claude": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "groq":   bool(os.environ.get("GROQ_API_KEY")),
        "manual_supported": True,
    }
