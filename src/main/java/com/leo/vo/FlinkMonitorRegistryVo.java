package com.leo.vo;

import lombok.Data;

import javax.validation.constraints.NotNull;

/**
 * @author suyh
 * @since 2024-02-07
 */
@Data
public class FlinkMonitorRegistryVo {
    @NotNull
    private String jobId;
    @NotNull
    private String host;
    @NotNull
    private Integer port;
}
