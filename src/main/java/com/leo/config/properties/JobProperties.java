package com.leo.config.properties;

import com.leo.constants.enums.JobNameEnums;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

/**
 * @author suyh
 * @since 2025-03-13
 */
@Data
public class JobProperties {
    private boolean enabled = true;

    @NotNull
    private JobNameEnums jobName;

    @NotBlank
    private String jarPath;
}
