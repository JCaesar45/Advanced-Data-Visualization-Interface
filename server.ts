interface ErrorResponse {
  code: string;
  message: string;
  requestId: string;
}

class CustomApplicationError extends Error {
  constructor(
    public code: string,
    message: string,
    public details?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'CustomApplicationError';
    Object.setPrototypeOf(this, CustomApplicationError.prototype);
  }
}

function isCustomApplicationError(error: unknown): error is CustomApplicationError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'code' in error &&
    'name' in error &&
    (error as { name: string }).name === 'CustomApplicationError'
  );
}

async function handleDataTransformation<T>(input: T): Promise<T | ErrorResponse> {
  try {
    if (!input) {
      throw new CustomApplicationError('INVALID_INPUT', 'Input cannot be null or undefined');
    }
    
    await new Promise(resolve => setTimeout(resolve, 10));
    return input;
  } catch (error) {
    if (isCustomApplicationError(error)) {
      console.error(`[Error ${error.code}] ${error.message}`, error.details);
      return {
        code: error.code,
        message: error.message,
        requestId: crypto.randomUUID()
      };
    }
    
    console.error('Unexpected error during transformation', error);
    return {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
      requestId: crypto.randomUUID()
    };
  }
}
