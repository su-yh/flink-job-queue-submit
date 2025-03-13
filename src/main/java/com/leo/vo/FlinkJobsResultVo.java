package com.leo.vo;

import lombok.Data;

import java.util.List;

/**
 * @author suyh
 * @since 2024-02-07
 */
@Data
public class FlinkJobsResultVo {
    private List<FlinkJobStatusResultVo> jobs;
}
