# Trade Opportunities API

FastAPI service that analyzes Indian market sectors and returns a structured markdown report with trade opportunities.

## Features

- `GET /analyze/{sector}` endpoint
- API key authentication using `X-API-Key`
- In-memory session tracking with server-issued cookie
- In-memory rate limiting per authenticated session
- Short-lived in-memory caching for repeated sector requests
- Input validation for sector names
- Tavily search for current market signals
- Gemini-powered markdown analysis
- OpenAPI docs available at `/docs`

## Environment Variables

Create a `.env` file in the project root:

```env
API_KEY=your-secure-api-key
TAVILY_API_KEY=your-tavily-api-key
GEMINI_API_KEY=your-gemini-api-key
RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW_SECONDS=60
SESSION_COOKIE_NAME=session_id
REQUEST_TIMEOUT_SECONDS=20
CACHE_TTL_SECONDS=300
```

## Sample Request

```powershell
curl -H "X-API-Key: your-secure-api-key" http://127.0.0.1:8000/analyze/pharmaceuticals
```

## Sample Response Shape

```json
{
  "report": "# Pharmaceuticals Sector Analysis\n..."
}
```

## Notes

- Authentication is required for every request.
- The API sets an HTTP-only session cookie and uses in-memory storage only.
- Rate limiting is enforced per authenticated session.
- Repeated requests for the same sector are served from in-memory cache until the TTL expires.
- Interactive API documentation is available at `http://127.0.0.1:8000/docs`.
