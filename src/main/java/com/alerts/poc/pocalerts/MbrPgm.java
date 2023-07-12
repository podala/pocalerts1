package com.alerts.poc.pocalerts;
import java.io.Serializable;
import javax.persistence.Entity;
import javax.persistence.Table;
import javax.persistence.Id;
import javax.persistence.Column;

@Entity
@Table(name = "mbr_pgm")
public class MbrPgm implements Serializable {

    @Id
    private String mbr_pgm_id;
    private String creat_sys_ref_id;
    private String mbr_pgm_sts_ref_id;
    private String indv_key_val;
    
    // The JSON data type will be represented as a String in the Java object.
    // We will parse it as JSON when we need it.
    @Column(columnDefinition = "json")
    private String mbr_cov_dtl;

    public String getMbr_pgm_id() {
        return mbr_pgm_id;
    }

    public void setMbr_pgm_id(String mbr_pgm_id) {
        this.mbr_pgm_id = mbr_pgm_id;
    }

    public String getCreat_sys_ref_id() {
        return creat_sys_ref_id;
    }

    public void setCreat_sys_ref_id(String creat_sys_ref_id) {
        this.creat_sys_ref_id = creat_sys_ref_id;
    }

    public String getMbr_pgm_sts_ref_id() {
        return mbr_pgm_sts_ref_id;
    }

    public void setMbr_pgm_sts_ref_id(String mbr_pgm_sts_ref_id) {
        this.mbr_pgm_sts_ref_id = mbr_pgm_sts_ref_id;
    }

    public String getIndv_key_val() {
        return indv_key_val;
    }

    public void setIndv_key_val(String indv_key_val) {
        this.indv_key_val = indv_key_val;
    }

    public String getMbr_cov_dtl() {
        return mbr_cov_dtl;
    }

    public void setMbr_cov_dtl(String mbr_cov_dtl) {
        this.mbr_cov_dtl = mbr_cov_dtl;
    }
}

