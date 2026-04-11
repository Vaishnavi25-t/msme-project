package com.msme.analyzer.controller;

import com.msme.analyzer.model.Transaction;
import com.msme.analyzer.repository.TransactionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.*;


@RestController
@RequestMapping("/api")
// Allow React (port 3000) to call this server (port 8080)
@CrossOrigin(origins = "http://localhost:3000")
public class AnalyzerController {

    @Autowired
    private TransactionRepository transactionRepo;

    // Read Python server URL from application.properties
    @Value("${ml.server.url}")
    private String mlServerUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    // --------------------------------------------------------
    // POST /api/analyze
    // Called by React frontend with financial data
    // Forwards to Python ML server, returns result
    // --------------------------------------------------------
    @PostMapping("/analyze")
    public ResponseEntity<Map<String, Object>> analyze(
            @RequestBody Map<String, Object> inputData) {
        try {
            // Forward the exact same data to Python
            String pythonUrl = mlServerUrl + "/api/predict";

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> request = new HttpEntity<>(inputData, headers);

            ResponseEntity<Map> response =
                restTemplate.postForEntity(pythonUrl, request, Map.class);

            return ResponseEntity.ok(response.getBody());

        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Could not connect to Python ML server. Is it running?");
            return ResponseEntity.status(503).body(error);
        }
    }

    // --------------------------------------------------------
    // POST /api/transaction
    // Saves a daily transaction to MySQL database
    // --------------------------------------------------------
    @PostMapping("/transaction")
    public ResponseEntity<Transaction> saveTransaction(
            @RequestBody Transaction transaction) {
        Transaction saved = transactionRepo.save(transaction);
        return ResponseEntity.ok(saved);
    }

    // --------------------------------------------------------
    // GET /api/transactions/{businessId}
    // Gets all transactions for a business from MySQL
    // --------------------------------------------------------
    @GetMapping("/transactions/{businessId}")
    public ResponseEntity<List<Transaction>> getTransactions(
            @PathVariable Long businessId) {
        return ResponseEntity.ok(
            transactionRepo.findByBusinessIdOrderByEntryDateDesc(businessId)
        );
    }

    // --------------------------------------------------------
    // GET /api/health
    // Test if Java server is running
    // --------------------------------------------------------
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "Java backend is running"));
    }
}