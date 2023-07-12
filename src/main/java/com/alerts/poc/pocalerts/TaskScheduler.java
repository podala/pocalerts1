package com.alerts.poc.pocalerts;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class TaskScheduler {

    @Autowired
    private MbrPgmService mbrPgmService;

    @Scheduled(cron = "0 0 0 * * ?") // every day at midnight
    public void processMembers() {
        mbrPgmService.processMembers();
    }
}
