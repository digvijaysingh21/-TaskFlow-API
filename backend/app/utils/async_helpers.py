import asyncio
import httpx
from typing import Any, Callable, Coroutine


async def run_concurrent(*coroutines: Coroutine) -> list[Any]:
    """
    Run multiple coroutines concurrently using asyncio.gather.
    Returns results in the same order as input coroutines.
    
    Usage:
        tasks, user = await run_concurrent(
            fetch_tasks(project_id),
            fetch_user(user_id),
        )
    """
    return await asyncio.gather(*coroutines)


async def run_concurrent_safe(*coroutines: Coroutine) -> list[Any | Exception]:
    """
    Same as run_concurrent but never raises — returns exceptions as values.
    Use when partial failure is acceptable.
    """
    return await asyncio.gather(*coroutines, return_exceptions=True)


async def fetch_external(
    url: str,
    method: str = "GET",
    headers: dict = None,
    json: dict = None,
    timeout: float = 10.0,
) -> dict:
    """
    Make an async HTTP request to an external API.
    Used for calling LLM APIs (Groq, OpenAI) from FastAPI routes.
    
    Usage:
        data = await fetch_external(
            url="https://api.groq.com/openai/v1/chat/completions",
            method="POST",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": "llama3-8b-8192", "messages": [...]},
        )
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.request(
            method=method,
            url=url,
            headers=headers or {},
            json=json,
        )
        response.raise_for_status()
        return response.json()


async def retry_async(
    coroutine_fn: Callable,
    retries: int = 3,
    delay: float = 1.0,
    *args,
    **kwargs,
) -> Any:
    """
    Retry an async function up to `retries` times with a delay between attempts.
    Useful for flaky external API calls.
    
    Usage:
        result = await retry_async(fetch_external, retries=3, delay=0.5, url="...")
    """
    last_exception = None
    for attempt in range(retries):
        try:
            return await coroutine_fn(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < retries - 1:
                await asyncio.sleep(delay * (attempt + 1))  # exponential backoff
    raise last_exception