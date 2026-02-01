"""
Convex HTTP Client for Python.

Provides async HTTP methods to interact with Convex mutations,
queries, and actions from the Python backend.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, Optional

import httpx

from core.config import settings
from core.logging import get_logger

logger = get_logger(__name__)


class ConvexClientError(Exception):
    """Base exception for Convex client errors."""
    pass


class ConvexUnavailableError(ConvexClientError):
    """Raised when Convex is unavailable."""
    pass


class ConvexAuthError(ConvexClientError):
    """Raised on authentication errors."""
    pass


class ConvexClient:
    """
    HTTP client for calling Convex from Python.
    
    Provides methods to call Convex mutations via HTTP endpoints.
    Uses async HTTP for non-blocking operations.
    
    Example:
        client = ConvexClient()
        await client.mutation("analysis:upsertAnalysis", {
            "ticker": "RELIANCE.NS",
            "ltp": 2850.50,
            ...
        })
    """
    
    def __init__(
        self,
        site_url: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        timeout: float = 30.0
    ):
        """
        Initialize Convex client.
        
        Args:
            site_url: Convex site URL for HTTP endpoints
            webhook_secret: Secret for webhook authentication
            timeout: Request timeout in seconds
        """
        self.site_url = site_url or settings.convex_site_url
        self.webhook_secret = webhook_secret or settings.webhook_secret
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                headers={
                    "Content-Type": "application/json",
                    "X-Webhook-Secret": self.webhook_secret,
                }
            )
        return self._client
    
    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
    
    async def post_webhook(
        self,
        endpoint: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send data to a Convex HTTP endpoint.
        
        Args:
            endpoint: HTTP endpoint path (e.g., "/api/webhook/analysis")
            data: Data to send in request body
        
        Returns:
            Response data from Convex
        
        Raises:
            ConvexUnavailableError: If Convex is unreachable
            ConvexAuthError: If authentication fails
            ConvexClientError: For other errors
        """
        url = f"{self.site_url}{endpoint}"
        
        try:
            client = await self._get_client()
            
            logger.info(f"POST to Convex: {endpoint}", extra={
                "url": url,
                "data_keys": list(data.keys())
            })
            
            response = await client.post(url, json=data)
            
            if response.status_code == 401:
                raise ConvexAuthError("Invalid webhook secret")
            
            if response.status_code >= 500:
                raise ConvexUnavailableError(
                    f"Convex server error: {response.status_code}"
                )
            
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Convex response received", extra={
                "endpoint": endpoint,
                "status": response.status_code
            })
            
            return result
            
        except httpx.ConnectError as e:
            logger.error(f"Failed to connect to Convex: {e}")
            raise ConvexUnavailableError(f"Cannot connect to Convex: {e}")
            
        except httpx.TimeoutException as e:
            logger.error(f"Convex request timed out: {e}")
            raise ConvexUnavailableError(f"Request timed out: {e}")
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Convex HTTP error: {e}")
            raise ConvexClientError(f"HTTP error: {e}")
    
    async def update_analysis(
        self,
        ticker: str,
        analysis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send analysis results to Convex.
        
        Args:
            ticker: Stock ticker symbol
            analysis_data: Complete analysis data
        
        Returns:
            Confirmation from Convex
        """
        return await self.post_webhook("/api/webhook/analysis", {
            "ticker": ticker,
            "analysis": analysis_data,
            "timestamp": datetime.now().isoformat()
        })
    
    async def update_scan_results(
        self,
        scan_type: str,
        results: list,
        stocks_scanned: int,
        duration_ms: int
    ) -> Dict[str, Any]:
        """
        Send batch scan results to Convex.
        
        Args:
            scan_type: Type of scan (BUY, SELL, REVERSAL, ALL)
            results: List of scan results
            stocks_scanned: Number of stocks scanned
            duration_ms: Scan duration in milliseconds
        
        Returns:
            Confirmation from Convex
        """
        return await self.post_webhook("/api/webhook/scan-results", {
            "scanType": scan_type,
            "results": results,
            "stocksScanned": stocks_scanned,
            "durationMs": duration_ms,
            "timestamp": datetime.now().isoformat()
        })
    
    async def create_signal(
        self,
        ticker: str,
        signal_type: str,
        price: float,
        entry: float,
        stop_loss: float,
        targets: list,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new trading signal in Convex.
        
        Args:
            ticker: Stock ticker symbol
            signal_type: Signal type (BUY, SELL, REVERSAL)
            price: Current price
            entry: Entry price
            stop_loss: Stop loss price
            targets: List of target prices
            metadata: Additional signal metadata
        
        Returns:
            Confirmation from Convex
        """
        return await self.post_webhook("/api/webhook/signal", {
            "ticker": ticker,
            "signalType": signal_type,
            "price": price,
            "entry": entry,
            "stopLoss": stop_loss,
            "targets": targets,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat()
        })


# Global client instance
_convex_client: Optional[ConvexClient] = None


def get_convex_client() -> ConvexClient:
    """Get or create global Convex client instance."""
    global _convex_client
    if _convex_client is None:
        _convex_client = ConvexClient()
    return _convex_client


async def close_convex_client() -> None:
    """Close global Convex client."""
    global _convex_client
    if _convex_client:
        await _convex_client.close()
        _convex_client = None
