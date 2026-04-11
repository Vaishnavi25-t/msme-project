package com.msme.analyzer.model;

import jakarta.persistence.*;
import java.time.LocalDate;

// This class maps to the "daily_transactions" table in MySQL
@Entity
@Table(name = "daily_transactions")
public class Transaction {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "business_id")
    private Long businessId;

    @Column(name = "entry_date")
    private LocalDate entryDate;

    @Column(name = "daily_sales")
    private Double dailySales;

    @Column(name = "daily_expenses")
    private Double dailyExpenses;

    @Column(name = "cash_balance")
    private Double cashBalance;

    // Getters and Setters (required by Spring)
    public Long getId()                    { return id; }
    public void setId(Long id)             { this.id = id; }

    public Long getBusinessId()            { return businessId; }
    public void setBusinessId(Long v)      { this.businessId = v; }

    public LocalDate getEntryDate()        { return entryDate; }
    public void setEntryDate(LocalDate v)  { this.entryDate = v; }

    public Double getDailySales()          { return dailySales; }
    public void setDailySales(Double v)    { this.dailySales = v; }

    public Double getDailyExpenses()       { return dailyExpenses; }
    public void setDailyExpenses(Double v) { this.dailyExpenses = v; }

    public Double getCashBalance()         { return cashBalance; }
    public void setCashBalance(Double v)   { this.cashBalance = v; }
}
