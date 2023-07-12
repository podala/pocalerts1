package com.alerts.poc.pocalerts;
import org.springframework.boot.autoconfigure.data.web.SpringDataWebProperties.Pageable;
import java.util.List;
import org.springframework.data.domain.Page;
import org.springframework.data.repository.PagingAndSortingRepository;

public interface MbrPgmRepository extends PagingAndSortingRepository<MbrPgm, Long> {
    Page<MbrPgm> findByCreatSysRefIdAndMbrPgmStsRefIdIn(String creatSysRefId, List<String> mbrPgmStsRefId, Pageable pageable);
}

