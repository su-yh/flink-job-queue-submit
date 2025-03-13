package com.leo.config;

import com.leo.config.properties.BaseProperties;
import org.springframework.boot.SpringBootConfiguration;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;

/**
 * @author suyh
 * @since 2025-03-06
 */
@EnableConfigurationProperties(BaseProperties.class)
@SpringBootConfiguration
public class AppAutoConfiguration {
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
