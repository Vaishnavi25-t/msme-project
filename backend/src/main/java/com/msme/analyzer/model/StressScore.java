package com.msme.analyzer.model;

import jakarta.persistence.*;
import java.time.LocalDate;

// This class maps to the "stress_scores" table in MySQL
// Every time user clicks Analyze, one row is saved here
@Entity
@Table(name = "stress_scores")
public class StressScore {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "business_id")
    private Long businessId;

    @Column(name = "score_date")
    private LocalDate scoreDate;

    @Column(name = "expense_ratio")
    private Double expenseRatio;

    @Column(name = "receivables_stress")
    private Double receivablesStress;

    @Column(name = "cash_buffer_stress")
    private Double cashBufferStress;

    @Column(name = "burn_rate_stress")
    private Double burnRateStress;

    @Column(name = "sc_lss_score")
    private Double scLssScore;

    @Column(name = "risk_level")
    private String riskLevel;

    @Column(name = "survival_days")
    private Integer survivalDays;

    // ── Getters and Setters ───────────────────────────────────────
    public Long getId()                        { return id; }
    public void setId(Long id)                 { this.id = id; }

    public Long getBusinessId()                { return businessId; }
    public void setBusinessId(Long v)          { this.businessId = v; }

    public LocalDate getScoreDate()            { return scoreDate; }
    public void setScoreDate(LocalDate v)      { this.scoreDate = v; }

    public Double getExpenseRatio()            { return expenseRatio; }
    public void setExpenseRatio(Double v)      { this.expenseRatio = v; }

    public Double getReceivablesStress()       { return receivablesStress; }
    public void setReceivablesStress(Double v) { this.receivablesStress = v; }

    public Double getCashBufferStress()        { return cashBufferStress; }
    public void setCashBufferStress(Double v)  { this.cashBufferStress = v; }

    public Double getBurnRateStress()          { return burnRateStress; }
    public void setBurnRateStress(Double v)    { this.burnRateStress = v; }

    public Double getScLssScore()              { return scLssScore; }
    public void setScLssScore(Double v)        { this.scLssScore = v; }

    public String getRiskLevel()               { return riskLevel; }
    public void setRiskLevel(String v)         { this.riskLevel = v; }

    public Integer getSurvivalDays()           { return survivalDays; }
    public void setSurvivalDays(Integer v)     { this.survivalDays = v; }
}
