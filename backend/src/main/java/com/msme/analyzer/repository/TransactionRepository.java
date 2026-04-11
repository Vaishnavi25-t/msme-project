package com.msme.analyzer.repository;
 
import com.msme.analyzer.model.Transaction;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
 
// Spring automatically creates the SQL queries for us
public interface TransactionRepository extends JpaRepository<Transaction, Long> {
    List<Transaction> findByBusinessIdOrderByEntryDateDesc(Long businessId);
}
 