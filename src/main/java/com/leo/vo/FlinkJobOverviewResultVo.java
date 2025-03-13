package com.leo.vo;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.leo.constants.enums.JobStatus;
import lombok.Data;

import java.util.Date;

/**
 * @author suyh
 * @since 2024-02-07
 */
@Data
public class FlinkJobOverviewResultVo {
    private String jid;
    private String name;
    private JobStatus state;
    @JsonProperty("start-time")
    private Date startTime;
    @JsonProperty("end-time")
    private Date endTime;
    private Long duration;
}
