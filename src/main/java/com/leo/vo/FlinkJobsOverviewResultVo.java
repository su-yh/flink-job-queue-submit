package com.leo.vo;

import lombok.Data;

import java.util.List;

/**
 * @author suyh
 * @since 2024-08-17
 */
@Data
public class FlinkJobsOverviewResultVo {
    private List<FlinkJobOverviewResultVo> jobs;
}
