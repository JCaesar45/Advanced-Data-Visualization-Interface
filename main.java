import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.logging.Level;
import java.util.logging.Logger;

public class SecureBackendService {
    private static final Logger logger = Logger.getLogger(SecureBackendService.class.getName());
    private final ExecutorService executorService;

    public SecureBackendService(int poolSize) {
        this.executorService = Executors.newFixedThreadPool(poolSize);
    }

    public CompletableFuture<ProcessingResult> processRequestAsync(RequestPayload payload) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                validatePayload(payload);
                return executeBusinessLogic(payload);
            } catch (ValidationException e) {
                logger.log(Level.WARNING, "Validation failed for request: {0}", e.getMessage());
                throw new CompletionException(e);
            } catch (Exception e) {
                logger.log(Level.SEVERE, "Unexpected error during processing", e);
                throw new CompletionException(new SystemException("Internal processing failure", e));
            }
        }, executorService);
    }

    private void validatePayload(RequestPayload payload) throws ValidationException {
        if (payload == null || payload.getId() == null) {
            throw new ValidationException("Payload ID is required");
        }
    }

    private ProcessingResult executeBusinessLogic(RequestPayload payload) {
        return new ProcessingResult(payload.getId(), "SUCCESS", System.currentTimeMillis());
    }

    public void shutdown() {
        executorService.shutdown();
    }
}

class ValidationException extends Exception {
    public ValidationException(String message) {
        super(message);
    }
}

class SystemException extends RuntimeException {
    public SystemException(String message, Throwable cause) {
        super(message, cause);
    }
}

record RequestPayload(String id, String data) {}
record ProcessingResult(String requestId, String status, long timestamp) {}
