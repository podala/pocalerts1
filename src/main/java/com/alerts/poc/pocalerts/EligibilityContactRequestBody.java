package com.alerts.poc.pocalerts;
public class EligibilityContactRequestBody {

    private String lastName;
    private String firstName;
    private String dateOfBirth;
    private String enrolleeSourceId;

    public EligibilityContactRequestBody(String lastName, String firstName, String dateOfBirth, String enrolleeSourceId) {
        this.lastName = lastName;
        this.firstName = firstName;
        this.dateOfBirth = dateOfBirth;
        this.enrolleeSourceId = enrolleeSourceId;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getDateOfBirth() {
        return dateOfBirth;
    }

    public void setDateOfBirth(String dateOfBirth) {
        this.dateOfBirth = dateOfBirth;
    }

    public String getEnrolleeSourceId() {
        return enrolleeSourceId;
    }

    public void setEnrolleeSourceId(String enrolleeSourceId) {
        this.enrolleeSourceId = enrolleeSourceId;
    }
}

