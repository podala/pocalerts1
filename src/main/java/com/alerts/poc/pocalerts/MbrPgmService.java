package com.alerts.poc.pocalerts;

import java.util.Arrays;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.boot.autoconfigure.data.web.SpringDataWebProperties.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.data.domain.Page;
import org.springframework.scheduling.annotation.Async;
import java.io.IOException;
import java.util.concurrent.CompletableFuture;

@Service
public class MbrPgmService {

    @Autowired
    private MbrPgmRepository mbrPgmRepository;

    @Autowired
    private RestTemplate restTemplate;

    private static final int PAGE_SIZE = 100;

    public void processMembers() {
        List<String> statuses = Arrays.asList("3700", "3701");

        int pageNumber = 0;

        while (true) {
            PageRequest pageRequest = PageRequest.of(pageNumber, PAGE_SIZE);
            Page<MbrPgm> mbrPgmPage = mbrPgmRepository.findByCreatSysRefIdAndMbrPgmStsRefIdIn("20685", statuses, pageRequest);
            List<MbrPgm> mbrPgmList = mbrPgmPage.getContent();

            if (!mbrPgmPage.hasNext()) {
                break;
            }

            mbrPgmList.stream()
                    .map(this::processMbrPgmAsync)
                    .forEach(CompletableFuture::join);

            pageNumber++;
        }
    }

    @Async
    public CompletableFuture<Void> processMbrPgmAsync(MbrPgm mbrPgm) {
        try {
            processMbrPgm(mbrPgm);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return CompletableFuture.completedFuture(null);
    }

    private void processMbrPgm(MbrPgm mbrPgm) throws IOException {
        ObjectMapper objectMapper = new ObjectMapper();

        // Convert the mbrCovDtl from a String to a JsonNode
        JsonNode mbrCovDtl = objectMapper.readTree(mbrPgm.getMbr_cov_dtl());

        // Extract the necessary fields from mbrCovDtl
        String lastName = mbrCovDtl.get("lastName").asText();
        String firstName = mbrCovDtl.get("firstName").asText();
        String dateOfBirth = mbrCovDtl.get("dateOfBirth").asText();
        String enrolleeSourceId = mbrCovDtl.get("enrolleeSourceId").asText();
        String mbrTermDate = mbrCovDtl.get("terminationDate").asText();

        // Prepare the request body for the APIs
        EligibilityContactRequestBody requestBody = new EligibilityContactRequestBody(lastName, firstName, dateOfBirth, enrolleeSourceId);

        // Call the Eligibility API
        EligibilityApiResponse eligibilityResponse = restTemplate.postForObject("ELIGIBILITY_API_URL", requestBody, EligibilityApiResponse.class);

        // Call the Contact API
        ContactApiResponse contactResponse = restTemplate.postForObject("CONTACT_API_URL", requestBody, ContactApiResponse.class);

         // Check the termination date from the Eligibility API
              String apiTermDate = eligibilityResponse.getTerminationDate();
               if (!mbrTermDate.equals(apiTermDate)) {
                ((ObjectNode) mbrCovDtl).put("terminationDate", apiTermDate);
                 }


        // Compare address state and update mbrCovDtl
        String apiState = contactResponse.getAddresses().stream().filter(address -> address.getUse().equalsIgnoreCase("HOME")).findFirst().get().getState();
        String mbrState = mbrCovDtl.get("ConfidentialAddress").get("stateCode").asText();
        if (!mbrState.equals(apiState)) {
            ((ObjectNode) mbrCovDtl.get("ConfidentialAddress")).put("stateCode", apiState);
        }

        // Convert the updated mbrCovDtl back to a String and update the mbrPgm
        mbrPgm.setMbr_cov_dtl(mbrCovDtl.toString());

        // Save the mbrPgm back to the DB
        mbrPgmRepository.save(mbrPgm);
    }
}
