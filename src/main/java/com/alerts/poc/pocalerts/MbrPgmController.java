package com.alerts.poc.pocalerts;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/mbrPgm")
public class MbrPgmController {

    @Autowired
    private MbrPgmService mbrPgmService;

    @PostMapping("/process")
    public void processMembers() {
        mbrPgmService.processMembers();
    }
}
