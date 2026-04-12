package com.msme.analyzer.repository;

import com.msme.analyzer.model.StressScore;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

// Spring automatically handles all SQL for us
public interface StressScoreRepository extends JpaRepository<StressScore, Long> {
    List<StressScore> findByBusinessIdOrderByScoreDateDesc(Long businessId);
}