import logging
import uuid
from typing import Any, Dict, Optional
from dataclasses import dataclass

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class APIResponse:
    status: int
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class DomainSpecificError(Exception):
    def __init__(self, message: str, error_code: str, details: Optional[Dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
        self.request_id = str(uuid.uuid4())

class DataProcessor:
    def __init__(self):
        self._cache: Dict[str, Any] = {}

    def process_payload(self, payload: Dict[str, Any]) -> APIResponse:
        try:
            if not isinstance(payload, dict):
                raise TypeError("Payload must be a dictionary")
            
            request_id = str(uuid.uuid4())
            logger.info(f"Processing request {request_id}", extra={"request_id": request_id})
            
            result = self._execute_logic(payload)
            return APIResponse(status=200, data=result)
            
        except TypeError as e:
            logger.warning(f"Validation failed: {str(e)}")
            return APIResponse(status=400, error=str(e))
        except DomainSpecificError as e:
            logger.error(f"Domain error {e.error_code}: {str(e)}", extra={"request_id": e.request_id})
            return APIResponse(status=422, error=e.message)
        except Exception as e:
            logger.critical(f"Unhandled exception: {str(e)}", exc_info=True)
            return APIResponse(status=500, error="Internal server error")

    def _execute_logic(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if "weight" not in payload:
            raise DomainSpecificError("Missing required field", "MISSING_WEIGHT")
        return {"processed": True, "input_weight": payload["weight"]}
