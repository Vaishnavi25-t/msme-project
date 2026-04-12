package com.msme.analyzer.controller;

import com.msme.analyzer.model.StressScore;
import com.msme.analyzer.model.Transaction;
import com.msme.analyzer.repository.StressScoreRepository;
import com.msme.analyzer.repository.TransactionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.time.LocalDate;
import java.util.*;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class AnalyzerController {

    @Autowired
    private TransactionRepository transactionRepo;

    @Autowired
    private StressScoreRepository stressScoreRepo;

    @Value("${ml.server.url}")
    private String mlServerUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    @PostMapping("/analyze")
    public ResponseEntity<Map<String, Object>> analyze(
            @RequestBody Map<String, Object> inputData) {

        System.out.println("=== /api/analyze called ===");
        System.out.println("Input received: " + inputData);

        try {
            // ── STEP 1: Save to daily_transactions ──────────────
            System.out.println("Step 1: Saving to daily_transactions...");

            Transaction txn = new Transaction();
            txn.setBusinessId(1L);
            txn.setEntryDate(LocalDate.now());
            txn.setDailySales(toDouble(inputData.get("daily_sales")));
            txn.setDailyExpenses(toDouble(inputData.get("daily_expenses")));
            txn.setCashBalance(toDouble(inputData.get("cash_balance")));
            transactionRepo.save(txn);

            System.out.println("Step 1 DONE: Transaction saved with id = " + txn.getId());

            // ── STEP 2: Call Python ML ───────────────────────────
            System.out.println("Step 2: Calling Python ML at " + mlServerUrl + "/api/predict");

            String pythonUrl = mlServerUrl + "/api/predict";
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> request = new HttpEntity<>(inputData, headers);

            ResponseEntity<Map> mlResponse =
                restTemplate.postForEntity(pythonUrl, request, Map.class);

            Map<String, Object> mlResult = mlResponse.getBody();
            System.out.println("Step 2 DONE: ML response = " + mlResult);

            if (mlResult == null) {
                throw new RuntimeException("ML server returned empty response");
            }

            // ── STEP 3: Save ML result to stress_scores ──────────
            System.out.println("Step 3: Saving to stress_scores...");

            StressScore score = new StressScore();
            score.setBusinessId(1L);
            score.setScoreDate(LocalDate.now());
            score.setExpenseRatio(toDouble(mlResult.get("expense_ratio")));
            score.setReceivablesStress(toDouble(mlResult.get("receivables_stress")));
            score.setCashBufferStress(toDouble(mlResult.get("cash_buffer_stress")));
            score.setBurnRateStress(toDouble(mlResult.get("burn_rate_stress")));
            score.setScLssScore(toDouble(mlResult.get("sc_lss_score")));
            score.setRiskLevel(
                mlResult.get("risk_label") != null
                    ? mlResult.get("risk_label").toString()
                    : "Unknown"
            );
            score.setSurvivalDays(toInteger(mlResult.get("survival_days")));
            stressScoreRepo.save(score);

            System.out.println("Step 3 DONE: StressScore saved with id = " + score.getId());
            System.out.println("=== COMPLETE — both tables saved ===");

            return ResponseEntity.ok(mlResult);

        } catch (Exception e) {
            System.out.println("ERROR at /api/analyze: " + e.getMessage());
            e.printStackTrace();
            Map<String, Object> error = new HashMap<>();
            error.put("error", e.getMessage());
            return ResponseEntity.status(500).body(error);
        }
    }

    @GetMapping("/transactions/{businessId}")
    public ResponseEntity<List<Transaction>> getTransactions(
            @PathVariable Long businessId) {
        return ResponseEntity.ok(
            transactionRepo.findByBusinessIdOrderByEntryDateDesc(businessId)
        );
    }

    @GetMapping("/scores/{businessId}")
    public ResponseEntity<List<StressScore>> getScores(
            @PathVariable Long businessId) {
        return ResponseEntity.ok(
            stressScoreRepo.findByBusinessIdOrderByScoreDateDesc(businessId)
        );
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "Java backend is running"));
    }

    private Double toDouble(Object val) {
        if (val == null) return 0.0;
        try { return Double.valueOf(val.toString()); }
        catch (Exception e) { return 0.0; }
    }

    private Integer toInteger(Object val) {
        if (val == null) return 0;
        try { return (int) Double.parseDouble(val.toString()); }
        catch (Exception e) { return 0; }
    }
}