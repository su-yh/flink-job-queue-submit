package com.leo.config.properties;

import lombok.Data;

import javax.validation.constraints.NotBlank;

/**
 * @author suyh
 * @since 2025-03-13
 */
@Data
public class JobProperties {
    private boolean enabled = true;

    @NotBlank
    private String jarPath;
}
