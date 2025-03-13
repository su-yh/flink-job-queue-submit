package com.leo.config.properties;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

/**
 * @author suyh
 * @since 2025-03-06
 */
@ConfigurationProperties(BaseProperties.PREFIX)
@Data
@Validated
public class BaseProperties {
    public static final String PREFIX = "flink.job.queue.submit";

    /**
     * flink 作业对应集群的web 监听ip
     */
    private String flinkWebHost = "localhost";
    /**
     * flink 作业对应集群的web 端口
     */
    private Integer flinkWebPort = 8081;

    @NotBlank
    private String flinkHome;
    @NotBlank
    private String cohortJobJar;
    @NotBlank
    private String realtimeJobJar;
    @NotBlank
    private String repetitionJobJar;
    @NotNull
    private Integer datesStart;
    @NotNull
    private Integer datesLast;
    private String pns;

    // 执行多少个作业之，重启一次flink 集群
    private Integer restartJobNumber = 10;
}
